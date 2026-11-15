# Mapping the article to the repository

This note connects the accompanying Substack article to the material present in this code repository. It distinguishes explanatory figures from executable code.

| Article topic / figure | Repository material | What the code currently demonstrates |
|---|---|---|
| Binary threshold neuron | `src/mcp_neuron/neuron.py` | Excitatory input counting, threshold activation, and inhibitory blocking |
| NOT, OR, AND logic | `src/mcp_neuron/gates.py` and `tests/test_gates.py` | Constructors for OR, AND, and AND-NOT; NOT is shown in the supplied explanatory figure |
| Elementary circuit arrangements | `src/mcp_neuron/network.py` | Neurons connected through named inputs and evaluated in discrete time steps |
| Delay chain | `Net.add_delay_chain` | A pass-through chain in which activity propagates across successive steps |
| Heat/cold example | `src/mcp_neuron/examples/heat_cold.py` | A simplified network with delayed cold activity, rebound, and heat/cold output signals |

## Figure assets

The `docs/figures/` directory contains the four diagrams supplied for the article:

1. `figure-01-mcculloch-pitts-neuron.png` — input, summation, threshold, and output.
2. `figure-02-delay-and-logic-circuits.png` — delay and AND-NOT/AND/OR circuit arrangements.
3. `figure-03-logic-gates.png` — NOT, OR, and AND truth-table illustrations.
4. `figure-04-heat-cold-example.png` — the heat/cold receptor logic flow.

These images are article illustrations. They are not automatically generated from, or verified against, the Python implementation. The code examples and tests should be treated as the executable source of truth for the behaviour implemented here.

## Scope and interpretation

The repository is a compact, modern implementation of selected ideas rather than a formal reconstruction of the complete 1943 paper. In particular, the heat/cold program is a schematic demonstration of discrete-time logic. It is not a biological simulation, and it does not establish that the original authors' full physiological account is reproduced.
