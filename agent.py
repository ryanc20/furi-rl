import gym
import gym_pddlworld

env = gym.make('lslite-v0')
env.reset()
state, reward, done, log = env.step((0,0,1,0))
pre, eff = state
print(format(pre, "12b"))
print(format(eff, "12b"))
