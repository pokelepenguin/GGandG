import numpy as np
import pygame
from pygame.locals import *
from collections import deque, defaultdict
import concurrent.futures
from itertools import combinations
from tqdm import tqdm
import random
from collections import defaultdict



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




def assign_zones(faces, num_players):
    num_faces = len(faces)

    # Initialize all faces as "normal" zones
    zones = ["normal"] * num_faces

    # Define spawn points for different player counts
    spawn_points = {
        2: [152, 264],
        4: [7, 40, 207, 244],
        5: [11, 114, 143, 148, 204],
        8: [5, 26, 50, 137, 210, 241, 258, 309]
    }

    # Ensure the number of players is supported
    if num_players not in spawn_points:
        raise ValueError("Unsupported number of players. Choose from 2, 4, 5, or 8.")

    # Set the spawn zones
    for index in spawn_points[num_players]:
        zones[index] = "spawn"

    return zones



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


def visualize_sphere_pygame(vertices, faces, zones=None):
    pygame.init()
    screen_width, screen_height = 1200, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption('Spherical Mesh Visualization')
    clock = pygame.time.Clock()
    colors = {'spawn': (255, 0, 0), 'normal': (0, 255, 255)}

    running = True
    angle_x, angle_y = 0, 0
    zoom = 300
    clicked_face = None

    def project_vertex(vertex, zoom, screen, offset_x=0):
        x = vertex[0] * zoom + screen.get_width() / 4 + offset_x
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
            projected_points = [project_vertex(vertices[j], zoom, screen) for j in face]
            if point_in_triangle(mouse_pos, *projected_points):
                return i
        return None

    def build_face_graph(faces):
        graph = defaultdict(list)
        face_edges = [{tuple(sorted([face[i], face[(i + 1) % 3]])) for i in range(3)} for face in faces]

        for i, edges1 in enumerate(face_edges):
            for j, edges2 in enumerate(face_edges):
                if i != j and len(edges1 & edges2) == 1:
                    graph[i].append(j)

        return graph

    def rotate_vertices(vertices, angle_x, angle_y):
        rotation_x = np.array([[1, 0, 0],
                               [0, np.cos(angle_x), -np.sin(angle_x)],
                               [0, np.sin(angle_x), np.cos(angle_x)]])
        rotation_y = np.array([[np.cos(angle_y), 0, np.sin(angle_y)],
                               [0, 1, 0],
                               [-np.sin(angle_y), 0, np.cos(angle_y)]])
        return np.dot(vertices, np.dot(rotation_x, rotation_y).T)

    face_graph = build_face_graph(faces)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    clicked_face = get_clicked_face(event.pos, rotated_vertices, faces)
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

        # Draw the 3D sphere visualization on the left side of the screen
        for i, face in enumerate(faces):
            if is_face_visible(face, rotated_vertices):
                points = [projected_vertices[j] for j in face]
                color = colors[zones[i]] if zones else (255, 255, 255)
                pygame.draw.polygon(screen, color, points, 0)
                pygame.draw.polygon(screen, (0, 0, 0), points, 1)
                if i == clicked_face:
                    pygame.draw.polygon(screen, (255, 255, 0), points,
                                        3)  # Highlight clicked triangle with yellow border

        # Draw the clicked face flat and not rotating on the right side of the screen
        if clicked_face is not None:
            face = faces[clicked_face]
            flat_points = [project_vertex(vertices[i], zoom, screen, screen_width // 2) for i in face]
            original_color = colors[zones[clicked_face]] if zones else (255, 255, 255)
            pygame.draw.polygon(screen, original_color, flat_points, 0)  # Use original color for clicked face
            pygame.draw.polygon(screen, (255, 255, 0), flat_points, 3)  # Highlight with yellow border

            neighbors = [n for n in face_graph[clicked_face]]
            for neighbor in neighbors:
                neighbor_points = [project_vertex(vertices[i], zoom, screen, screen_width // 2) for i in
                                   faces[neighbor]]
                neighbor_color = colors[zones[neighbor]] if zones else (255, 255, 255)
                pygame.draw.polygon(screen, neighbor_color, neighbor_points, 0)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
