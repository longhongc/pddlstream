(define (domain manipulation-station)
  (:requirements :strips :equality)
  (:predicates
    (Stackable ?o ?s)
    (Sink ?r)
    (Stove ?r)

    (Robot ?r)
    (Kin ?r ?o ?p ?g ?q ?t)
    (Motion ?r ?q1 ?q2 ?t)
    (Pull ?r ?rq1 ?rq2 ?d ?dq1 ?dq2 ?t)
    (Supported ?o ?p ?s)

    ; "Type" static predicates
    (Conf ?r ?q)
    (Pose ?o ?p)
    (Grasp ?o ?g)
    (Traj ?t)


    ; Collision static predicates
    (TrajPoseCollision ?t ?o ?p)
    (TrajConfCollision ?t ?d ?q)

    ; Fluents
    (AtPose ?o ?p)
    (AtGrasp ?r ?o ?g)
    (HandEmpty ?r)
    (AtConf ?r ?q)
    (CanMove ?r)
    (Cleaned ?o)
    (Cooked ?o)

    ; Derived predicates (alternatively axioms)
    (On ?o ?s)
    (Holding ?o)
    (UnsafeTraj ?t)
  )

  (:action move
    :parameters (?r ?q1 ?q2 ?t)
    :precondition (and (Motion ?r ?q1 ?q2 ?t)
                       (AtConf ?r ?q1) (CanMove ?r))
    :effect (and (AtConf ?r ?q2)
                 (not (AtConf ?r ?q1)) (not (CanMove ?r)))
  )

  (:action pick
    :parameters (?r ?o ?p ?g ?q ?t)
    :precondition (and (Kin ?r ?o ?p ?g ?q ?t)
                       (AtPose ?o ?p) (HandEmpty ?r) (AtConf ?r ?q) (not (UnsafeTraj ?t)))
    :effect (and (AtGrasp ?r ?o ?g) (CanMove ?r)
                 (not (AtPose ?o ?p)) (not (HandEmpty ?r)))
  )
  (:action place
    :parameters (?r ?o ?p ?g ?q ?t)
    :precondition (and (Kin ?r ?o ?p ?g ?q ?t)
                       (AtGrasp ?r ?o ?g) (AtConf ?r ?q) (not (UnsafeTraj ?t)))
    :effect (and (AtPose ?o ?p) (HandEmpty ?r) (CanMove ?r)
                 (not (AtGrasp ?r ?o ?g)))
  )
  (:action pull
    :parameters (?r ?rq1 ?rq2 ?d ?dq1 ?dq2 ?t)
    :precondition (and (Pull ?r ?rq1 ?rq2 ?d ?dq1 ?dq2 ?t)
                       (HandEmpty ?r) (AtConf ?r ?rq1) (AtConf ?d ?dq1) (not (UnsafeTraj ?t)))
    :effect (and (AtConf ?r ?rq2) (AtConf ?d ?dq2) (CanMove ?r)
                 (not (AtConf ?r ?rq1)) (not (AtConf ?d ?dq1)))
  )

  (:action clean
    :parameters (?o ?s)
    :precondition (and (Stackable ?o ?s) (Sink ?s)
                       (On ?o ?s))
    :effect (Cleaned ?o)
  )
  (:action cook
    :parameters (?o ?s)
    :precondition (and (Stackable ?o ?s) (Stove ?s)
                       (On ?o ?s) (Cleaned ?o))
    :effect (and (Cooked ?o)
                 (not (Cleaned ?o)))
  )

  (:derived (On ?o ?s)
    (exists (?p) (and (Supported ?o ?p ?s)
                      (AtPose ?o ?p)))
  )
  (:derived (Holding ?r ?o)
    (exists (?g) (and (Robot ?r) (Grasp ?o ?g)
                      (AtGrasp ?r ?o ?g)))
  )

  (:derived (UnsafeTraj ?t)
    (or
      (exists (?o ?p) (and (TrajPoseCollision ?t ?o ?p) (Traj ?t) (Pose ?o ?p)
                           (AtPose ?o ?p)))
      (exists (?d ?q) (and (TrajConfCollision ?t ?d ?q) (Traj ?t) (Conf ?d ?q)
                           (AtConf ?d ?q)))
    )
  )
)