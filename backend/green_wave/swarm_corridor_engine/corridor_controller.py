from swarm_corridor_engine.dynamic_routing import compute_fastest_route
from swarm_corridor_engine.green_wave_simulator import run_green_wave

def activate_emergency_corridor(start,destination):

    route = compute_fastest_route(start,destination)

    print("Optimal Emergency Route:",route)

    run_green_wave(route)