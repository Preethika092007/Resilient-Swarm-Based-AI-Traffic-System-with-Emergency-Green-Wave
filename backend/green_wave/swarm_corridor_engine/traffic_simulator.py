import random

def simulate_traffic(G):

    traffic = {}

    for node in G.nodes:

        vehicles = random.randint(0,20)

        traffic[node] = vehicles

    return traffic