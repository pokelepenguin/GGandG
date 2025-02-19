import spherey
import zone_stats

# Number of players (choose from 2, 4, 5, 8)
num_players = 2

# Create the spherical mesh with 2 subdivisions
vertices, faces = spherey.create_spherical_mesh(subdivisions=2)

# Assign zones
zones = zone_stats.assign_zones(faces, num_players)

# Generate stats for each zone
zones = zone_stats.generate_zone_stats(zones)

# Optionally calculate and print distances between spawn points
distances = spherey.calculate_total_distances(faces, zones)
for index, total_distance in distances:
    print(f"Total distance for spawn point at face {index}: {total_distance}")

# Visualize the spherical mesh with zones and interactive rotation using Pygame
spherey.visualize_sphere_pygame(vertices, faces, zones)



