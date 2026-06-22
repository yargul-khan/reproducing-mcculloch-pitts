"""
mcp_neuron.examples.order0_logic
=================================

Worked example: an order-0 (feedforward) net where a downstream neuron D
fires only when A and B fire but C does not -

    D(t) = A(t-1) AND B(t-1) AND NOT C(t-1)

This is the "D fires if A and B fire, but C doesn't" example from the
companion article, and demonstrates Theorem II: any Boolean expression
over a net's peripheral afferents can be realized by a net of order zero
(no circles).

Run directly with:
    python -m mcp_neuron.examples.order0_logic
"""
from mcp_neuron.network import Net
from mcp_neuron.neuron import Neuron


def build_net() -> Net:
    net = Net()
    # D requires both A and B (threshold=2) and is vetoed by any C activity.
    net.add_neuron(
        Neuron("D", threshold=2, excitatory_inputs=("A", "B"), inhibitory_inputs=("C",))
    )
    return net


def run() -> None:
    net = build_net()
    scenarios = {
        "A and B fire, C silent": {"A": [True], "B": [True], "C": [False]},
        "A and B fire, C also fires": {"A": [True], "B": [True], "C": [True]},
        "Only A fires": {"A": [True], "B": [False], "C": [False]},
    }
    for label, external in scenarios.items():
        history = net.simulate(steps=1, external=external)
        print(f"{label:<30} -> D fires: {history['D'][1]}")


if __name__ == "__main__":
    run()
