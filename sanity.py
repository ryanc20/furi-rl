import gym
import gym_pddlworld
import os
from collections import defaultdict
import random

DOMAIN_MOD = ''
PROB = ''
DOM_TEMPL = ''
PROB_TEMPL = ''
PROP_LIST = ''

RL_DIR = os.environ.get('RL_DIR')

if False:
    DOMAIN_MOD = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/domain.pddl'
    PROB = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prob.pddl'
    DOM_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/domain_temp.pddl'
    PROB_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prob_templ.pddl'
    PROP_LIST = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prop_list'
    level_one = [
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_1/prob2.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_1/prob2.pddl'
    ]
    level_two = [
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_2/prob1.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_2/prob2.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_2/prob3.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_2/prob4.pddl'
    ]
    level_three = [
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob1.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob2.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob3.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob4.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob5.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob6.pddl',
    ]
    problem_list = [level_one, level_two, level_three]
else: 
    DOMAIN_MOD = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain.pddl'
    PROB = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob.pddl'
    DOM_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain_temp.pddl'
    PROB_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob_templ.pddl'
    PROP_LIST =  RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prop_list'
    level_one = [
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob1.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob2.pddl'
    ]
    problem_list = [level_one]

env = gym.make('lslite-v0')
env.setPDDL(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST, problem_list)
state = env.reset()

pre = int('010001010100',2)
eff = int('100100001001', 2)
state = (pre, eff)
env.testState(state)