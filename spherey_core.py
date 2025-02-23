import numpy as np
from collections import defaultdict, deque

def normalize(v):
    return v / np.linalg.norm(v)

def calculate_centroid(points):
    x_coords = [p[0] for p in points]
    y_coords = [p[1] for p in points]
    length = len(points)
    centroid_x = sum(x_coords) / length
    centroid_y = sum(y_coords) / length
    return (centroid_x, centroid_y)

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
