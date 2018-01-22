(define (domain switchworld)

(:requirements :strips :typing :negative-preconditions)
(:predicates
    (switch1_on)
    (switch2_on)
    (switch3_on)
    (light_bulb_on)
)
(:action switchon_switch1
	:parameters ()
    :precondition (and (not (switch1_on)))
    :effect (and (switch1_on))
)
(:action switchon_switch2
    :parameters ()
    :precondition (and (not (switch2_on)))
    :effect (and (switch2_on))
)
(:action switchon_switch3
    :parameters ()
    :precondition (and (not (switch3_on)))
    :effect (and (switch3_on))
)
(:action switchoff_switch1
    :parameters ()
    :precondition (and (switch1_on))
    :effect (and (not (switch1_on)))
)
(:action switchoff_switch2
    :parameters ()
    :precondition (and (switch2_on))
    :effect (and (not (switch2_on)))
)
(:action switchoff_switch3
    :parameters ()
    :precondition (and (switch3_on))
    :effect (and (not (switch3_on)))
)
(:action switchon_bulb
    :parameters ()
    :precondition (and (switch1_on) (not (switch2_on)) (switch3_on))
    :effect (and (light_bulb_on))
)
)
