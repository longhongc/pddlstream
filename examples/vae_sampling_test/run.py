from __future__ import print_function
import os

from pddlstream.algorithms.search import solve_from_pddl
from pddlstream.algorithms.focused import solve_focused
from pddlstream.utils import read
from pddlstream.language.constants import get_length
from pddlstream.language.constants import print_solution
from pddlstream.language.generator import from_gen_fn, from_fn, empty_gen

DOMAIN_PDDL = """
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
      (Collision ?t)

      (AtPose ?o ?p)
      (AtGrasp ?o ?g)
      (HandEmpty)
      (AtConf ?q)

      (On ?o ?r)

    )

    (:action move_free
        :parameters (?q1 ?t ?q2)
        :precondition (and (Motion ?q1 ?t ?q2)(AtConf ?q1)(HandEmpty)(not (Collision ?t)))
        :effect (and (AtConf ?q2) (not (AtConf ?q1))))

    (:action move_holding
        :parameters (?q1 ?t ?q2 ?o ?g )
        :precondition (and (Motion ?q1 ?t ?q2)(AtConf ?q1) (AtGrasp ?o ?g) (not (HandEmpty))(not (Collision ?t)))
        :effect (and (AtConf ?q2) (not (AtConf ?q1))))


    (:action pick
        :parameters (?o ?p ?g ?q)
        :precondition (and (Kin ?o ?p ?g ?q)(AtPose ?o ?p) (HandEmpty) (AtConf ?q))
        :effect (and (AtGrasp ?o ?g)(not (AtPose ?o ?p))(not (HandEmpty))))


    (:action place
        :parameters (?o ?p ?g ?q)
        :precondition (and (Kin ?o ?p ?g ?q)(AtGrasp ?o ?g) (not (HandEmpty)) (AtConf ?q))
        :effect (and (AtPose ?o ?p)(HandEmpty) (not (AtGrasp ?o ?g))))


    (:derived (On ?o ?r)
        (exists (?p) (and (Supported ?o ?p ?r)(AtPose ?o ?p))))

)
"""


def read_pddl(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    return read(os.path.join(directory, filename))

def get_problem():
    #domain_pddl = read_pddl('domain.pddl')
    constant_map = {}
    stream_pddl = None
    stream_map = {}

    init = [
        ('Conf','#q1'),
        ('Conf','#q2'),
        ('Conf','#q3'),
        ('Conf','#q4'),
        ('AtConf','#q1'),
        ('Pose','#p2'),
        ('Pose','#p3'),
        ('Pose','#p4'),
        ('AtPose','a','#p2'),
        ('HandEmpty',),
        ('Stackable','a','red'),
        ('Supported','a','#p4','red'),
        ('Grasp','#g1'),
        ('Motion','#q1','#t12','#q2'),
        ('Motion','#q2','#t23','#q3'),
        ('Motion','#q3','#t34','#q4'),
        ('Motion','#q2','#t24','#q4'),
        ('Kin','a','#p2','#g1','#q2'),
        ('Kin','a','#p3','#g1','#q3'),
        ('Kin','a','#p4','#g1','#q4'), 
        #('Collision', '#t24')
    ]
    goal = ('On', 'a', 'red')
    #goal = ('AtConf', '#q2')
    #goal = ('test', 'a', '#g1', '#p2')

    return DOMAIN_PDDL, constant_map, stream_pddl, stream_map, init, goal

def solve_pddl():
    domain_pddl = read_pddl('domain.pddl')
    #stream_pddl = read_pddl('stream.pddl')
    problem_pddl = read_pddl('problem.pddl')

    plan, cost = solve_from_pddl(domain_pddl, problem_pddl)
    solved = plan is not None
    print('Solved: {}'.format(solved))
    print('Cost: {}'.format(cost))
    print('Length: {}'.format(get_length(plan)))
    if not solved:
        print('fail ')
        return
    for i, action in enumerate(plan):
        print('{}) {}'.format(i+1, ''.join(map(str, action))))
def solve_pddlstream():
    pddlstream_problem = get_problem()
    solution = solve_focused(pddlstream_problem, unit_costs=True)
    print_solution(solution)

def main():
    #solve_pddl()
    solve_pddlstream()

if __name__ == '__main__':
    main()
    
