import random

def simulate_traffic_conditions(G):
    # Add random traffic weights to edges
    for u, v, k, data in G.edges(keys=True, data=True):
        # Simulate traffic congestion (1.0 = no traffic, 3.0 = heavy traffic)
        traffic_factor = round(random.uniform(1.0, 3.0), 1)
        G[u][v][k]['traffic_weight'] = data['length'] * traffic_factor
        G[u][v][k]['traffic_factor'] = traffic_factor
    return G
