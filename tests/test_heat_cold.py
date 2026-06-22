from mcp_neuron.examples.heat_cold import build_heat_cold_net


def test_quick_touch_causes_rebound_warmth():
    # Cold receptor on for 2 steps (t=1,2), then off.
    heat_input = [False] * 9
    cold_input = [False, True, True, False, False, False, False, False, False]

    net = build_heat_cold_net()
    history = net.simulate(steps=8, external={"N1": heat_input, "N2": cold_input})

    # No heat sensation while cold is happening or right after.
    assert history["N3_heat"][1] == False
    assert history["N3_heat"][2] == False
    assert history["N3_heat"][3] == False

    # A brief warmth rebound appears a couple of steps after cold is removed.
    assert history["N3_heat"][5] == True


def test_sustained_touch_causes_no_rebound():
    # Cold receptor stays on the whole time - no "removal" event.
    heat_input = [False] * 9
    cold_input = [False, True, True, True, True, True, True, True, True]

    net = build_heat_cold_net()
    history = net.simulate(steps=8, external={"N1": heat_input, "N2": cold_input})

    # Heat sensation should never fire during a sustained touch.
    for value in history["N3_heat"]:
        assert value == False

    # Cold sensation should be on by the end (sustained contact).
    assert history["N4_cold"][8] == True
