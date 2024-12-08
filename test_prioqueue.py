import unittest
import prioqueue


import logging


class TestPrioqueue(unittest.TestCase):



    def test_basic(self):
        """can you even instantiate?"""
        
        # turn off the info/debug logging
        prioqueue.LOGGER.setLevel(logging.ERROR)
        
        # basic sanity checks
        with self.assertRaises(ValueError):
            prioqueue.PrioQueue(max_size=-1, highest_priority=10)
    
        # use more detailed test setup later for complex cases, these are simple ranging
        # only checks
        for init_max_size, init_highest_prio in [ 
                (100,10), 
                (10,-2),
                (None,-2),
            ]:
            pq = prioqueue.PrioQueue(max_size=init_max_size, highest_priority=init_highest_prio)
            self.assertEqual(pq.count, 0, "initialsize")
            self.assertEqual(pq.max_size, init_max_size, "capacity")
            self.assertEqual(pq.max_prio, max(0, init_highest_prio), "priority")




    def test_accept_task(self):
        """ accept a task, nothing exciting """

        # add task
        # check internal task count increments
        # check that it's there in the task inspectability table
        # should be correctly sorted
        # task max len

        # note you can add same task several times, no task ident
        # maybe we use time as the ident..

        # decide behaviours pls
        # human error try spec 4.4 (non-int)
        # human error try spec 12 (overmax)
        # human error try spec 12.5 (overmax and int)

        pass

    def test_overflow(self):
        """ there's gotta be a limit to tasks """
        # instantiate with limit and then add past that
        # overflow logically follows accept
        pq = prioqueue.PrioQueue(max_size=10, highest_priority=-2)
  
    


    def test_dequeue_task(self):
        """dequeue a task - ensure that it's not longer there """
        
        # pad with tasks, ensure that removal is successful
        # if no tasks, should not fail


    



    