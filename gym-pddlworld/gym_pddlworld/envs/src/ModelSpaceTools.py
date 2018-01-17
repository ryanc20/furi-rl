import argparse
import sys
import pddlpy
import yaml
import os
import copy
import numpy
import itertools

OPERATOR_DEFN_KEYS = ['precondition_pos','precondition_neg', 'effect_pos', 'effect_neg']
PLANNER_COMMAND = './fdplan.sh {} {}'
ACTION_DEF_STR = '(:action {}\n:parameters ()\n:precondition\n(and\n{}\n)\n:effect\n(and\n{}\n)\n)\n'

class ModelSpaceTool:
    def __init__(self, domain_model, problem, dom_templ, prob_templ, proposition_list_file):
        self.dom_prob = pddlpy.DomainProblem(domain_model, problem)
        # get list of prop list
        with open(proposition_list_file) as p_fd:
            self.proposition_set = set(p.strip() for p in p_fd.readlines())
        # get the model prop list and actions
        self.create_domain_set_and_action_list()
        # get missing propositions
        self.missing_predicates = self.find_missing_predicate_set()

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
        self.domain_pred = set()
        self.action_list =  []
         
        for act in self.dom_prob.operators():
            for act_obj in list(self.dom_prob.ground_operator(act)):
                # TODO: Skipping parameters as it is a grounded domain model
                #sorted_var_name = list(act_obj.variable_list.keys())
                #sorted_var_name.sort()
                action_name = act_obj.operator_name #+ "_" + '_'.join(act_obj.variable_list[i] for i in sorted_var_name)
                self.domain_pred |= set(action_name+'_has_precondition_pos_'+i for i in self.convert_prop_tuple_list(act_obj.precondition_pos))
                self.domain_pred |= set(action_name+'_has_precondition_neg_'+i for i in self.convert_prop_tuple_list(act_obj.precondition_neg))
                self.domain_pred |= set(action_name+'_has_effect_pos_'+i for i in self.convert_prop_tuple_list(act_obj.effect_pos))
                self.domain_pred |= set(action_name+'_has_effect_neg_'+i for i in self.convert_prop_tuple_list(act_obj.effect_neg))
                self.action_list.append(action_name)


    def find_missing_predicate_set(self):
        curr_set = set()
        for act in self.action_list:
            for prop in self.proposition_set:
                for cond in OPERATOR_DEFN_KEYS:
                    tmp_prop = act+'_has_' + cond + '_' + prop
                    if tmp_prop not in self.domain_pred:
                        curr_set.add(tmp_prop)
        return curr_set
            

    def create_domain_file(self, dom_prop_set, dom_dest, prob_dest):
        act_map = {}
        for prop in  dom_prop_set:
            regex_probe = re.compile("(.*)_has_("+'|'.join(OPERATOR_DEFN_KEYS)+")_(.*)$").search(prop)
            action_name = regex_probe.group(1)
            condition = regex_probe.group(2)
            predicate_name = regex_probe.group(3)
            if action_name not in act_map.keys():
                act_map[action_name] = {}
            if condition not in act_map[action_name].keys():
                act_map[action_name][condition] = set()
            act_map[action_name][condition].add(predicate_name)

        for i in  act_map.keys():
            precondition_list = ['('+i+')' for i in act_map[i]['precondition_pos']]
            precondition_list += ['(not ('+i+'))' for i in act_map[i]['precondition_neg']]
            effect_list = ['('+i+')' for i in act_map[i]['effect_pos']]
            effect_list += ['(not ('+i+'))' for i in act_map[i]['effect_neg']]

            action_strings.append(ACTION_DEF_STR.format(i,"\n".join(precondition_list),"\n".join(effect_list)))
        dom_str = self.domain_template_str.format("\n".join(action_strings))


        self.goal_state = ['('+i+')' for i in self.convert_prop_tuple_list(self.dom_prob.goals())]
        self.init_state = ['('+i+')' for i in self.convert_prop_tuple_list(self.dom_prob.initialstate())]

        prob_str = self.prob_template_str.format("\n".join(self.init_state), "\n".join(self.goal_state))

        with open(dom_dest, 'w') as d_fd:
            d_fd.write(dom_str)
        with open(prob_dest, 'w') as p_fd:
            p_fd.write(prob_str)



    def find_plan(self, node):
        tmp_domain = "/tmp/domain.pddl"
        tmp_problem = "/tmp/problem.pddl"
        self.create_domain_problem(node, tmp_domain, tmp_problem)
        output = [i.strip() for i in os.popen(PLANNER_COMMAND.format(tmp_domain, tmp_problem)).read().strip().split('\n')]
        return output

       


def main():
    parser = argparse.ArgumentParser(description='''The driver Script for the Explanation generation''',
                                     epilog="Usage >> ./Explainer.py -d ../domain/original_domain.pddl -p" +
                                            " ../domain/original_problem.pddl -f ../domain/foil.sol")
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
    print ("Propositions", mt.proposition_set)
    print ("Actions: ", mt.action_list)
    #print ("Missing Predicates",mt.missing_predicates)
    #print ("Domain Pred", mt.domain_pred)
    #print ("Domain actions", mt.action_list)

if __name__ == "__main__":
    main()
