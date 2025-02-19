import numpy as np
import pygame
from pygame.locals import *
from collections import deque, defaultdict
import concurrent.futures
from itertools import combinations
from tqdm import tqdm
import random
from collections import defaultdict
from zone_stats import assign_zones, calculate_color, calculate_defense_range


def normalize(v):
    return v / np.linalg.norm(v)

def generate_icosahedron():
    phi = (1 + np.sqrt(5)) / 2
    vertices = np.array([
        [-1, phi, 0], [1, phi, 0], [-1, -phi, 0], [1, -phi, 0],
        [0, -1, phi], [0, 1, phi], [0, -1, -phi], [0, 1, -phi],
        [phi, 0, -1], [phi, 0, 1], [-phi, 0, -1], [-phi, 0, 1]
    ])
    vertices /= np.linalg.norm(vertices, axis=1)[:, np.newaxis]
    faces = np.array([
        [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
        [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
        [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
        [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1]
    ])
    return vertices, faces

def midpoint(v1, v2):
    return (v1 + v2) / 2.0

def subdivide(vertices, faces):
    mid_cache = {}
    new_faces = []

    def add_midpoint(v1, v2):
        nonlocal vertices
        smaller, larger = min(v1, v2), max(v1, v2)
        if (smaller, larger) in mid_cache:
            return mid_cache[(smaller, larger)]
        mid_vertex = midpoint(vertices[smaller], vertices[larger])
        mid_vertex = normalize(mid_vertex)
        mid_cache[(smaller, larger)] = len(vertices)
        vertices = np.vstack([vertices, mid_vertex])
        return mid_cache[(smaller, larger)]

    for tri in faces:
        a, b, c = tri
        ab = add_midpoint(a, b)
        bc = add_midpoint(b, c)
        ca = add_midpoint(c, a)

        new_faces.append([a, ab, ca])
        new_faces.append([b, bc, ab])
        new_faces.append([c, ca, bc])
        new_faces.append([ab, bc, ca])

    return vertices, new_faces

def create_spherical_mesh(subdivisions=2):
    vertices, faces = generate_icosahedron()
    for _ in range(subdivisions):
        vertices, faces = subdivide(vertices, faces)
    return vertices, faces




def build_face_graph(faces):
    graph = defaultdict(list)
    face_edges = [{tuple(sorted([face[i], face[(i + 1) % 3]])) for i in range(3)} for face in faces]

    for i, edges1 in enumerate(face_edges):
        for j, edges2 in enumerate(face_edges):
            if i != j and len(edges1 & edges2) == 1:
                graph[i].append(j)

    return graph

def calculate_total_distances(faces, zones):
    spawn_indices = [i for i, zone in enumerate(zones) if zone == "spawn"]
    num_spawns = len(spawn_indices)

    face_graph = build_face_graph(faces)
    total_distances = []

    def bfs(start):
        queue = deque([(start, 0)])
        visited = {start}
        distances = {start: 0}
        while queue:
            current, dist = queue.popleft()
            for neighbor in face_graph[current]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    distances[neighbor] = dist + 1
                    queue.append((neighbor, dist + 1))
        return distances

    for i in range(num_spawns):
        distances_dict = dict(bfs(spawn_indices[i]))
        total_distance = sum(distances_dict.get(spawn_index, float('inf')) for spawn_index in spawn_indices if spawn_index != spawn_indices[i])
        total_distances.append((spawn_indices[i], total_distance))

    return total_distances






def rotate_vertices(vertices, angle_x, angle_y):
    rotation_matrix_x = np.array([
        [1, 0, 0],
        [0, np.cos(angle_x), -np.sin(angle_x)],
        [0, np.sin(angle_x), np.cos(angle_x)]
    ])
    rotation_matrix_y = np.array([
        [np.cos(angle_y), 0, np.sin(angle_y)],
        [0, 1, 0],
        [-np.sin(angle_y), 0, np.cos(angle_y)]
    ])
    rotated_vertices = np.dot(vertices, rotation_matrix_x)
    rotated_vertices = np.dot(rotated_vertices, rotation_matrix_y)
    return rotated_vertices


def visualize_sphere_pygame(vertices, faces, zones):
    pygame.init()
    screen_width, screen_height = 1400, 800  # Increased size for better visibility
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Spherical Mesh Visualization')
    clock = pygame.time.Clock()

    running = True
    angle_x, angle_y = 0, 0
    zoom = 300
    clicked_face = None
    selected_zone = None  # To keep track of the selected zone

    # Calculate defense range for color normalization
    min_defense, max_defense = calculate_defense_range(zones)

    def display_zone_stats(screen, zone):
        font = pygame.font.SysFont('Arial', 16)
        stats_text = [
            f"Zone Index: {zone.index}",
            f"Type: {zone.zone_type}",
            f"Goop Saturation: {zone.goop_sv:.2f}",
            f"Gold per Year: {zone.gold_py:.2f}",
            f"Defense: {zone.defense:.2f}"
        ]

        # Position to display the stats
        x, y = 20, 20  # Adjust as needed

        # Background rectangle
        pygame.draw.rect(screen, (50, 50, 50), (x - 10, y - 10, 220, 130))

        for line in stats_text:
            text_surface = font.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (x, y))
            y += 20

    def project_vertex(vertex, zoom, screen, offset_x=0):
        x = vertex[0] * zoom + screen.get_width() / 3 + offset_x
        y = -vertex[1] * zoom + screen.get_height() / 2
        return (x, y)

    def is_face_visible(face, vertices):
        v1, v2, v3 = vertices[face[0]], vertices[face[1]], vertices[face[2]]
        normal = np.cross(v2 - v1, v3 - v1)
        to_camera = np.array([0, 0, 1])
        return np.dot(normal, to_camera) < 0

    def point_in_triangle(pt, v1, v2, v3):
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        d1 = sign(pt, v1, v2)
        d2 = sign(pt, v2, v3)
        d3 = sign(pt, v3, v1)

        has_neg = (d1 < 0) or (d2 < 0) or (d3 < 0)
        has_pos = (d1 > 0) or (d2 > 0) or (d3 > 0)

        return not (has_neg and has_pos)

    def get_clicked_face(mouse_pos, vertices, faces):
        for i, face in enumerate(faces):
            if is_face_visible(face, vertices):
                projected_points = [project_vertex(vertices[j], zoom, screen) for j in face]
                if point_in_triangle(mouse_pos, *projected_points):
                    return i
        return None

    def build_face_graph(faces):
        graph = defaultdict(list)
        edge_dict = defaultdict(list)
        for idx, face in enumerate(faces):
            edges = [(face[i], face[(i + 1) % 3]) for i in range(3)]
            for edge in edges:
                edge = tuple(sorted(edge))
                edge_dict[edge].append(idx)
        for edge, face_list in edge_dict.items():
            if len(face_list) == 2:
                a, b = face_list
                graph[a].append(b)
                graph[b].append(a)
        return graph

    def rotate_vertices(vertices, angle_x, angle_y):
        rotation_x = np.array([[1, 0, 0],
                               [0, np.cos(angle_x), -np.sin(angle_x)],
                               [0, np.sin(angle_x), np.cos(angle_x)]])
        rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                               [0, 1, 0],
                               [-np.sin(angle_y), 0, np.cos(angle_y)]])
        return np.dot(vertices, np.dot(rotation_y, rotation_x))

    def flatten_triangle(vertices_3d, angle_x, angle_y):
        # Rotate the vertices to align with the current view
        rotated_vertices = rotate_vertices(np.array(vertices_3d), angle_x, angle_y)
        v0, v1, v2 = rotated_vertices

        # Edge vectors
        e1 = v1 - v0
        e2 = v2 - v0

        # Compute the normal vector
        normal = np.cross(e1, e2)
        normal /= np.linalg.norm(normal)  # Normalize

        # Compute the centroid
        centroid = (v0 + v1 + v2) / 3

        # Ensure the normal points outward
        if np.dot(normal, centroid) < 0:
            normal = -normal  # Flip the normal vector

        # Choose a stable reference axis from the world axes
        if abs(normal[1]) < 0.9:
            x_axis_world = np.array([0, 1, 0])
        else:
            x_axis_world = np.array([1, 0, 0])

        # Compute the local axes
        x_axis = np.cross(x_axis_world, normal)
        x_axis /= np.linalg.norm(x_axis)
        y_axis = np.cross(x_axis, normal)

        # Negate x_axis to correct mirror image
        x_axis = -x_axis

        # Project vertices onto the local axes
        projected_points = []
        for vertex in [v0, v1, v2]:
            vec = vertex - v0  # Use v0 as the origin
            x = np.dot(vec, x_axis)
            y = np.dot(vec, y_axis)
            projected_points.append(np.array([x, y]))
        p0, p1, p2 = projected_points

        return [p0, p1, p2], x_axis, y_axis, v0, normal

    face_graph = build_face_graph(faces)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_face = get_clicked_face(event.pos, rotated_vertices, faces)
                    if clicked_face is not None:
                        selected_zone = zones[clicked_face]  # Get the selected zone
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    angle_y -= 0.1
                elif event.key == K_RIGHT:
                    angle_y += 0.1
                elif event.key == K_UP:
                    angle_x -= 0.1
                elif event.key == K_DOWN:
                    angle_x += 0.1

        screen.fill((0, 0, 0))

        rotated_vertices = rotate_vertices(vertices, angle_x, angle_y)
        projected_vertices = [project_vertex(v, zoom, screen) for v in rotated_vertices]

        # Draw the 3D sphere visualization on the left
        projected_faces = []  # To keep track for click detection
        for i, face in enumerate(faces):
            if is_face_visible(face, rotated_vertices):
                points = [projected_vertices[j] for j in face]
                projected_faces.append(points)
                zone = zones[i]
                # Calculate color based on zone type and defense
                color = calculate_color(zone, min_defense, max_defense)
                pygame.draw.polygon(screen, color, points)
                pygame.draw.polygon(screen, (0, 0, 0), points, 1)
                if i == clicked_face:
                    pygame.draw.polygon(screen, (255, 255, 0), points, 3)
            else:
                projected_faces.append(None)  # Placeholder

        # Draw the selected face and neighbors on the right
        if clicked_face is not None:
            center_x = 2 * screen.get_width() / 3
            center_y = screen.get_height() / 2

            size = 300  # Increased size for better visibility
            selected_face = faces[clicked_face]
            selected_vertices_indices = selected_face
            selected_vertices = [vertices[idx] for idx in selected_vertices_indices]

            # Flatten the selected triangle to 2D with correct orientation
            tri_2d, x_axis, y_axis, v0, normal_sel = flatten_triangle(selected_vertices, angle_x, angle_y)

            # Scale and translate the triangle to the right side
            tri_2d = [p * size for p in tri_2d]
            tri_center = sum(tri_2d) / 3
            tri_2d = [p - tri_center + np.array([center_x, center_y]) for p in tri_2d]

            # Draw the selected triangle
            zone = zones[clicked_face]
            color = calculate_color(zone, min_defense, max_defense)
            pygame.draw.polygon(screen, color, tri_2d)
            pygame.draw.polygon(screen, (0, 0, 0), tri_2d, 1)

            # Mapping from global vertex indices to positions in tri_2d
            index_to_pos = {selected_vertices_indices[i]: tri_2d[i] for i in range(3)}

            # Retrieve the neighbors of the selected face
            neighbors = face_graph[clicked_face]

            # Draw neighboring triangles
            for neighbor_idx in neighbors:
                neighbor_face = faces[neighbor_idx]
                neighbor_vertices_indices = neighbor_face
                neighbor_vertices = [rotated_vertices[idx] for idx in neighbor_vertices_indices]
                neighbor_tri_2d = []

                for vertex in neighbor_vertices:
                    # Compute vector from v0 to the vertex
                    vec = vertex - v0
                    # Project onto the same 2D plane using x_axis and y_axis
                    x = np.dot(vec, x_axis)
                    y = np.dot(vec, y_axis)
                    neighbor_tri_2d.append(np.array([x, y]) * size)

                # Adjust positions to fit the display
                neighbor_tri_2d = [p - tri_center + np.array([center_x, center_y]) for p in neighbor_tri_2d]

                # Draw the neighbor triangle
                neighbor_zone = zones[neighbor_idx]
                color = calculate_color(neighbor_zone, min_defense, max_defense)
                pygame.draw.polygon(screen, color, neighbor_tri_2d)
                pygame.draw.polygon(screen, (0, 0, 0), neighbor_tri_2d, 1)

            # Display stats for the selected zone
            display_zone_stats(screen, selected_zone)

        pygame.display.flip()
        clock.tick(60)


    pygame.quit()
