(define (domain switchworld)

(:requirements :strips :typing :negative-preconditions)
(:predicates
    (switch1_on)
    (switch2_on)
    (switch3_on)
    (switch4_on)
    (switch5_on)
    (switch6_on)
    (switch7_on)
    (switch8_on)
    (light_bulb1_on)
    (light_bulb2_on)
    (light_bulb3_on)
    (light_bulb4_on)
    (light_bulb5_on)
    (light_bulb6_on)
    (light_bulb7_on)
    (light_bulb8_on)
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
(:action switchon_switch4
    :parameters ()
    :precondition (and (not (switch4_on)))
    :effect (and (switch4_on))
)
(:action switchon_switch5
	:parameters ()
    :precondition (and (not (switch5_on)))
    :effect (and (switch5_on))
)
(:action switchon_switch6
    :parameters ()
    :precondition (and (not (switc6_on)))
    :effect (and (switch6_on))
)
(:action switchon_switch7
    :parameters ()
    :precondition (and (not (switch7_on)))
    :effect (and (switch7_on))
)
(:action switchon_switch8
    :parameters ()
    :precondition (and (not (switch8_on)))
    :effect (and (switch8_on))
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
(:action switchoff_switch4
    :parameters ()
    :precondition (and (switch4_on))
    :effect (and (not (switch4_on)))
)
(:action switchoff_switch5
    :parameters ()
    :precondition (and (switch5_on))
    :effect (and (not (switch5_on)))
)
(:action switchoff_switch6
    :parameters ()
    :precondition (and (switch6_on))
    :effect (and (not (switch6_on)))
)
(:action switchoff_switch7
    :parameters ()
    :precondition (and (switch7_on))
    :effect (and (not (switch7_on)))
)
(:action switchoff_switch8
    :parameters ()
    :precondition (and (switch8_on))
    :effect (and (not (switch8_on)))
)
(:action switchon_bulb1
    :parameters ()
    :precondition (and (switch1_on) (not (switch2_on)) (switch3_on))
    :effect (and (light_bulb1_on))
)
(:action switchon_bulb2
    :parameters()
    :precondition (and (switch2_on) (switch3_on) (not (switch1_on)) (not (switch4_on)))
    :effect (and (light_bulb2_on))
)

(:action switchon_bulb3
    :parameters()
    :precondition (and (switch3_on) (not (switch1_on)) (not (switch2_on)) (switch4_on))
    :effect (and (light_bulb3_on))
)

(:action switchon_bulb4
    :parameters()
    :precondition (and (switch4_on) (switch1_on) (switch2_on) (not (switch3_on)))
    :effect (and (light_bulb4_on))
)
(:action switchon_bulb5
    :parameters ()
    :precondition (and (switch5_on) (not (switch1_on)) (switch7_on) (not (switch1_on)))
    :effect (and (light_bulb5_on))
)
(:action switchon_bulb6
    :parameters()
    :precondition (and (switch6_on) (switch2_on) (not (switch3_on)) (not (switch5_on)))
    :effect (and (light_bulb6_on))
)

(:action switchon_bulb7
    :parameters()
    :precondition (and (switch7_on) (not (switch8_on)) (not (switch3_on)) (switch1_on))
    :effect (and (light_bulb7_on))
)

(:action switchon_bulb8
    :parameters()
    :precondition (and (switch8_on) (switch3_on) (switch6_on) (not (switch7_on)))
    :effect (and (light_bulb8_on))
)
)
