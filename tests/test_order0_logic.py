from mcp_neuron.examples.order0_logic import build_net


def test_d_fires_when_a_and_b_and_not_c():
    net = build_net()
    history = net.simulate(steps=1, external={"A": [True], "B": [True], "C": [False]})
    assert history["D"][1] == True


def test_d_blocked_when_c_fires():
    net = build_net()
    history = net.simulate(steps=1, external={"A": [True], "B": [True], "C": [True]})
    assert history["D"][1] == False


def test_d_needs_both_a_and_b():
    net = build_net()
    history = net.simulate(steps=1, external={"A": [True], "B": [False], "C": [False]})
    assert history["D"][1] == False
