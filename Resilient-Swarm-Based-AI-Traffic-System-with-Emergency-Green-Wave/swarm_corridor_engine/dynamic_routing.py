import networkx as nx
import random
from swarm_corridor_engine.city_map import build_city_network


def heuristic(a,b):
    return abs(a-b)


def compute_fastest_route(start,destination):

    G = build_city_network()

    # simulate traffic weights
    for u,v in G.edges():

        traffic_load = random.randint(1,10)

        G[u][v]['weight'] = traffic_load

    print("\nTraffic Conditions:")
    for u,v,data in G.edges(data=True):
        print(f"{u}->{v} congestion: {data['weight']}")

    route = nx.astar_path(
        G,
        start,
        destination,
        heuristic=heuristic,
        weight="weight"
    )

    return route