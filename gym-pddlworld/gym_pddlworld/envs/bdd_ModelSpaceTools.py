import re
import argparse
import sys
import pddlpy
import yaml
import os
import copy
import numpy
import itertools

RL_DIR = os.environ.get('RL_DIR')

OPERATOR_DEFN_KEYS = ['precondition_pos','precondition_neg', 'effect_pos', 'effect_neg']
PLANNER_COMMAND = RL_DIR + 'furi-rl/gym-pddlworld/gym_pddlworld/envs/fdplan.sh {} {}'
ACTION_DEF_STR = '(:action {}\n:parameters ()\n:precondition\n{}\n:effect\n(and\n{}\n)\n)\n'
VAL_PLAN_CMD  = RL_DIR + "furi-rl/gym-pddlworld/gym_pddlworld/envs/valplan.sh {} {} {}"

class bddModelSpaceTool:
    def __init__(self, domain_model, problem, dom_templ, prob_templ, proposition_list_file):
        self.original_domain_file = domain_model
        self.original_problem_file = problem
        self.dom_prob = pddlpy.DomainProblem(domain_model, problem)
        self.domain_template_file = dom_templ
        self.prob_template_file = prob_templ
        # get list of prop list
        with open(proposition_list_file) as p_fd:
            self.proposition_set = set(p.strip() for p in p_fd.readlines())
        # get the model prop list and actions
        self.create_domain_set_and_action_list()
        # get missing propositions
        self.missing_predicates = self.find_missing_predicate_set()
        with open(self.domain_template_file) as d_fd:
            self.domain_template_str = "\n".join([i.strip() for i in d_fd.readlines()])
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
        self.action_list =  []
         
        for act in self.dom_prob.operators():
            for act_obj in list(self.dom_prob.ground_operator(act)):
                # TODO: Skipping parameters as it is a grounded domain model
                #sorted_var_name = list(act_obj.variable_list.keys())
                #sorted_var_name.sort()
                action_name = act_obj.operator_name #+ "_" + '_'.join(act_obj.variable_list[i] for i in sorted_var_name)
                self.domain_props |= set(action_name+'_has_precondition_pos_'+i for i in self.convert_prop_tuple_list(act_obj.precondition_pos))
                self.domain_props |= set(action_name+'_has_precondition_neg_'+i for i in self.convert_prop_tuple_list(act_obj.precondition_neg))
                self.domain_props |= set(action_name+'_has_effect_pos_'+i for i in self.convert_prop_tuple_list(act_obj.effect_pos))
                self.domain_props |= set(action_name+'_has_effect_neg_'+i for i in self.convert_prop_tuple_list(act_obj.effect_neg))
                self.action_list.append(action_name)


    def find_missing_predicate_set(self):
        curr_set = set()
        for act in self.action_list:
            for prop in self.proposition_set:
                for cond in OPERATOR_DEFN_KEYS:
                    tmp_prop = act+'_has_' + cond + '_' + prop
                    if tmp_prop not in self.domain_props:
                        curr_set.add(tmp_prop)
        return curr_set
            

    def create_domain_file(self, dom_precons, dom_effects, dom_dest, prob_dest):
        #print("BDD MST: ", dom_precons)
        act_map = {}
        for prop in  dom_effects:
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
            
            act_map[action_name]['precondition'] = '(and )'
            act_map[action_name][condition].add(predicate_name)

        for action_name in dom_precons.keys():
            if action_name not in act_map.keys():
                act_map[action_name] = {}
            act_map[action_name]['precondition'] = dom_precons[action_name]
            for condition in ['effect_pos', 'effect_neg']:
                if condition not in act_map[action_name].keys():
                    act_map[action_name][condition] = set()

        action_strings = []

        for i in  act_map.keys():
            precondition_list = act_map[i]['precondition']
            #print("Action: ", i, "Preconditions: ", precondition_list)
            #precondition_list = ['('+i+')' for i in act_map[i]['precondition_pos']]
            #precondition_list += ['(not ('+i+'))' for i in act_map[i]['precondition_neg']]
            effect_list = ['('+i+')' for i in act_map[i]['effect_pos']]
            effect_list += ['(not ('+i+'))' for i in act_map[i]['effect_neg']]

            #action_strings.append(ACTION_DEF_STR.format(i,"\n".join(precondition_list),"\n".join(effect_list)))
            action_strings.append(ACTION_DEF_STR.format(i,precondition_list,"\n".join(effect_list)))

        
        dom_str = self.domain_template_str.format("\n".join(action_strings))


        self.goal_state = ['('+i+')' for i in self.convert_prop_tuple_list(self.dom_prob.goals())]
        if len(self.dom_prob.initialstate()) == 0:
            self.init_state = [' ']
        else:
            self.init_state = ['('+i+')' for i in self.convert_prop_tuple_list(self.dom_prob.initialstate())]

        prob_str = self.prob_template_str.format("\n".join(self.init_state), "\n".join(self.goal_state))
        
        with open(dom_dest, 'w') as d_fd:
            d_fd.write(dom_str)
        with open(prob_dest, 'w') as p_fd:
            p_fd.write(prob_str)



    def find_plan_and_test(self, precons, effects, customProblem):
        tmp_domain = "/tmp/domain.pddl"
        tmp_problem = "/tmp/problem.pddl"
        tmp_plan = "/tmp/plan.sol"
        self.create_domain_file(precons, effects, tmp_domain, tmp_problem)
        plan_lst = ['('+i.strip()+')' for i in os.popen(PLANNER_COMMAND.format(tmp_domain, customProblem)).read().strip().split('\n')]
        #print(plan_lst)
        
        if len(plan_lst) < 0:
            # You can return a false here if you are sure you wont have empty plans
            pass
        with open(tmp_plan, 'w') as p_fd:
            p_fd.write("\n".join(plan_lst))
        v_out = os.popen(VAL_PLAN_CMD.format(self.original_domain_file, customProblem, tmp_plan)).read().strip()
        return eval(v_out)


def main():
    parser = argparse.ArgumentParser(description='''The class for Meta space search''',
                                     epilog="Usage >> python3 ModelSpaceTools.py -d ../domains/test_domain/domain.pddl -p ../domains/test_domain/prob.pddl -t ../domains/test_domain/domain_temp.pddl -s ../domains/test_domain/prob_templ.pddl -l ../domains/test_domain/prop_list")
    '''
        # Flags
        --generate_lattice
    '''
    parser.add_argument('-d', '--domain_model',   type=str, help="Domain file with real PDDL model of robot.", required=True)
    parser.add_argument('-p', '--problem', type=str, help="Problem file for robot.", required=True)
    parser.add_argument('-t', '--domain_templ', type=str, help="Domain template file")
    parser.add_argument('-s', '--prob_templ', type=str, help="Problem template file")
    parser.add_argument('-l', '--prop_list', type=str, help="Possible Propositions at object level")

    if not sys.argv[1:] or '-h' in sys.argv[1:]:
        print (parser.print_help())
        sys.exit(1)
    args = parser.parse_args()
    mt = ModelSpaceTool(args.domain_model, args.problem, args.domain_templ, args.prob_templ, args.prop_list)
    #print ("Propositions", mt.proposition_set)
    #print ("Actions: ", mt.action_list)
    print ("Missing Predicates",mt.missing_predicates)
    print ("Domain Pred", mt.proposition_set)
    print ("Domain actions", mt.action_list)
    #print ("Missing Predicates",mt.missing_predicates)
    print ("Plan and test",mt.find_plan_and_test(mt.domain_props))

if __name__ == "__main__":
    main()
