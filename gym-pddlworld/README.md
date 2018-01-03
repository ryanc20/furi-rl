# gym-pddlworld
The pddlworld environment is a single agent domain featuring a discrete state and action space.

## Environment
The state space of the environment consists of the variations of the grounded object domains that can be created using the following actions and propositions:

Simple lightswitch domain:
```
:predicates(
	(switch1_on)
	(lightbulb_on)
)

(:action switchon_sw1
	:parameters ()
	:precondition (and (not (switch1_on)))
	:effect (and (switch1_on) (lightbulb_on))
)

(:action switchoff_sw1
	:parameters ()
	:precondition (and (switch1_on))
	:effect(and (not (switch1_on)) (not (lightbulb_on))
)
```

## State
A state in the pddlworld environment is a tuple: `(preconditions, effects)`. 
The elements in the tuple are binary numbers with a length of 12: 
zzz yyy xxx www

Each triplet references the state of a particular proposition for an action in the metastate. The values that the triplet can take on are:
100 => proposition exists in the positive form
010 => proposition is not present
001 => proposition exists in the negative form

The index of the triplet indicates the action and proposition that is represented. It is most easily understood with reference to the following diagram:

```
 ---------------------------------------------
 |          |  Proposition 1 | Proposition 2 | 
 ---------------------------------------------
 | Action 1 |      www       |      xxx      | 
 --------------------------------------------
 | Action 2 |      yyy       |      zzz      |
 ---------------------------------------------

```

## Actions
The action space in the pddlworld environment is a tuple: 
`(clause, action_index, proposition_index, new_value )`

`clause` is a binary value
0 => Target the `preconditions`
1 => Target the `effects`

`action_index` indicates which action should be updated

`proposition_index` indicates which proposition should be updated

`new_value` indicates the value that the triplet should take on. Possible options are:
0 => 100
1 => 010
2 => 001

## Start State
The starting state will be a pddl domain where the actions have no preconditions or effects. More concretely, the starting state will be `(010010010010, 010010010010)` where both the preconditions and effects can be interpreted in the following way:
```
 -------------------------------------------------------------
 |                   |  (1) switch1_on   |  (2) lightbulb_on | 
 -------------------------------------------------------------
 | (1) switchon_sw1  |        010        |        010        | 
 -------------------------------------------------------------
 | (2) switchoff_sw1 |        010        |        010        |
 -------------------------------------------------------------
 ```

## Reward

## Episode Termination