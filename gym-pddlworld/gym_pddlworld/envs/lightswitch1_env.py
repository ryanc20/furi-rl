from gym import Env
from gym import error, spaces
from gym_pddlworld.envs.ModelSpaceTools import ModelSpaceTool
import random

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

		##TEST ON PROBLEMS WITH SAME CHALLENGE LEVEL
		problems = self.problem_set[self.challenge_level - 1]
		numProbsSolved = 0
		numProbsNotSolved = 0
		reward = 0
		for problem in problems:
			valid_plan = self.mt.find_plan_and_test(accepted_relations, problem)
			#print("Valid Plan Found: ", valid_plan)
			if valid_plan:
				numProbsSolved += 1
				#reward = 100 * numProbsSolved
			else:
				numProbsNotSolved += 1
				#reward = -100 * (len(problems) - numProbsSolved)

		if numProbsSolved >= numProbsNotSolved:
			reward = 100 * (numProbsSolved)
		else:
			reward = -100 * (numProbsNotSolved)

		#if numProbsSolved == len(problems) and self.challenge_level < self.numLevels:
		if reward == 100 * len(problems):
			done = True	
			if self.challenge_level < self.numLevels:
				self.challenge_level += 1

		return self._get_obs(), reward, done, {}

	def setPDDL(self, DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST, problem_set):
		self.mt = ModelSpaceTool(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST)
		print("##INITIALIZING WITH PDDL")
		self.ACTS = self.mt.action_list
		self.PROPS = list(self.mt.proposition_set)
		self.problem_set = problem_set
		self.numLevels = len(problem_set)
		self.challenge_level = 1
		for index in range(len(self.PROPS)):
			self.PROPS[index] = self.PROPS[index].strip("()")
		self.PROPS.remove('dummy')
		self.action_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(len(self.ACTS)), spaces.Discrete(len(self.PROPS)), spaces.Discrete(3)))
		print("Actions: ", self.ACTS)
		print("Propositions: ", self.PROPS)
		print("Goals: ", self.mt.dom_prob.goals())
		print("Init State: ", self.mt.dom_prob.initialstate())
		print("##END OF INITIALIZATION")

	'''
	Resets the environment to the starting state
	'''
	def _reset(self):
		prop_array = ['010', '100', '001'] #picks random start state

		prop_clear = ''
		for i in range(len(self.ACTS)):
			for j in range(len(self.PROPS)):
				prop_clear += random.choice(prop_array)
		prop_clear = int(prop_clear, 2)
		self.state = (prop_clear, prop_clear)
		return self.state

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
						action = self.ACTS[action_index] + "_has_precondition_pos_" + self.PROPS[prop_index]
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
		props += self.parse_input(format(eff,"b").zfill(str_length), 1)
		#print("Pre: ", format(pre,"b").zfill(str_length))
		#print("Eff: ", format(eff,"b").zfill(str_length))
		print("Accepted relations: ", props)
	
	def getLegalActions(self, state):
		legal_actions = list()
		pre, eff = state
		str_length = 3*len(self.PROPS) * len(self.ACTS)
		legal_actions += self.parseLegalActions(format(pre,"b").zfill(str_length), 0)
		legal_actions += self.parseLegalActions(format(eff,"b").zfill(str_length), 1)
		return legal_actions


	def parseLegalActions(self, input, clause):
		legal_actions = list()
		action_length = 3 * len(self.PROPS)
		total_actions = len(self.ACTS)
		action_index = total_actions - 1
		prop_index = len(self.PROPS) - 1

		for i in range(0, len(input)):
			if i % action_length == 0 and i != 0: #Updates the action_index for every 6 binary values
				action_index -= 1
				prop_index = len(self.PROPS) - 1
			if i % 3 == 0 and i % action_length != 0 and i != 0:
				prop_index -= 1
			if i % 3 == 0: #Tests 3 bits at a time to see if the proposition is valid
				if input[i: i + 3] == "100":
					legal_actions.append((clause, action_index, prop_index, 1))
					legal_actions.append((clause, action_index, prop_index, 2))

				elif input[i: i + 3] == "001":
					legal_actions.append((clause, action_index, prop_index, 0))
					legal_actions.append((clause, action_index, prop_index, 1))
				elif input[i: i + 3] == "010":
					legal_actions.append((clause, action_index, prop_index, 0))
					legal_actions.append((clause, action_index, prop_index, 2))

		return legal_actions

	def serialize(self, state, action):
		"""
		Standard format to set for the key of the dictionary.
			"precond"-"effect"-"clause"-"act"-"prop"-"val"
		
		Where "precond" and "effect" come from the action as 2 integers,
		and "clause", "act", "prop", and "val" are integers from the 4-tuple
		from each legal action in getLegalActions(state).
		"""
		state_val = str(state[0]) + "-" + str(state[1])
		action_val = str(action[0]) + "-" + str(action[1]) + "-" + str(action[2]) + "-" + str(action[3])

		formatted_key = state_val + "-" + action_val 
		return formatted_key

	def testState(self, state):
		pre, eff = state
		
		#Convert state into propositions
		str_length = 3*len(self.PROPS) * len(self.ACTS)
		accepted_relations = self.parse_input(format(pre,"b").zfill(str_length), 0)
		accepted_relations += self.parse_input(format(eff,"b").zfill(str_length), 1)

		print("Here")
		print(accepted_relations)
		#Test the problems
		problems = self.problem_set[self.challenge_level - 1]
		numProbsSolved = 0
		for problem in problems:
			valid_plan = self.mt.find_plan_and_test(accepted_relations, problem)
			#print("Valid Plan Found: ", valid_plan)
			if valid_plan:
				print("Problem solved: ", problem)

def set_bit(value, index, flip):
	"""Set the index:th bit of value to 1 if flip = true, else 0"""
	mask = 1 << index
	value &= ~mask
	if flip:
		value |= mask
	return value
