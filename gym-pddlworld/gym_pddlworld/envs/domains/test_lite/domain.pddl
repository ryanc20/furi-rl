(define (domain switchworld)

(:requirements :strips :typing :negative-preconditions)
(:predicates
    (switch1_on)
    (lightbulb_on)
    (dummy)
)
(:action switchon_switch1
    :parameters ()
    :precondition (and (not (switch1_on)) (not (lightbulb_on)))
    :effect (and (switch1_on) (lightbulb_on))
)

(:action switchoff_switch1
    :parameters ()
    :precondition (and (switch1_on) (lightbulb_on))
    :effect (and (not (switch1_on)) (not (lightbulb_on)))
)
)
