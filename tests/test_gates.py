from mcp_neuron.network import Net
from mcp_neuron.gates import make_and, make_or, make_and_not


def run_gate(builder, a, b):
    net = Net()
    builder(net, "out", "A", "B")
    history = net.simulate(steps=1, external={"A": [a], "B": [b]})
    return history["out"][1]


def test_and_gate():
    assert run_gate(make_and, True, True) == True
    assert run_gate(make_and, True, False) == False
    assert run_gate(make_and, False, False) == False


def test_or_gate():
    assert run_gate(make_or, True, False) == True
    assert run_gate(make_or, False, True) == True
    assert run_gate(make_or, False, False) == False


def test_and_not_gate():
    assert run_gate(make_and_not, True, False) == True
    assert run_gate(make_and_not, True, True) == False
    assert run_gate(make_and_not, False, False) == False
