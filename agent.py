import gym
import gym_pddlworld

DOMAIN_MOD = ''
PROB = ''
DOM_TEMPL = ''
PROB_TEMPL = ''
PROP_LIST = ''

if True:
    DOMAIN_MOD = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/domain.pddl'
    PROB = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prob.pddl'
    DOM_TEMPL = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/domain_temp.pddl'
    PROB_TEMPL = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prob_templ.pddl'
    PROP_LIST = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prop_list'
else: 
    DOMAIN_MOD = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain.pddl'
    PROB = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob.pddl'
    DOM_TEMPL = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain_temp.pddl'
    PROB_TEMPL = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob_templ.pddl'
    PROP_LIST = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prop_list'

env = gym.make('lslite-v0')
env.setPDDL(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST)
env.reset()
<<<<<<< HEAD
env.step((0,0,0,2))

=======
state, reward, done, log = env.step((0,0,1,2))
pre, eff = state
print("Pre:", format(pre, "b"))
print("Eff:", format(eff, "b"))
>>>>>>> bc30c1d5c51f3e852227972f22f450276ecd55dd
