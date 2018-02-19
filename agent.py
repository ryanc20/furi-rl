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
else: 
    DOMAIN_MOD = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain.pddl'
    PROB = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob.pddl'
    DOM_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain_temp.pddl'
    PROB_TEMPL = RL_DIR +  'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob_templ.pddl'
    PROP_LIST =  RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prop_list'
    problem_list = [[RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob1.pddl',
                     RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob2.pddl' ]
                    ]

env = gym.make('lslite-v0')
env.setPDDL(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST, problem_list)
state = env.reset()

def flipCoin( p ):
    r = random.random()
    return r < p

def getValue(state):
    legal_actions = env.getLegalActions(state)
    qvalues = []
    for action in legal_actions:
        key = env.serialize(state, action)
        qvalues.append(Q[key])
    return max(qvalues)

def getPolicy(state):
    optAction = None
    optValue = float("-inf")
    for action in env.getLegalActions(state):
        key = env.serialize(state, action)
        if Q[key] > optValue:
            optValue = Q[key]
            optAction = action
    return optAction

def chooseAction(epsilon, state):
    legal_actions = env.getLegalActions(state)
    action = None
    if flipCoin(epsilon):
        action = random.choice(legal_actions)
    else:
        action = getPolicy(state)
    return action

def epsilonGreedyTrain(Q, state, alpha, epsilon, gamma, num_of_episodes, env):
    total_reward = 0
    reward = 0
    for episode in range(0, num_of_episodes):
        done = False
        cutoff_counter = 0     #cutoffs the agent after
        while done == False and cutoff_counter < 200:
            action = chooseAction(epsilon, state)
            next_state, reward, done, info = env._step(action)
            current_key = env.serialize(state, action)
            next_state_q_val = getValue(next_state)
            Q[current_key] += alpha * (reward + (next_state_q_val - Q[current_key]))
            total_reward += reward
            state = next_state
            print(len(Q))
            cutoff_counter += 1
        str_length = 3*len(self.PROPS) * len(self.ACTS)
        print(env.parse_input(format(state[0],"b").zfill(str_length), 0))
        if episode % 10 == 0:
            print("Episode: {} Total Reward {}".format(episode, total_reward))

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

            next_state, reward, done, info = env._step(action) #step function

            current_key = env.serialize(state, action)
            Q[current_key] = reward

            next_legal_actions = env.getLegalActions(next_state)
            next_action = random.choice(next_legal_actions)
            next_key = env.serialize(next_state, next_action)

            Q[current_key] += alpha * (reward + (Q[next_key] - Q[current_key]))

            total_reward += reward
            state = next_state
            print(len(Q))
        str_length = 3*len(self.PROPS) * len(self.ACTS)
        print(env.parse_input(format(state[0],"b").zfill(str_length), 0))
        if episode % 10 == 0:
            print("Episode: {} Total Reward {}".format(episode, total_reward))
Q = {}
Q = defaultdict(lambda: 0, Q)
alpha =.6       # learning rate
epsilon = .1    # epsilon-greedy rate
gamma = .9      # discount factor
num_of_episodes = 50
print("State: ", state[0], state[1])
legal_actions = env.getLegalActions(state) #list of legal actions for the state
var = env.serialize(state, legal_actions[0]) #serialize requires an index of the legal actions list.
print("Key: ", var)

state = env.reset()
#train(Q, state, alpha, epsilon, gamma, num_of_episodes, env)
epsilonGreedyTrain(Q, state, alpha, epsilon, gamma, num_of_episodes, env)
