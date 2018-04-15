(define (problem test)

(:domain switchworld)

(:objects )

(:init
(switch2_on)
(lightbulb2_on)
)


(:goal
(and
(lightbulb1_on)
(not (lightbulb2_on))
)
)

)
