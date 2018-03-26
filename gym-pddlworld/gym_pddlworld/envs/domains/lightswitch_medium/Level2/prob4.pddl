(define (problem test)

(:domain switchworld)

(:objects )

(:init
(switch1_on)
(lightbulb1_on)
(switch2_on)
(lightbulb2_on)
)


(:goal
(and
(not (lightbulb1_on))
(not (lightbulb2_on))
)
)

)
