from mcp_neuron.network import Net
from mcp_neuron.neuron import Neuron


def build_net():
    net = Net()
    # D fires only if A and B are both active, and C is not active.
    net.add_neuron(
        Neuron("D", threshold=2, excitatory_inputs=["A", "B"], inhibitory_inputs=["C"])
    )
    return net


def run():
    net = build_net()

    scenarios = {
        "A and B fire, C silent": {"A": [True], "B": [True], "C": [False]},
        "A and B fire, C also fires": {"A": [True], "B": [True], "C": [True]},
        "Only A fires": {"A": [True], "B": [False], "C": [False]},
    }

    for label in scenarios:
        external = scenarios[label]
        history = net.simulate(steps=1, external=external)
        print(label, "-> D fires:", history["D"][1])


if __name__ == "__main__":
    run()
