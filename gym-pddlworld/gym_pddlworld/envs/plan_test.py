import os

RL_DIR = os.environ.get('RL_DIR')

PLANNER_COMMAND = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/fdplan.sh {} {}'
VAL_PLAN_CMD  = RL_DIR + "furi-rl/gym-pddlworld/gym_pddlworld/envs/valplan.sh {} {} {}"

original_domain_file = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/domain.pddl'

level_prob_nums = [3, 7, 12, 19, 30, 34, 39, 33, 18, 10]
problems = []

for i in range(10):
	level = []
	for j in range(level_prob_nums[i]):
		path = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_8prop_12act/Length_{}/prob{}.pddl'.format(i + 1, j + 1)
		level.append(path)
	problems.append(level)

problems = [
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob1.pddl',
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob2.pddl',
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_lite/prob3.pddl',
]

tmp_domain = "/tmp/domain.pddl"
tmp_problem = "/tmp/problem.pddl"
tmp_plan = "/tmp/plan.sol"

# Create a plan with the tmp_domain
# Validate the plan
if True:
	for customProblem in problems:
		print(customProblem)
		plan_lst = ['('+i.strip()+')' for i in os.popen(PLANNER_COMMAND.format(tmp_domain, customProblem)).read().strip().split('\n')]
		if len(plan_lst) < 0:
		    # You can return a false here if you are sure you wont have empty plans
		    pass

		with open(tmp_plan, 'w') as p_fd:
		    p_fd.write("\n".join(plan_lst))
		v_out = os.popen(VAL_PLAN_CMD.format(original_domain_file, customProblem, tmp_plan)).read().strip()

		passed = eval(v_out)
		print(eval(v_out))	
		if not passed:
			print(plan_lst)
else:
	for i in range(len(problems)):
		level = problems[i]
		for j in range(len(level)):
			print("Level: {} \tProblem: {}".format(i+1, j + 1))
			customProblem = level[i]
			plan_lst = ['('+i.strip()+')' for i in os.popen(PLANNER_COMMAND.format(tmp_domain, customProblem)).read().strip().split('\n')]
			if len(plan_lst) < 0:
			    # You can return a false here if you are sure you wont have empty plans
			    pass

			with open(tmp_plan, 'w') as p_fd:
			    p_fd.write("\n".join(plan_lst))
			v_out = os.popen(VAL_PLAN_CMD.format(original_domain_file, customProblem, tmp_plan)).read().strip()

			passed = eval(v_out)
			print(eval(v_out))	
			if not passed:
				print(plan_lst)
