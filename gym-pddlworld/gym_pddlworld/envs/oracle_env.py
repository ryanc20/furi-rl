from gym import Env
from gym import error, spaces
from gym_pddlworld.envs.bdd_ModelSpaceTools import bddModelSpaceTool
from gym_pddlworld.envs.ProbGenScript import ProbGen
import random
import os
from datetime import datetime
from pyeda.inter import *
import copy
from collections import defaultdict
import re
RL_DIR = os.environ.get('RL_DIR')
'''
ENVIRONMENT

OBSERVATION

ACTIONS

REWARD

START STATE

EPISODE TERMINATION
'''
class OracleEnv(Env):
	def __init__(self):
		self.state = None
		self.state_pre_has_effect = defaultdict(list)
		self.state_pre_no_effect = defaultdict(list)
		#self.observation_space = spaces.Tuple((int, int))
	
	def generate_sample(self, action):
		num_props = random.randint(1, len(self.PROPS)) ## number of props to sample
		init_state = set(random.sample(self.PROPS, num_props))
		##Choose random OBJ action
		rand_act = self.ACTS[random.randint(0, len(self.ACTS) - 1 )]\
		#CALL PROB GEN
		action_effects = self.probGen.generate_next_state(init_state, rand_act)

		return init_state, action_effects

	def format_expr(self, expr):
		expr = expr.replace("Or(", "(or ")
		expr = expr.replace("And(", "(and ")
		expr = expr.replace(",", "")
		expr = expr.replace("Not(", "(not")
		expr = re.sub("~([^\s]+)", r"(not \1)", expr)
		for prop in self.PROPS:
			if prop in expr:
				expr = expr.replace(prop, "({})".format(prop))
		return expr

	def create_expr(self, obj_state):
		#Create initial state expression
		obj_state = list(obj_state)
		if len(obj_state) != 0:
			init_expr = exprvar(obj_state[0])
			for i in range(1, len(obj_state)):
				prop = obj_state[i]
				init_expr = init_expr & exprvar(prop)
		return init_expr.simplify()
	
	def combine_by_disjunction(self, disjuncts):
		disjuncts = list(disjuncts)
		if len(disjuncts) != 0:
			expr = disjuncts[0]
			for i in range(1, len(disjuncts)):
				dis = disjuncts[i]
				expr = expr | dis
			return expr.simplify()
		else:
			return None

	def generate_preconditions(self):
		# Dictionary of action -> precondition
		preconditions = defaultdict(str)

		#Create precondition for each action
		for action in self.ACTS:
			pre_has_effect = self.combine_by_disjunction(self.state_pre_has_effect[action])
			pre_no_effect = self.combine_by_disjunction(self.state_pre_no_effect[action])
			if(pre_has_effect != None):
				# Case 1: We have data on what works and doesn't work
				if pre_no_effect != None:
					pre = pre_has_effect & ~pre_no_effect
					#pre = pre.to_dnf()
					preconditions[action] = self.format_expr(str(pre))
				# Case 2: We have data only on what works
				else:
					pre = pre_has_effect
					preconditions[action] = self.format_expr(str(pre))
			# Case 3: No data => precondition is empty
			else:
				preconditions[action] = '(and )'
			if preconditions[action] == '1':
				print(self.state_pre_has_effect[action])
				print(self.state_pre_no_effect[action])
				print(action, "_pre: ", preconditions[action]) 
		return preconditions

	def oracleAction(self, action):
		meta_updates = list()

		# Generate S, A, S' sample		
		init_state, action_effects = self.generate_sample(action)

		# Generate the BDD representation of S
		init_expr = self.create_expr(init_state)		

		# Determine meta-actions needed to update the meta-state effects
		# If S' != S, then add S to precondition has effect list
		if action_effects != None:
			self.state_pre_has_effect[action].append(init_expr)
			for eff in action_effects:
				todo, prop = eff
				if todo == 'add':
					meta_updates.append((1, self.ACTS.index(action), self.PROPS.index(prop), 0))
				else:
					meta_updates.append((1, self.ACTS.index(action), self.PROPS.index(prop), 2))
		# If S' == S, then add S to precondition no effect list
		else:
			self.state_pre_no_effect[action].append(init_expr)
		return meta_updates

	def updateState(self, meta_action):
		pre, eff = self.state
		clause, act, prop, val = meta_action

		# Determine if the precondition or effects should be 
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

	def evaluteProblemSet(self):
		reward = 0
		done = False
		
		# Test on problems with same challenge level
		problems = self.problem_set[self.challenge_level - 1]
		numProbsSolved = 0
		numProbsNotSolved = 0

		effects = self.getAcceptedRelations(self.state)
		precons = self.generate_preconditions()
		for problem in problems:
			valid_plan = self.mt.find_plan_and_test(precons, effects, problem)
			print("Valid Plan Found: ", valid_plan)
			if valid_plan:
				numProbsSolved += 1
			else:
				numProbsNotSolved += 1

		if numProbsSolved >= numProbsNotSolved:
			reward = 100 * (numProbsSolved)
		else:
			reward = -100 * (numProbsNotSolved)

		# Check if level is complete by comparing number of problems solved
		level_complete = numProbsSolved == len(problems)

		# Record Results if Level was completed
		if level_complete:
			pddl_file = '/tmp/domain.pddl'
			dest_file = '{}RL_Search_Results/{}:{}:{}_{}:{}_Level{}_domain_bdd_oracle_env.pddl'.format(RL_DIR, datetime.now().year, datetime.now().month, datetime.now().day, datetime.now().hour, datetime.now().minute, self.challenge_level)
			with open(dest_file, 'w') as d_fd:
				with open(pddl_file, 'r') as p_fd:
					d_fd.write(p_fd.read())
			print("Agent Passed Level: ", self.challenge_level)

		# Increment the challenge level OR end the search
		if level_complete and self.challenge_level < self.numLevels:
			self.challenge_level += 1
		elif level_complete and self.challenge_level == self.numLevels:
			done = True

		return reward, done

	'''
	Performs the input action and returns the resulting state, reward
	Input: action
	Ouput: state, reward, done, log_info
	'''
	def _step(self, meta_action):
		reward = 0
		done = False
		# Evalute the current model on the problem set
		if meta_action == 'EVAL':
			reward, done = self.evaluteProblemSet()
		# Perform the oracle action on the given object level action
		else:
			meta_updates = self.oracleAction(meta_action)
			## Perform all the updates to the meta-state
			for meta_act in meta_updates:
				self.updateState(meta_act)
		return self._get_obs(), reward, done, {}

	def setPDDL(self, DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST, problem_set):
		self.mt = bddModelSpaceTool(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL, PROP_LIST)
		self.probGen = ProbGen(DOMAIN_MOD, PROB, DOM_TEMPL, PROB_TEMPL)
		print("##INITIALIZING WITH PDDL")
		self.ACTS = self.mt.action_list
		self.PROPS = list(self.mt.proposition_set)
		self.problem_set = problem_set
		self.numLevels = len(problem_set)
		self.challenge_level = 1
		for index in range(len(self.PROPS)):
			self.PROPS[index] = self.PROPS[index].strip("()")
			var = exprvar(self.PROPS[index])
		if 'dummy' in self.PROPS:
			self.PROPS.remove('dummy')
		#self.action_space = spaces.Tuple((spaces.Discrete(2), spaces.Discrete(len(self.ACTS)), spaces.Discrete(len(self.PROPS)), spaces.Discrete(3)))
		print("Actions: ", self.ACTS)
		print("Propositions: ", self.PROPS)
		print("Goals: ", self.mt.dom_prob.goals())
		print("Init State: ", self.mt.dom_prob.initialstate())
		print("##END OF INITIALIZATION")

	'''
	Resets the environment to the starting state
	'''
	def _reset(self):
		# Instantiate state as clear 010 for every prop
		# prop_array = ['010', '100', '001'] 
		prop_clear = ''
		for i in range(len(self.ACTS)):
			for j in range(len(self.PROPS)):
				prop_clear += '010'
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
		props = self.getAcceptedRelations(self.state)
		#print("Pre: ", format(pre,"b").zfill(str_length))
		#print("Eff: ", format(eff,"b").zfill(str_length))
		print("Accepted relations: ", props)
	
	def getLegalActions(self):
		# Oracle action for each obj level action
		legal_actions = copy.deepcopy(self.ACTS)
		# Evaluation Action
		legal_actions.append('EVAL')
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
		if action=='ORACLE':
			action_val = 'ORACLE'
		else:
			action_val = str(action[0]) + "-" + str(action[1]) + "-" + str(action[2]) + "-" + str(action[3])

		formatted_key = state_val + "-" + action_val 
		return formatted_key

	def getAcceptedRelations(self, state):
		pre, eff = state
		str_length = 3*len(self.PROPS) * len(self.ACTS)
		accepted_relations = self.parse_input(format(pre,"b").zfill(str_length), 0)
		accepted_relations += self.parse_input(format(eff,"b").zfill(str_length), 1)
		return accepted_relations

def set_bit(value, index, flip):
	"""Set the index:th bit of value to 1 if flip = true, else 0"""
	mask = 1 << index
	value &= ~mask
	if flip:
		value |= mask
	return value
