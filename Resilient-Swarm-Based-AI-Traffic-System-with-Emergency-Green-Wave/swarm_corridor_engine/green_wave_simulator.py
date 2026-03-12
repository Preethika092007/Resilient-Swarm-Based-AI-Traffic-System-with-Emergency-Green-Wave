import time

def run_green_wave(route):

    print("\n🚑 EMERGENCY GREEN CORRIDOR ACTIVATED\n")

    active_signals = []

    for i, node in enumerate(route):

        active_signals.append(node)

        print(f"Signal {node} → GREEN")

        if i > 0:
            prev = route[i-1]
            print(f"Signal {prev} → AMBULANCE PASSED")

        time.sleep(0.8)