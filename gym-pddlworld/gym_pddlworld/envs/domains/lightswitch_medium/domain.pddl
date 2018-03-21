(define (domain switchworld)

(:requirements :strips :typing :negative-preconditions)
(:predicates
    (switch1_on)
    (lightbulb1_on)
    (switch2_on)
    (lightbulb2_on)
    (dummy)
)
(:action switchon_switch1
    :parameters ()
    :precondition (and (not (switch1_on)))
    :effect (and (switch1_on) (lightbulb1_on))
)

(:action switchoff_switch1
    :parameters ()
    :precondition (and (switch1_on))
    :effect (and (not (switch1_on)) (not( lightbulb1_on)))
)

(:action switchon_switch2
    :parameters ()
    :precondition (and (not (switch2_on)))
    :effect (and (switch2_on) (lightbulb2_on))
)

(:action switchoff_switch2
    :parameters ()
    :precondition (and (switch2_on))
    :effect (and (not (switch2_on)) (not( lightbulb2_on)))
)
)
