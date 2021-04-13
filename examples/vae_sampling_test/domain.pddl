(define (domain test1)
    (:requirements :strips :equality)
    (:predicates
      (Stackable ?o ?r)
      (Grasp ?g)
      (Conf ?q)
      (Pose ?p)

      (Kin ?o ?p ?g ?q)
      (Motion ?q1 ?t ?q2)
      (Supported ?o ?p ?r)

      (AtPose ?o ?p)
      (AtGrasp ?o ?g)
      (HandEmpty)
      (AtConf ?q)

      (On ?o ?r)
    )

    (:action move_free
        :parameters (?q1 ?q2 ?t)
        :precondition (and (Motion ?q1 ?t ?q2)
                           (AtConf ?q1) (HandEmpty))
        :effect (and (AtConf ?q2) (not (AtConf ?q1)))
    )

    (:action move_holding
        :parameters (?q1 ?q2 ?o ?g ?t)
        :precondition (and (Motion ?q1 ?t ?q2)
                           (AtConf ?q1) (AtGrasp ?o ?g) (not HandEmpty))
        :effect (and (AtConf ?q2) (not (AtConf ?q1)))
    )

    (:action pick
        :parameters (?o ?p ?g ?q)
        :precondition (and (Kin ?o ?p ?g ?q)
                           (AtPose ?o ?p) (HandEmpty) (AtConf ?q))
        :effect (and (AtGrasp ?o ?g)
                     (not (AtPose ?o ?p)) (not (HandEmpty)))
    )

    (:action place
        :parameters (?o ?p ?g ?q)
        :precondition (and (Kin ?o ?p ?g ?q)
                           (AtGrasp ?o ?g) (not (HandEmpty)) (AtConf ?q))
        :effect (and (AtPose ?o ?p)
                     (HandEmpty) (not (AtGrasp ?o ?g)))
    )

    (:derived (On ?o ?r)
        (exists (?p) (and (Supported ?o ?p ?r)
                          (AtPose ?o ?p)))
    )

)

