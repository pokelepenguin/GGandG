import spherey

# Number of players (choose from 2, 4, 5, 8)
num_players = 4

# Create the spherical mesh with 2 subdivisions
vertices, faces = spherey.create_spherical_mesh(subdivisions=2)

# Assign zones
zones = spherey.assign_zones(faces, num_players)

# Calculate and print distances between spawn points
distances = spherey.calculate_total_distances(faces, zones)
for index, total_distance in distances:
    print(f"Total distance for spawn point at face {index}: {total_distance}")




# Visualize the spherical mesh with zones and interactive rotation using Pygame
spherey.visualize_sphere_pygame(vertices, faces, zones)

