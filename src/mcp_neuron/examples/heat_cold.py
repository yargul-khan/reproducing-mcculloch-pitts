from mcp_neuron.network import Net
from mcp_neuron.neuron import Neuron


def build_heat_cold_net():
    """
    Builds the heat/cold circuit from the 1943 paper (p.122).
    """
    net = Net()

    # Step 1: repeat the cold signal (N2), but one time step later.
    net.add_neuron(Neuron("d1", threshold=1, excitatory_inputs=["N2"]))

    # Step 2: "rebound" fires when cold WAS active a moment before (d1),
    # but is NOT active right now (N2 is the inhibitor here).
    net.add_neuron(
        Neuron("rebound", threshold=1, excitatory_inputs=["d1"], inhibitory_inputs=["N2"])
    )

    # Step 3: heat sensation fires from real heat (N1), OR from rebound.
    net.add_neuron(Neuron("N3_heat", threshold=1, excitatory_inputs=["N1", "rebound"]))

    # Step 4: cold sensation only fires if cold has been on for 2 steps
    # in a row (needs both d1 AND N2 active, threshold=2).
    net.add_neuron(Neuron("N4_cold", threshold=2, excitatory_inputs=["d1", "N2"]))

    return net


def run_scenario(label, heat_input, cold_input, steps):
    net = build_heat_cold_net()
    history = net.simulate(steps=steps, external={"N1": heat_input, "N2": cold_input})

    print()
    print(label)
    print("t | cold receptor | heat sensation | cold sensation")
    for t in range(steps + 1):
        cold_now = cold_input[t] if t < len(cold_input) else False
        print(t, "|", cold_now, "|", history["N3_heat"][t], "|", history["N4_cold"][t])


if __name__ == "__main__":
    steps = 8

    # Quick touch: cold receptor on for 2 steps, then off.
    quick_heat = [False] * (steps + 1)
    quick_cold = [False, True, True, False, False, False, False, False, False]
    run_scenario("Quick cold touch (brief contact, then removed)", quick_heat, quick_cold, steps)

    # Long touch: cold receptor stays on the whole time.
    long_heat = [False] * (steps + 1)
    long_cold = [False, True, True, True, True, True, True, True, True]
    run_scenario("Long cold touch (sustained contact)", long_heat, long_cold, steps)
