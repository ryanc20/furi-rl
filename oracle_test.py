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

if True:
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
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob2.pddl',
        RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob3.pddl'
    ]
    problem_list = [level_one]

env = gym.make('lslite-v0')
env.setPDDL(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST, problem_list)

for episode in range(100):
    state = env.reset()
    num_acts = 0
    done = False
    while not done and num_acts <= 200:
        next_state, reward, done, info = env._step('ORACLE')
        state = next_state
        print("Reward: {}\tCounter: {}\t\tOracleCalls: {}".format(reward, cutoff_counter, num_oracle_calls))
    print("END OF EPISODE {}: value of done = {}".format(episode, done))
