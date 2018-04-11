import os

RL_DIR = os.environ.get('RL_DIR')

PLANNER_COMMAND = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/fdplan.sh {} {}'
VAL_PLAN_CMD  = RL_DIR + "furi-rl/gym-pddlworld/gym_pddlworld/envs/valplan.sh {} {} {}"

original_domain_file = '/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/domain.pddl'

problems = [
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob1.pddl',
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob2.pddl',
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob3.pddl',
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob4.pddl',
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob5.pddl',
	'/home/perry/Documents/Research/furi-rl/gym-pddlworld/gym_pddlworld/envs/domains/test_domain/Length_3/prob6.pddl',]

tmp_domain = "/tmp/domain.pddl"
tmp_problem = "/tmp/problem.pddl"
tmp_plan = "/tmp/plan.sol"

# Create a plan with the tmp_domain
# Validate the plan
for i in range(len(problems)):
	print("Problem: ", i)
	customProblem = problems[i]
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
