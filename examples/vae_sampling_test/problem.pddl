(define (problem test_pddl)
    (:domian test1)
    (:objects a)
    (:init
        (on a red)
        (Conf #q1)
        (Conf #q2)
        (Conf #q3)
        (Conf #q4)
        (AtConf #q1)

        (Pose #p2)
        (Pose #p3)
        (Pose #p4)
        (AtPose a #p2)

        (HandEmpty)
        (Stackable a red)
        (Supported a #p4 red)

        (Grasp #g1)

        (Motion #q1 #t12 #q2)
        (Motion #q2 #t23 #q3)
        (Motion #q3 #t34 #q4)
        (Motion #q2 #t24 #q4)

        (Kin a #p2 #g1 #q2)
        (Kin a #p3 #g1 #q3)
        (Kin a #p4 #g1 #q4)

    )
    (:goal (and (on a red)))
)
