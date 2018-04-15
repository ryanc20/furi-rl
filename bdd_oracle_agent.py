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

problem_set = 3
if problem_set == 0:
    print("2 Props 2 Acts")
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
elif problem_set == 1:
    print("4 Props 4 Acts")
    DOMAIN_MOD = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/lightswitch_medium/domain.pddl'
    PROB = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/lightswitch_medium/prob.pddl'
    DOM_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/lightswitch_medium/domain_temp.pddl'
    PROB_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/lightswitch_medium/prob_templ.pddl'
    PROP_LIST = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/lightswitch_medium/prop_list'
    problem_list = []
    level_prob_nums = [6, 4]
    for i in range(len(level_prob_nums)):
        level = []
        for j in range(level_prob_nums[i]):
            path = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/lightswitch_medium/Length_{}/prob{}.pddl'.format(i + 1, j + 1)
            level.append(path)
        problem_list.append(level)
elif problem_set == 2:
    print("4 Props 7 Acts")
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
elif problem_set == 3:
    print("8 Props 12 Acts")
    DOMAIN_MOD = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_8prop_12act/domain.pddl'
    PROB = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_8prop_12act/prob.pddl'
    DOM_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_8prop_12act/domain_temp.pddl'
    PROB_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_8prop_12act/prob_templ.pddl'
    PROP_LIST =  RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_8prop_12act/prop_list'
    problem_list = []
    level_prob_nums = [3, 7, 12, 19, 30, 34, 39, 33, 18, 10]
    for i in range(len(level_prob_nums)):
        level = []
        for j in range(level_prob_nums[i]):
            path = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_8prop_12act/Length_{}/prob{}.pddl'.format(i + 1, j + 1)
            level.append(path)
        problem_list.append(level)
elif problem_set == 4:
    print("16 Props 24 Acts")
    DOMAIN_MOD = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_16prop_24act/domain.pddl'
    PROB = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_16prop_24act/prob.pddl'
    DOM_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_16prop_24act/domain_temp.pddl'
    PROB_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_16prop_24act/prob_templ.pddl'
    PROP_LIST =  RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_16prop_24act/prop_list'
    problem_list = []
    level_prob_nums = [7, 30, 30, 30, 30, 30, 25, 23, 19, 9, 10, 11]
    for i in range(len(level_prob_nums)):
        level = []
        for j in range(level_prob_nums[i]):
            path = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_16prop_24act/Length_{}/prob{}.pddl'.format(i + 1, j + 1)
            level.append(path)
        problem_list.append(level)



env = gym.make('oracle-v0')
env.setPDDL(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST, problem_list)

state = env.reset()
counter = 0
done = False
while not done:
    for i in range(0, 250):
        #print(i, end='')
        legal_actions = env.getLegalActions()
        legal_actions.remove('EVAL')
        act = random.choice(legal_actions)
        next_state, reward, done, info = env._step(act)
        counter += 1
    next_state, reward, done, info = env._step('EVAL')

print("Number Samples Needed: ", counter)