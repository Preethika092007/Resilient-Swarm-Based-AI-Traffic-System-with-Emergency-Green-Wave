import networkx as nx
import random

CITY_GRAPH = None
EDGE_TRAFFIC = {}
CITY_POSITIONS = None


def build_city_network():

    global CITY_GRAPH, EDGE_TRAFFIC, CITY_POSITIONS

    if CITY_GRAPH is not None:
        return CITY_GRAPH

    # create 4x4 city grid
    G = nx.grid_2d_graph(4, 4)

    # convert nodes from (x,y) to numbers
    G = nx.convert_node_labels_to_integers(G)

    for u, v in G.edges():

        traffic = random.randint(1, 10)

        G[u][v]["weight"] = traffic

        EDGE_TRAFFIC[(u, v)] = traffic
        EDGE_TRAFFIC[(v, u)] = traffic

    CITY_GRAPH = G

    # fixed layout so graph always looks same
    CITY_POSITIONS = nx.spring_layout(G, seed=42)

    return CITY_GRAPH


def get_city_positions():

    global CITY_POSITIONS

    return CITY_POSITIONS