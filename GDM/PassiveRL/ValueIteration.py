from typing import Dict

from ..utility import reset_utility, create_policy_from_utility
from ..Graph import Graph

def __in_place_value_iteration(G: Graph, max_iteration: int, gamma: float, theta: float):
    for _ in range(max_iteration):
        delta = 0

        for n in G.nodes:
            r = G.nodes[n].reward
            u = max(sum([p_val*G.nodes[n_true].utility for n_true, p_val in G.edges[(n, n_p)].probability.items()]) for n_p in G.neighbors(n))
            u = r + gamma*u
            delta = max(delta, abs(G.nodes[n].utility - u))
            
            G.nodes[n].utility = u

        if delta < theta:
            break

def __value_iteration(G: Graph, max_iteration: int, gamma: float, theta: float):
    for _ in range(max_iteration):
        delta = 0
        u_temp: Dict[str, float] = {}

        for n in G.nodes:
            r = G.nodes[n].reward
            u = max(sum([p_val*G.nodes[n_true].utility for n_true, p_val in G.edges[(n, n_p)].probability.items()]) for n_p in G.neighbors(n))
            u = r + gamma*u
            delta = max(delta, abs(G.nodes[n].utility - u))

            u_temp[n] = u

        G.set_node_utilities(u_temp)

        if delta < theta:
            break

def value_iteration(G: Graph, max_iteration: int, gamma: float, theta: float, in_place: bool=False, should_reset_utility: bool=True):
    if should_reset_utility:
        reset_utility(G)

    if in_place:
        __in_place_value_iteration(G, max_iteration, gamma, theta)
    else:
        __value_iteration(G, max_iteration, gamma, theta)

    return create_policy_from_utility(G)

