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
class LsLiteEnv(Env):
	def __init__(self):
		self.state = None
		self.observation_space = spaces.Tuple((int, int))
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
		action_start = 3 * len(self.PROPS) * act
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

		pre, eff = self.state
		str_length = 3*len(self.PROPS) * len(self.ACTS)
		accepted_relations = self.parse_input(format(pre,"b").zfill(str_length), 0)
		accepted_relations += self.parse_input(format(eff,"b").zfill(str_length), 1)

		valid_plan = self.mt.find_plan_and_test(accepted_relations)
		print("Valid Plan Found: ", valid_plan)
		if valid_plan:
			reward = 10

		return self._get_obs(), done, reward, {}

	def setPDDL(self, DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST):
		self.mt = ModelSpaceTool(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST)
		print("##INITIALIAZING WITH PDDL")
		self.ACTS = self.mt.action_list
		self.PROPS = list(self.mt.proposition_set)
		for index in range(len(self.PROPS)):
			self.PROPS[index] = self.PROPS[index].strip("()")

		self.action_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(len(self.ACTS)), spaces.Discrete(len(self.PROPS)), spaces.Discrete(3)))
		print("Actions: ", self.ACTS)
		print("Propositions: ", self.PROPS)
		print("##END OF INITIALIZATION")

	'''
	Resets the environment to the starting state
	'''
	def _reset(self):
		prop_clear = ''
		for i in range(len(self.ACTS)):
			for j in range(len(self.PROPS)):
				prop_clear += '010'
		prop_clear = int(prop_clear, 2)
		self.state = (prop_clear, prop_clear)
		self._render()

	'''
	Returns the current state
	'''
	def _get_obs(self):
		return self.state
	'''
	Returns a list of possible actions based on current state

	def getLegalActions(self):
	'''
	
	def parse_input(self, input, clause):
		"""
		Parsing the (3 * n) bit input, based on the binary values.

		100 - Proposition exists in the positive form
		010 - Proposition is not present
		001 - Proposition exists in the negative form

		pre is a binary value of 0 or 1 indicating whether it is a precondition or effect
		0 = precondition
		1 = effect
		"""
		accepted_relations = [] #List that stores the actions that are accepted
		action_length = 3 * len(self.PROPS)
		total_actions = int(len(input) / action_length) #Each action has 6 binary values for the propositions tested
		action_index = total_actions - 1 #index starts at 0, so subtract 1 from the total_actions
		prop_index = len(self.PROPS) - 1
		for i in range(0, len(input)):
			if i % action_length == 0 and i != 0: #Updates the action_index for every 6 binary values
				action_index -= 1
				prop_index = len(self.PROPS) - 1
			if i % 3 == 0 and i % action_length != 0 and i != 0:
				prop_index -= 1
			if i % 3 == 0: #Tests 3 bits at a time to see if the proposition is valid
				if clause == 0:
					if input[i: i + 3] == "100":
						action = self.ACTS[action_index] + "_has_precondition_pos_" + self.PROPS[action_index]
						#print(action)
						accepted_relations.append(action)

					elif input[i: i + 3] == "001":
						action = self.ACTS[action_index] + "_has_precondition_neg_" + self.PROPS[prop_index]
						#print(action)
						accepted_relations.append(action)
					#else:
						#print(self.PROPS[prop_index] + " was NOT an accepted precondition for the action " + self.ACTS[action_index])
				else:
					if input[i: i + 3] == "100":
						action = self.ACTS[action_index] + "_has_effect_pos_" + self.PROPS[prop_index]
						#print(action)
						accepted_relations.append(action)

					elif input[i: i + 3] == "001":
						action = self.ACTS[action_index] + "_has_effect_neg_" + self.PROPS[prop_index]
						#print(action)
						accepted_relations.append(action)
					#else:

						#print(self.PROPS[prop_index] + " was NOT an accepted effect for the action " + self.ACTS[action_index])
		#Prints out the list of accepted relations
		#print("ACCEPTED ACTIONS: ")
		#for i in range(0, len(accepted_relations)):
		#	print(accepted_relations[i])
		
		## Return the accepted relations
		return accepted_relations

	'''
	Prints the current domain model
	'''
	def _render(self, mode='human', close = False):
		pre, eff = self.state
		str_length = 3*len(self.PROPS) * len(self.ACTS)
		props = self.parse_input(format(pre,"b").zfill(str_length), 0)
		props += self.parse_input(format(eff,"b").zfill(str_length), 0)
		#print("Pre: ", format(pre,"b").zfill(str_length))
		#print("Eff: ", format(eff,"b").zfill(str_length))
		print("Accepted relations: ", props)

def set_bit(value, index, flip):
	"""Set the index:th bit of value to 1 if flip = true, else 0"""
	mask = 1 << index
	value &= ~mask
	if flip:
		value |= mask
	return value
