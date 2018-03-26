import re
import argparse
import sys
import pddlpy
import yaml
import os
import copy
import numpy
import itertools
import random
import time

OPERATOR_DEFN_KEYS = ['precondition_pos','precondition_neg', 'effect_pos', 'effect_neg']
PLANNER_COMMAND = './fdplan.sh {} {}'
ACTION_DEF_STR = '(:action {}\n:parameters ()\n:precondition\n(and\n{}\n)\n:effect\n(and\n{}\n)\n)\n'
VAL_PLAN_CMD  = "./valplan.sh {} {} {}"

class ProbGen:
    def __init__(self, domain_model, problem, dom_templ, prob_templ):
        self.dom_prob = pddlpy.DomainProblem(domain_model, problem)
        self.original_domain_file = domain_model
        self.domain_template_file = dom_templ
        self.prob_template_file = prob_templ

        # get the model prop list and actions
        self.create_domain_set_and_action_list()
        self.goal_state = self.convert_prop_tuple_list(self.dom_prob.goals())
        self.init_state = self.convert_prop_tuple_list(self.dom_prob.initialstate())
        self.prev_goals = set()
        # get missing propositions
        with open(self.prob_template_file) as p_fd:
            self.prob_template_str = "\n".join([i.strip() for i in p_fd.readlines()])

    def convert_prop_tuple_list(self, orig_prop_list, skip_list = []):
        prop_list = set()
        for p in orig_prop_list:
            #print (p)
            if type(p) is tuple:
                prop = ' '.join([str(i) for i in p])
            else:
                prop = ' '.join([str(i) for i in p.predicate])
            #print ("prop",prop)
            if prop not in skip_list:
                prop_list.add(prop)
        return prop_list



    
    def create_domain_set_and_action_list(self):
        '''
            Creates a set of propositions representing the current domain model and set of actions
        '''
        self.domain_props = set()
        self.action_map =  {}
         
        for act in self.dom_prob.operators():
            for act_obj in list(self.dom_prob.ground_operator(act)):
                # TODO: Skipping parameters as it is a grounded domain model
                #sorted_var_name = list(act_obj.variable_list.keys())
                #sorted_var_name.sort()
                action_name = act_obj.operator_name #+ "_" + '_'.join(act_obj.variable_list[i] for i in sorted_var_name)
                self.action_map[action_name] = {}
                self.action_map[action_name]['precondition_pos'] = self.convert_prop_tuple_list(act_obj.precondition_pos)
                self.action_map[action_name]['precondition_neg'] =  self.convert_prop_tuple_list(act_obj.precondition_neg)
                self.action_map[action_name]['effect_pos'] = self.convert_prop_tuple_list(act_obj.effect_pos)
                self.action_map[action_name]['effect_neg'] = self.convert_prop_tuple_list(act_obj.effect_neg)

            

    def create_domain_file(self, dom_prop_set, dom_dest, prob_dest):
        act_map = {}
        for prop in  dom_prop_set:
            regex_probe = re.compile("(.*)_has_("+'|'.join(OPERATOR_DEFN_KEYS)+")_(.*)$").search(prop)
            action_name = regex_probe.group(1)
            condition = regex_probe.group(2)
            predicate_name = regex_probe.group(3)

            if action_name not in act_map.keys():
                act_map[action_name] = {}
                for cond in OPERATOR_DEFN_KEYS:
                    act_map[action_name][cond] = set()

            if condition not in act_map[action_name].keys():
                act_map[action_name][condition] = set()
            act_map[action_name][condition].add(predicate_name)

        action_strings = []

        for i in  act_map.keys():
            precondition_list = ['('+i+')' for i in act_map[i]['precondition_pos']]
            precondition_list += ['(not ('+i+'))' for i in act_map[i]['precondition_neg']]
            effect_list = ['('+i+')' for i in act_map[i]['effect_pos']]
            effect_list += ['(not ('+i+'))' for i in act_map[i]['effect_neg']]

            action_strings.append(ACTION_DEF_STR.format(i,"\n".join(precondition_list),"\n".join(effect_list)))

        

        dom_str = self.domain_template_str.format("\n".join(action_strings))


        goal_state = ['('+i+')' for i in self.goal_state]#self.convert_prop_tuple_list(self.dom_prob.goals())]
        init_state = ['('+i+')' for i in self.init_state] #self.convert_prop_tuple_list(self.dom_prob.initialstate())]

        prob_str = self.prob_template_str.format("\n".join(init_state), "\n".join(goal_state))

        with open(dom_dest, 'w') as d_fd:
            d_fd.write(dom_str)
        with open(prob_dest, 'w') as p_fd:
            p_fd.write(prob_str)



    def find_plan_and_test(self):
        tmp_domain = "/tmp/domain.pddl"
        tmp_problem = "/tmp/problem.pddl"
        tmp_plan = "/tmp/plan.sol"
        self.create_domain_file(meta_state, tmp_domain, tmp_problem)
        plan_lst = ['('+i.strip()+')' for i in os.popen(PLANNER_COMMAND.format(tmp_domain, tmp_problem)).read().strip().split('\n')]
        #print (plan_lst)
        if len(plan_lst) < 0:
            # You can return a false here if you are sure you wont have empty plans
            pass
        with open(tmp_plan, 'w') as p_fd:
            p_fd.write("\n".join(plan_lst))
        v_out = os.popen(VAL_PLAN_CMD.format(tmp_domain, tmp_problem, tmp_plan)).read().strip()
        return eval(v_out)

    def execute_plan(self, plan):
        curr_state = copy.deepcopy(self.init_state)
        for act in plan:
            if self.action_map[act]['precondition_pos'] <= curr_state and len(self.action_map[act]['precondition_neg'] & curr_state) == 0:
                for pred in self.action_map[act]['effect_neg']:
                    if pred in curr_state:
                        curr_state.remove(pred)
                for pred in self.action_map[act]['effect_pos']:
                    curr_state.add(pred)
            else:
                return None
        return curr_state    

    ## Generate an object level next state given some start state and action
    def generate_next_state(self, init_state, rand_act):
        curr_state = copy.deepcopy(init_state)
        action_effects = list()
        if self.action_map[rand_act]['precondition_pos'] <= curr_state and len(self.action_map[rand_act]['precondition_neg'] & curr_state) == 0:
            for pred in self.action_map[rand_act]['effect_neg']:
                if pred in curr_state:
                    curr_state.remove(pred)
                    action_effects.append(('del', pred))
            for pred in self.action_map[rand_act]['effect_pos']:
                curr_state.add(pred)
                action_effects.append(('add', pred))                
        else:
            return None
        return action_effects

    def generate(self):
        start_time = time.time()
        curr_time = time.time()
        init_state_str = "@".join(sorted(list(self.init_state)))
        init_state = ['('+i+')' for i in self.init_state]
        print(init_state)
        #nprint ("self.duration:",self.duration)
        self.prev_goals.add(init_state_str)
        while (curr_time - start_time) < self.duration:
            # sample a plan
            #print ("Generated ",self.prob_count," problems till now.")
            curr_acts = list(self.action_map.keys())
            print(curr_acts)
            random.seed()
            plan = list(random.sample(curr_acts, int(self.plan_length)))
            g_state = self.execute_plan(plan)
            if g_state:
                goal = list(g_state)
                goal.sort()
                if "@".join(goal) not in self.prev_goals:
                    self.prev_goals.add("@".join(goal))
                    self.prob_count += 1
                    new_goal_state = ['('+i+')' for i in goal]
                    new_prob_str = self.prob_template_str.format("\n".join(init_state), "\n".join(new_goal_state))
                    new_prob_dest = self.destination +'/prob'+str(self.prob_count)+'.pddl'
                    with open(new_prob_dest, 'w') as p_fd:
                        p_fd.write(new_prob_str)
            


def main():
    parser = argparse.ArgumentParser(description='''Script to generate problems with fixed plan length''',
                                     epilog="Usage >> python3 ProbGenScript.py")
    '''
        # Flags
        --generate_lattice
    '''
    parser.add_argument('-d', '--domain_model',   type=str, help="Domain file", required=True)
    parser.add_argument('-p', '--problem', type=str, help="Original problem file", required=True)
    parser.add_argument('-t', '--domain_templ', type=str, help="Domain template file")
    parser.add_argument('-s', '--prob_templ', type=str, help="Problem template file")
    parser.add_argument('-l', '--plan_length', type=str, help="Required plan length")
    parser.add_argument('-f', '--target_file_location', type=str, help="Directory where the new problem files will be saved")
    parser.add_argument('-r', '--runtime', type=str, help="Script Runtime")

    if not sys.argv[1:] or '-h' in sys.argv[1:]:
        print (parser.print_help())
        sys.exit(1)
    args = parser.parse_args()
    pg = ProbGen(args.domain_model, args.problem, args.domain_templ, args.prob_templ, args.plan_length, args.runtime, args.target_file_location)
    pg.generate()
if __name__ == "__main__":
    main()
