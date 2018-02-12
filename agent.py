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
else: 
    DOMAIN_MOD = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain.pddl'
    PROB = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob.pddl'
    DOM_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain_temp.pddl'
    PROB_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob_templ.pddl'
    PROP_LIST =  RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prop_list'

env = gym.make('lslite-v0')
env.setPDDL(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST)
state = env.reset()
<<<<<<< HEAD
print state
print env.getLegalActions(state)
=======

def train(Q, state, alpha, epsilon, gamma, num_of_episodes, env):
    """
    Trains the agent with predetermined alpha, epsilon,
    gamma, and number of episodes to train.
    """
    total_reward = 0
    reward = 0
    for episode in range(0, num_of_episodes):
        done = False
        while done == False:
            legal_actions = env.getLegalActions(state)
            action = random.choice(legal_actions) # picks a random action from the legal actions
            next_state, reward, done, info = env._step(action)
            current_key = env.serialize(state, action)
            Q[current_key] = reward
            next_legal_actions = env.getLegalActions(next_state)
            next_action = random.choice(next_legal_actions)
            next_key = env.serialize(next_state, next_action)
            Q[current_key] += alpha * (reward + (Q[next_key] - Q[current_key]))
            total_reward += reward
            state = next_state
    if episode % 10 == 0:
        print("Episode: {} Total Reward {}".format(episode, total_reward))
Q = {}
Q = defaultdict(lambda: 0, Q)
alpha =.6
epsilon = .1
gamma = .9
num_of_episodes = 50
print("State: ", state[0], state[1])
legal_actions = env.getLegalActions(state) #list of legal actions for the state
var = env.serialize(state, legal_actions[0]) #serialize requires an index of the legal actions list.
print("Key: ", var)

state = env.reset()
train(Q, state, alpha, epsilon, gamma, num_of_episodes, env)

>>>>>>> ryan/master
