import matplotlib.pyplot as plt
import pandas as pd
import osmnx as ox

def plot_performance_comparison(results_df):
    algorithms = ['Dijkstra Time', 'A* Time', 'Bellman-Ford Time']
    
    plt.figure(figsize=(12, 6))
    results_df[algorithms].plot(kind='bar')
    plt.title('Algorithm Performance Comparison')
    plt.xlabel('Test Case')
    plt.ylabel('Computation Time (seconds)')
    plt.legend(title='Algorithm')
    plt.tight_layout()
    plt.show()

def visualize_paths(G, paths_dict):
    for algo_name, path in paths_dict.items():
        fig, ax = ox.plot_graph_route(G, path, 
                                    route_color='r' if algo_name == 'Dijkstra' else 'b' if algo_name == 'A*' else 'g',
                                    route_linewidth=6, 
                                    node_size=0,
                                    title=f'{algo_name} Path')
