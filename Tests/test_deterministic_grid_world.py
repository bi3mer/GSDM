from GDM.ActiveRL import DUE
from GDM import PassiveRL
from GDM.Graph import Graph
from GDM.utility import *

from random import seed


def __build_grid_world(MAX_X, MAX_Y):
    g = Graph() 

    # create nodes
    for y in range(MAX_Y):
        for x in range(MAX_X):
            # ignore the blank position
            if y == 1 and x == 1:
                continue

            # create node and its reward
            src = f'{y}_{x}'
            if x == MAX_X - 1 and y == MAX_Y - 1:
                g.add_default_node(src, terminal=True)
            elif x == MAX_X - 1 and y == MAX_Y - 2:
                g.add_default_node(src, reward=-1, terminal=True)
            else:
                g.add_default_node(src, reward=-0.05)

    # create edges
    for src in g.nodes:
        # get name
        y, x = [int(i) for i in src.split('_')]

        # create left connection
        if x - 1 >= 0 and not (x - 1 == 1 and y == 1):
            tgt = f'{y}_{x-1}'
            g.add_default_edge(src, tgt, {tgt: 1.0})

        # create right connection
        if x + 1 < MAX_X and not (x + 1 == 1 and y == 1):
            tgt = f'{y}_{x+1}'
            g.add_default_edge(src, tgt, {tgt: 1.0})

        # create up connection
        if y - 1 >= 0 and not (x == 1 and y - 1 == 1):
            tgt = f'{y-1}_{x}'
            g.add_default_edge(src, tgt, {tgt: 1.0})

        # create down connection
        if y + 1 < MAX_Y and not (x == 1 and y + 1 == 1):
            tgt = f'{y+1}_{x}'
            g.add_default_edge(src, tgt, {tgt: 1.0})

    return '0_0', g

def test_policy_iteration():
    start, G = __build_grid_world(5, 5)
    pi = PassiveRL.policy_iteration(G, 0.6)
    assert pi != None
    states, rewards = run_policy(G, start, pi, 20)
    assert len(states) == 9
    assert len(rewards) == 9
    assert rewards[-1] == 1
    assert states[-1] == '4_4'

def test_in_place_policy_iteration():
    start, G = __build_grid_world(20, 20)
    pi = PassiveRL.policy_iteration(G, 0.5, in_place=True)
    assert pi != None
    states, rewards = run_policy(G, start, pi,100)
    assert len(states) == 39
    assert len(rewards) == 39
    assert rewards[-1] == 1
    assert states[-1] == '19_19'

def test_modified_policy_iteration():
    start, G = __build_grid_world(30, 30)
    pi = PassiveRL.policy_iteration(G, 0.7, modified=True)
    assert pi != None
    states, rewards = run_policy(G, start, pi, 100)
    assert len(states) == 59
    assert len(rewards) == 59
    assert rewards[-1] == 1
    assert states[-1] == '29_29'

def test_modified_in_place_policy_iteration():
    start, G = __build_grid_world(50, 50)
    pi = PassiveRL.policy_iteration(G, 0.9, modified=True, in_place=True)
    assert pi != None
    states, rewards = run_policy(G, start, pi, 100)
    assert len(states) == 99
    assert len(rewards) == 99
    assert rewards[-1] == 1
    assert states[-1] == '49_49'

def test_value_iteration():
    start, G = __build_grid_world(5, 10)
    pi = PassiveRL.value_iteration(G, 100, 0.8, 1e-13, in_place=False)
    assert pi != None
    states, rewards = run_policy(G, start, pi, 100)
    assert len(states) == 14
    assert len(rewards) == 14
    assert rewards[-1] == 1
    assert states[-1] == '9_4'

def test_in_place_value_iteration():
    start, G = __build_grid_world(8, 10)
    pi = PassiveRL.value_iteration(G, 100, 0.8, 1e-13, in_place=True)
    assert pi != None
    states, rewards = run_policy(G, start, pi, 100)
    assert len(states) == 17
    assert len(rewards) == 17
    assert rewards[-1] == 1
    assert states[-1] == '9_7'

def test_direct_utility_estimation():
    MAX_STEPS = 50
    GAMMA = 0.9
    EPSILON = 0.2 
    seed(0)

    start, G = __build_grid_world(5, 4)
    pi = create_policy_from_utility(G)
    for _ in range(200):
        states, rewards = run_epsilon_greedy_utility_policy(G, start, pi, EPSILON, MAX_STEPS)
        pi = DUE.direct_utility_estimation(G, GAMMA, states, rewards)

    states, rewards = run_policy(G, start, pi, MAX_STEPS)
    
    assert rewards[-1] == 1
    assert len(states) == 8
    assert len(states) == len(rewards)
    assert states[-1] == '3_4'