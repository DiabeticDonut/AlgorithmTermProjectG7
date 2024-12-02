import osmnx as ox
from path_algorithms import PathFinder
import pandas as pd
import matplotlib.pyplot as plt
from traffic_simulation import simulate_traffic_conditions
import folium

# Get the street network
place = "Savannah, Georgia, USA"
G = ox.graph_from_place(place, network_type="drive")
G = simulate_traffic_conditions(G)



# Savannah, Georgia test cases
savannah_cases = [
    ((32.03292259158145, -81.10128627312753), (32.09122999567041, -81.09923303303097)),  # Memorial Health University Medical Center to Talmadge Memorial Bridge
    ((32.004189, -81.115379), (32.028182, -81.120673)),  # Oglethorpe Mall to Hunter Army Airfield
    ((31.978861, -81.162827), (32.082062, -81.036018)) # Georgia Southern Armstrong to Old Fort Jackson
]



test_cases = savannah_cases



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

    #Calculating traffic weights for each path
    dijkstra_traffic = sum(G[dijkstra_path[i]][dijkstra_path[i+1]][0]['traffic_weight'] 
                          for i in range(len(dijkstra_path)-1))
    astar_traffic = sum(G[astar_path[i]][astar_path[i+1]][0]['traffic_weight'] 
                       for i in range(len(astar_path)-1))
    bellman_traffic = sum(G[bellman_path[i]][bellman_path[i+1]][0]['traffic_weight'] 
                         for i in range(len(bellman_path)-1))
    
    # Store results
    results.append({
        'Route': f'Route {len(results)+1}',
        'Dijkstra Time': dijkstra_time,
        'A* Time': astar_time,
        'Bellman-Ford Time': bellman_time,
        'Dijkstra Length': len(dijkstra_path),
        'A* Length': len(astar_path),
        'Bellman-Ford Length': len(bellman_path),
        'Dijkstra Traffic': dijkstra_traffic,
        'A* Traffic': astar_traffic,
        'Bellman-Ford Traffic': bellman_traffic
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


# # No need to run this part of the code as maps are generated in .html files

 

# D = ox.plot_route_folium(G, dijkstra_path, color='red', weight=4, opacity=0.8,)



# # Add A* route in a different color
# A = ox.plot_route_folium(G, astar_path, color='blue', weight=4, opacity=0.8, map=D)

# # Add Bellman-Ford route in a different color
# B = ox.plot_route_folium(G, bellman_path, color='green', weight=4, opacity=0.8, map=D)

# # Add a legend to distinguish the routes
# legend_html = '''
# <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; background-color: white; padding: 10px; border: 2px solid grey;">
# <p><span style="color: red;">■</span> Dijkstra</p>
# <p><span style="color: blue;">■</span> A*</p>
# <p><span style="color: green;">■</span> Bellman-Ford</p>
# </div>
# '''


# D.get_root().html.add_child(folium.Element(legend_html))
# A.get_root().html.add_child(folium.Element(legend_html))
# B.get_root().html.add_child(folium.Element(legend_html))

# # Save the maps to HTML files
# D.save('dijkstra_path_route3.html')
# A.save('astar_path_route3.html')
# B.save('bellman_path_route3.html')


