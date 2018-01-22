import gym
import gym_pddlworld

env = gym.make('lslite-v0')
env.reset()
<<<<<<< HEAD
state, reward, done, log = env.step((0,0,1,0))
pre, eff = state
print(format(pre, "12b"))
print(format(eff, "12b"))
=======
state, reward, done, log = env.step((0,0,1,2))
pre, eff = state
print("Pre:", format(pre, "b").zfill(12))
print("Eff:", format(eff, "b").zfill(12))
>>>>>>> d19c593d0c41d72b52a859c07a0a71a3d8a869cd
