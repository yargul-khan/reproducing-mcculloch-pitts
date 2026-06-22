"""
mcp_neuron.examples.heat_cold
===============================

Reproduces the transient-cold/warmth illusion worked example from
McCulloch & Pitts (1943), Section II "Theory: Nets Without Circles"
(p.121-122) - the paper's own demonstration of Theorem III.

The paper's formulas (p.122), where N1/N2 are the heat/cold receptors
and N3/N4 are the heat/cold sensation neurons:

    N3(t) = N1(t-1) v [N2(t-3) . ~N2(t-2)]      (heat sensation)
    N4(t) = N2(t-2) . N2(t-1)                    (cold sensation)

Rather than just evaluating these formulas directly, this module builds
the actual circuit out of single-synaptic-delay neurons - one delay
neuron (d1) and two threshold units (rebound, and the two sensation
neurons) - mirroring how the paper itself builds nets out of delay
chains and threshold gates (its Figure 1).

Run directly with:
    python -m mcp_neuron.examples.heat_cold
"""
from mcp_neuron.network import Net
from mcp_neuron.neuron import Neuron


def build_heat_cold_net() -> Net:
    """Construct the heat/cold circuit.

    Wiring:
        d1       : one-step delay of the cold receptor N2.
        rebound  : fires when cold was active two steps ago but not one
                   step ago (the "just removed" transient).
        N3_heat  : fires from direct heat input OR the cold-removal
                   rebound.
        N4_cold  : fires only when cold has been active for two
                   consecutive steps (sustained contact).
    """
    net = Net()
    net.add_neuron(Neuron("d1", threshold=1, excitatory_inputs=("N2",)))
    net.add_neuron(
        Neuron("rebound", threshold=1, excitatory_inputs=("d1",), inhibitory_inputs=("N2",))
    )
    net.add_neuron(
        Neuron("N3_heat", threshold=1, excitatory_inputs=("N1", "rebound"))
    )
    net.add_neuron(
        Neuron("N4_cold", threshold=2, excitatory_inputs=("d1", "N2"))
    )
    return net


def run_scenario(label: str, n1_seq, n2_seq, steps: int) -> None:
    net = build_heat_cold_net()
    history = net.simulate(steps=steps, external={"N1": n1_seq, "N2": n2_seq})

    print(f"\n{label}")
    print(f"{'t':<3}{'cold receptor':<16}{'heat sensation':<16}{'cold sensation':<16}")
    for t in range(steps + 1):
        n2 = n2_seq[t] if t < len(n2_seq) else False
        print(
            f"{t:<3}{str(n2):<16}{str(history['N3_heat'][t]):<16}{str(history['N4_cold'][t]):<16}"
        )


if __name__ == "__main__":
    steps = 8

    # Brief touch: cold receptor fires for two steps, then is removed.
    quick_n1 = [False] * (steps + 1)
    quick_n2 = [False, True, True, False, False, False, False, False, False]
    run_scenario("Quick cold touch (brief contact, then removed)", quick_n1, quick_n2, steps)

    # Sustained touch: cold receptor stays active throughout.
    long_n1 = [False] * (steps + 1)
    long_n2 = [False, True, True, True, True, True, True, True, True]
    run_scenario("Long cold touch (sustained contact)", long_n1, long_n2, steps)
