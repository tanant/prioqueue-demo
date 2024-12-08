import unittest
import prioqueue


class TestPrioqueue(unittest.TestCase):



    def test_basic(self):
        """can you even instantiate?"""
        # 
        # basic sanity check, note that this is an actual test for
        # if it was done in setup, and failed, it'd be an error

    def test_accept_task(self):
        """ accept a task, nothing exciting """

        # add task
        # check internal task count increments
        # check that it's there in the task inspectability table
        # should be correctly sorted
        # task max len

        # note you can add same task several times, no task ident
        # maybe we use time as the ident..

        pass

    def test_overflow(self):
        """ there's gotta be a limit to tasks """
        # instantiate with limit and then add past that
        # overflow logically follows accept
    


    def test_dequeue_task(self):
        """dequeue a task - ensure that it's not longer there """
        
        # pad with tasks, ensure that removal is successful
        # if no tasks, should not fail


    



    