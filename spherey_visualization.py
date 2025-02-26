import numpy as np
import pygame
from pygame.locals import *
from collections import deque, defaultdict
from zone_stats import calculate_color
import game_menu
import spherey_core as core

def display_current_filter(screen, current_filter):
    filter_names = {
        'none': 'None',
        'goop': 'Goop Saturation',
        'gold': 'Gold per Year',
        'defense': 'Defense',
        'ownership': 'Ownership',
    }
    font = pygame.font.SysFont('Arial', 18)
    filter_text =  f"Current Filter: {filter_names.get(current_filter, 'Unknown')}"
    text_surface = font.render(filter_text, True, (255, 255, 255))
    x = screen.get_width() - 400
    y = 20
    pygame.draw.rect(screen, (50, 50, 50), (x - 10, y - 10, 300, 40))
    screen.blit(text_surface, (x, y))

def display_zone_stats(screen, zone):
    font = pygame.font.SysFont('Arial', 16)
    owner_text = f"Owner: Player {zone.owner}" if zone.owner is not None else "Owner: None"
    stats_text = [
        f"Zone Index: {zone.index}",
        f"Type: {zone.zone_type}",
        owner_text,
        f"Goop Saturation: {zone.goop_sv:.2f}",
        f"Gold per Year: {zone.gold_py:.2f}",
        f"Defense: {zone.defense:.2f}"
    ]

    x, y = 20, 20
    pygame.draw.rect(screen, (50, 50, 50), (x - 10, y - 10, 250, 150))

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

def get_clicked_face(mouse_pos, vertices, faces, zoom, screen):
    for i, face in enumerate(faces):
        if is_face_visible(face, vertices):
            projected_points = [project_vertex(vertices[j], zoom, screen) for j in face]
            if point_in_triangle(mouse_pos, *projected_points):
                return i
    return None

def visualize_sphere_pygame(vertices, faces, zones, screen, current_player):
    clock = pygame.time.Clock()
    running = True
    angle_x, angle_y = 0, 0
    zoom = 300
    clicked_face = None
    selected_zone = None
    current_filter = 'none'

    min_values = {
        'goop': min(zone.goop_sv for zone in zones),
        'gold': min(zone.gold_py for zone in zones),
        'defense': min(zone.defense for zone in zones if zone.zone_type != 'spawn')
    }
    max_values = {
        'goop': max(zone.goop_sv for zone in zones),
        'gold': max(zone.gold_py for zone in zones),
        'defense': max(zone.defense for zone in zones if zone.zone_type != 'spawn')
    }

    face_graph = core.build_face_graph(faces)

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_face = get_clicked_face(event.pos, rotated_vertices, faces, zoom, screen)
                    if clicked_face is not None:
                        selected_zone = zones[clicked_face]
            elif event.type == KEYDOWN:
                if event.key == K_LEFT:
                    angle_y -= 0.1
                elif event.key == K_RIGHT:
                    angle_y += 0.1
                elif event.key == K_UP:
                    angle_x -= 0.1
                elif event.key == K_DOWN:
                    angle_x += 0.1
                elif event.unicode == '1':
                    current_filter = 'none'
                    print("Filter set to: None")
                elif event.unicode == '2':
                    current_filter = 'goop'
                    print("Filter set to: Goop Saturation")
                elif event.unicode == '3':
                    current_filter = 'gold'
                    print("Filter set to: Gold per Year")
                elif event.unicode == '4':
                    current_filter = 'defense'
                    print("Filter set to: Defense")
                elif event.unicode == '5':
                    current_filter = 'ownership'
                    print("Filter set to: Ownership (Displaying player numbers)")
                elif event.unicode == 'm':
                    game_menu.main_game_menu(screen, current_player, vertices, faces, zones)

        screen.fill((0, 0, 0))

        rotated_vertices = core.rotate_vertices(vertices, angle_x, angle_y)
        projected_vertices = [project_vertex(v, zoom, screen) for v in rotated_vertices]

        projected_faces = []
        for i, face in enumerate(faces):
            if is_face_visible(face, rotated_vertices):
                points = [projected_vertices[j] for j in face]
                projected_faces.append(points)
                zone = zones[i]
                color = calculate_color(zone, min_values, max_values, current_filter)
                pygame.draw.polygon(screen, color, points)
                pygame.draw.polygon(screen, (0, 0, 0), points, 1)

                if current_filter == 'ownership':
                    if zone.owner is not None:
                        centroid = core.calculate_centroid(points)
                        font = pygame.font.SysFont('Arial', 14, bold=True)
                        player_number = str(zone.owner.company_id)
                        text_surface = font.render(player_number, True, (0, 0, 0))
                        text_rect = text_surface.get_rect(center=centroid)
                        screen.blit(text_surface, text_rect)

                if i == clicked_face:
                    pygame.draw.polygon(screen, (255, 255, 0), points, 3)
            else:
                projected_faces.append(None)

        if clicked_face is not None:
            center_x = 2 * screen.get_width() / 3
            center_y = screen.get_height() / 2

            size = 300
            selected_face = faces[clicked_face]
            selected_vertices_indices = selected_face
            selected_vertices = [vertices[idx] for idx in selected_vertices_indices]

            tri_2d, x_axis, y_axis, v0, normal_sel = core.flatten_triangle(selected_vertices, angle_x, angle_y)

            tri_2d = [p * size for p in tri_2d]
            tri_center = sum(tri_2d) / 3
            tri_2d = [p - tri_center + np.array([center_x, center_y]) for p in tri_2d]

            zone = zones[clicked_face]
            color = calculate_color(zone, min_values, max_values, current_filter)
            pygame.draw.polygon(screen, color, tri_2d)
            pygame.draw.polygon(screen, (0, 0, 0), tri_2d, 1)

            index_to_pos = {selected_vertices_indices[i]: tri_2d[i] for i in range(3)}

            neighbors = face_graph[clicked_face]

            for neighbor_idx in neighbors:
                neighbor_face = faces[neighbor_idx]
                neighbor_vertices_indices = neighbor_face
                neighbor_vertices = [rotated_vertices[idx] for idx in neighbor_vertices_indices]
                neighbor_tri_2d = []

                for vertex in neighbor_vertices:
                    vec = vertex - v0
                    x = np.dot(vec, x_axis)
                    y = np.dot(vec, y_axis)
                    neighbor_tri_2d.append(np.array([x, y]) * size)

                neighbor_tri_2d = [p - tri_center + np.array([center_x, center_y]) for p in neighbor_tri_2d]

                neighbor_zone = zones[neighbor_idx]
                color = calculate_color(neighbor_zone, min_values, max_values, current_filter)
                pygame.draw.polygon(screen, color, neighbor_tri_2d)
                pygame.draw.polygon(screen, (0, 0, 0), neighbor_tri_2d, 1)

            display_zone_stats(screen, selected_zone)
            display_current_filter(screen, current_filter)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()