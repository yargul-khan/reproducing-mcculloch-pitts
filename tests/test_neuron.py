from mcp_neuron.neuron import Neuron


def test_excitatory_threshold():
    # A neuron needing 2 active inputs should only fire when both are on.
    n = Neuron("n", threshold=2, excitatory_inputs=["a", "b"])
    assert n.fires({"a", "b"}) == True
    assert n.fires({"a"}) == False
    assert n.fires(set()) == False


def test_inhibition_is_absolute():
    # An active inhibitory input should block firing, even if the
    # excitatory input is also active.
    n = Neuron("n", threshold=1, excitatory_inputs=["a"], inhibitory_inputs=["b"])
    assert n.fires({"a"}) == True
    assert n.fires({"a", "b"}) == False
