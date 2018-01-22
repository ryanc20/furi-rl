from gym import Env
from gym import error, spaces
from gym_pddlworld.envs.ModelSpaceTools import ModelSpaceTool
'''
ENVIRONMENT

OBSERVATION

ACTIONS

REWARD

START STATE

EPISODE TERMINATION
'''

ACTS = ['switchon_sw1', 'switchoff_sw1']
PROPS = ['switch1_on', 'lightbulb_on']

DOMAIN_MOD = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/domain.pddl'
PROB = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prob.pddl'
DOM_TEMPL = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/domain_temp.pddl'
PROB_TEMPL = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prob_templ.pddl'
PROP_LIST = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/prop_list'
class LsLiteEnv(Env):
	def __init__(self):
		self.mt = ModelSpaceTool(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST)
		print("INITIALIAZING WITH PDDL")
		print(self.mt.proposition_set)
		print(self.mt.action_list)
		print("END OF INITIALIZATION")
		self.state = None
	'''
	Performs the input action and returns the resulting state, reward
	Input: action
	Ouput: state, reward, done, log_info
	'''
	def _step(self, action):
		clause, act, prop, val = action
		pre, eff = self.state
		done = False
		reward = 0

		target_clause = pre
		if clause:
			target_clause = eff

		# Calculate starting index for triplet
		action_start = 3 * len(PROPS) * act
		prop_start = 3 * prop
		triplet_index = action_start + prop_start
		
		# Change bits for target triplet to 000
		new_clause_val = set_bit(target_clause, triplet_index, 0)
		new_clause_val = set_bit(new_clause_val, triplet_index + 1, 0)
		new_clause_val = set_bit(new_clause_val, triplet_index + 2, 0)

		if val == 0:
			# Change triplet to 100
			new_clause_val = set_bit(new_clause_val, triplet_index + 2, 1)
		elif val == 1:
			# Change triplet to 010
			new_clause_val = set_bit(new_clause_val, triplet_index + 1, 1)
		else:
			# Change triplet to 001
			new_clause_val = set_bit(new_clause_val, triplet_index, 1)
		if clause == 0:
			self.state = (new_clause_val, eff)
		else:
			self.state = (pre, new_clause_val)

		return self._get_obs(), done, reward, {}

	'''
	Resets the environment to the starting state
	'''
	def _reset(self):
		prop_clear = int('010010010010', 2)
		self.state = (prop_clear, prop_clear)
		self._render()

	'''
	Returns the current state
	'''
	def _get_obs(self):
		return self.state

	'''
	Prints the current domain model
	'''
	def _render(self, mode='human', close = False):
		pre, eff = self.state
		print("Preconditions:", format(pre, "12b"))
		print("Effects:", format(eff, "12b"))
	'''
	Returns a list of possible actions based on current state
	
	def getLegalActions(self):
	'''
	@property
	def observation_space(self):
		# (preconditions, effects)
		# Elements in the tuple are binary values that represent state
		# 010010010010 => 010 010 010 010
		return spaces.Tuple(int, int)

	@property
	def action_space(self):
		return spaces.Tuple(spaces.Discrete(2), spaces.Discrete(2), spaces.Discrete(2), spaces.Discrete(3))

def set_bit(value, index, flip):
	"""Set the index:th bit of value to 1 if flip = true, else 0"""
	mask = 1 << index
	value &= ~mask
	if flip:
		value |= mask
	return value