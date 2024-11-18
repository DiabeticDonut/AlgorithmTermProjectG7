import osmnx as ox
from path_algorithms import PathFinder
import pandas as pd
import matplotlib.pyplot as plt

# Get the street network
place = "Statesboro, Georgia, USA"
G = ox.graph_from_place(place, network_type="drive")

# Create test cases with different origin-destination pairs


# Savannah, Georgia test cases
savannah_cases = [
    ((32.0809, -81.0912), (32.0835, -81.0998)),  # Forsyth Park to River Street
    ((32.0722, -81.0951), (32.0747, -81.1324)),  # Oglethorpe Mall to Hunter Army Airfield
    ((32.0835, -81.0998), (32.0199, -81.1448)),  # River Street to Savannah Mall
]

# Statesboro, Georgia test cases
statesboro_cases = [
    ((32.4488, -81.7832), (32.4158, -81.7837)),  # Georgia Southern to The Plaza
    ((32.4488, -81.7832), (32.4580, -81.7835)),  # Georgia Southern to Downtown
    ((32.4158, -81.7837), (32.4279, -81.7592)),  # The Plaza to Mill Creek Park
]

test_cases = statesboro_cases



# Initialize PathFinder
path_finder = PathFinder(G)

# Compare algorithms and store results
results = []
for orig_coords, dest_coords in test_cases:
    #convert coordinates to nearest network nodes
    orig = ox.nearest_nodes(G, orig_coords[1], orig_coords[0])
    dest = ox.nearest_nodes(G, dest_coords[1], dest_coords[0])
    # Run each algorithm
    dijkstra_path, dijkstra_time = path_finder.dijkstra_path(orig, dest)
    astar_path, astar_time = path_finder.astar_path(orig, dest)
    bellman_path, bellman_time = path_finder.bellman_ford_path(orig, dest)
    
    # Store results
    results.append({
        'Route': f'Route {len(results)+1}',
        'Dijkstra Time': dijkstra_time,
        'A* Time': astar_time,
        'Bellman-Ford Time': bellman_time,
        'Dijkstra Length': len(dijkstra_path),
        'A* Length': len(astar_path),
        'Bellman-Ford Length': len(bellman_path)
    })

# Convert results to DataFrame
results_df = pd.DataFrame(results)
print("\nAlgorithm Performance Results:")
print(results_df)

# Plot paths for each algorithm
algorithms = {
    'Dijkstra': dijkstra_path,
    'A*': astar_path,
    'Bellman-Ford': bellman_path
}

colors = {'Dijkstra': 'r', 'A*': 'b', 'Bellman-Ford': 'g'}
  # Plot each path
for algo_name, path in algorithms.items():
    fig, ax = ox.plot_graph_route(G, path, 
                                route_color=colors[algo_name],
                                route_linewidth=6, 
                                node_size=0)
    # plt.title(f'{algo_name} Path')
    # plt.show()
# Plot performance comparison with improved visualization
plt.figure(figsize=(12, 6))
time_columns = ['Dijkstra Time', 'A* Time', 'Bellman-Ford Time']
results_df[time_columns].plot(kind='bar', width=0.8)
plt.title('Algorithm Performance Comparison')
plt.xlabel('Test Routes')
plt.ylabel('Computation Time (seconds)')
plt.legend(title='Algorithm')
plt.grid(True, axis='y')
plt.xticks(range(len(results_df)), results_df['Route'], rotation=45)
plt.tight_layout()
plt.show()
