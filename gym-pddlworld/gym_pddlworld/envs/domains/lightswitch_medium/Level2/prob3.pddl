(define (problem test)

(:domain switchworld)

(:objects )

(:init
(switch1_on)
(lightbulb1_on)
)


(:goal
(and
(lightbulb2_on)
(not (lightbulb1_on))
)
)

)
