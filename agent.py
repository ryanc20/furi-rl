import gym
import gym_pddlworld

env = gym.make('lslite-v0')
env.reset()
state, reward, done, log = env.step((0,0,1,2))
pre, eff = state
print("Pre:", format(pre, "b").zfill(12))
print("Eff:", format(eff, "b").zfill(12))
