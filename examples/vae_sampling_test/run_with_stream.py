from __future__ import print_function
import os
import cProfile
import pstats

from pddlstream.algorithms.search import solve_from_pddl
from pddlstream.algorithms.focused import solve_focused
from pddlstream.algorithms.incremental import solve_incremental
from pddlstream.utils import read, INF, get_file_path
from pddlstream.language.constants import get_length
from pddlstream.language.constants import print_solution
from pddlstream.language.generator import from_gen_fn, from_sampler, from_test, from_fn, empty_gen
from pddlstream.language.stream import DEBUG
#from examples.pybullet.utils.pybullet_tools.kuka_primitives import get_stable_gen

DOMAIN_PDDL = """
(define (domain test1)
    (:requirements :strips :equality)
    (:predicates
      (Stackable ?o ?r)
      (Grasp ?g)
      (Conf ?q)
      (Pose ?p)
      (Region ?r)
      (Object ?o)
      (Traj ?t)

      (Kin ?o ?p ?g ?q)
      (Motion ?q1 ?t ?q2)
      (Supported ?o ?p ?r)
      (NoCollision ?t)

      (AtPose ?o ?p)
      (AtGrasp ?o ?g)
      (HandEmpty)
      (AtConf ?q)

      (On ?o ?r)

    )

    (:action move_free
        :parameters (?q1 ?t ?q2)
        :precondition (and (Motion ?q1 ?t ?q2)(AtConf ?q1)(HandEmpty)(NoCollision ?t))
        :effect (and (AtConf ?q2) (not (AtConf ?q1))))

    (:action move_holding
        :parameters (?q1 ?t ?q2 ?o ?g )
        :precondition (and (Motion ?q1 ?t ?q2)(AtConf ?q1) (AtGrasp ?o ?g) (not (HandEmpty))(NoCollision ?t))
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
def get_traj_gen():
    def gen(obj, pos, grasp, conf1):
        if (pos[1] != conf1[1]):
            conf2 = 'q'+pos[1]
            traj = 't'+conf1[1]+conf2[1]
            print("Sample traj:", traj) 
            yield (conf2, traj)

    return gen

def get_collision_check():
    def gen(conf1, traj, conf2):
        print("Collsion test")
        print(traj)
        if (traj != "t24"):
            print("Not Collide")
            return True
        
    return gen

def get_grasp_check():
    def gen(obj, pos, grasp, conf):
        print("Grasp test")
        if (pos[1]==conf[1]):
            print("Can grasp")
            return True

    return gen

def get_stable_test():
    return True

def read_pddl(filename):
    directory = os.path.dirname(os.path.abspath(__file__))
    return read(os.path.join(directory, filename))

def get_problem():
    #domain_pddl = read_pddl('domain.pddl')
    constant_map = {}
    #stream_pddl = None
    #stream_pddl = read_pddl('stream.pddl')
    stream_pddl = read(get_file_path(__file__, 'stream.pddl'))
    #stream_map = DEBUG
    stream_map = {
           'vae-sampler': from_gen_fn(get_traj_gen()),
           'collision-checker': from_test(get_collision_check()),
           'grasp-checker': from_test(get_grasp_check())
    }
    init = [
        ('Conf','q1'),
        #('Conf','q2'),
        #('Conf','q3'),
        #('Conf','q4'),
        ('AtConf','q1'),
        ('Object', 'a'),
        ('Region','red'),
        ('Pose','p2'),
        ('Pose','p3'),
        ('Pose','p4'),
        ('AtPose','a','p2'),
        ('HandEmpty',),
        ('Stackable','a','red'),
        ('Supported','a','p4','red'),
        ('Grasp','g1'),
        #('Motion','q1','t12','q2'),
        #('Motion','q2','t23','q3'),
        #('Motion','q3','t34','q4'),
        #('Motion','q2','t24','q4'),
        #('Kin','a','p2','g1','q2'),
        #('Kin','a','p3','g1','q3'),
        #('Kin','a','p4','g1','q4') 
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
    _,_,_, stream_map, init, goal=pddlstream_problem
    print('Init:', init)
    print('Goal:', goal)
    #print('Streams:', stream_map.keys())
    pr = cProfile.Profile()
    pr.enable()
    solution = solve_incremental(pddlstream_problem, success_cost=INF)
    #solution = solve_incremental(pddlstream_problem)
    #solution = solve_focused(pddlstream_problem, success_cost=INF)
    print_solution(solution)
    pr.disable()
    pstats.Stats(pr).sort_stats('tottime').print_stats(10)

def main():
    #solve_pddl()
    solve_pddlstream()

if __name__ == '__main__':
    main()
    
