import unittest
import prioqueue
import datetime
import logging


class TestPrioqueue(unittest.TestCase):

    def test_basic(self):
        """Can you even instantiate?"""

        # turn off the info/debug logging for presentation purposes
        prioqueue.LOGGER.setLevel(logging.ERROR)

        # basic sanity checks
        with self.assertRaises(ValueError):
            prioqueue.PrioQueue(max_size=-1, highest_priority=10)

        # use more detailed test setup later for complex cases, these are simple ranging
        # only checks
        for init_max_size, init_highest_prio in [
            (100, 10),
            (10, -2),
            (None, -2),
        ]:
            pq = prioqueue.PrioQueue(
                max_size=init_max_size, highest_priority=init_highest_prio
            )
            self.assertEqual(pq.count, 0, msg="initialsize")
            self.assertEqual(pq.max_size, init_max_size, msg="capacity")
            self.assertEqual(pq.max_prio, max(0, init_highest_prio), msg="priority")

    def test_accept_task(self):
        """Check that tasks are added with the correct conformed priority code"""

        highest_priority = 7
        pq = prioqueue.PrioQueue(highest_priority=highest_priority)

        # assert you couldn't add
        with self.assertRaises(TypeError, msg="text priority accepted"):
            pq.push("dostuff", "max")
        self.assertEqual(pq.count, 0)

        # add something that's higher, make sure it's added _but_
        # that the priority was max only
        result = pq.push("overprio", highest_priority + 1)
        self.assertEqual(result["priority"], highest_priority)
        self.assertEqual(pq.count, 1)

        result = pq.push("underprio", -1)
        self.assertEqual(result["priority"], 0)
        self.assertEqual(pq.count, 2)

        # Deal with fractionals
        result = pq.push("split high", 3.9)
        self.assertEqual(result["priority"], 3)
        self.assertEqual(pq.count, 3)

        result = pq.push("split low", 3.1)
        self.assertEqual(result["priority"], 3)
        self.assertEqual(pq.count, 4)

        # test the timestamping is present and Close Enough
        # TODO: widen delta range if the queue get performance issues
        now = datetime.datetime.now()
        result = pq.push("timestamp", 3.1)
        self.assertAlmostEqual(result["add_time"], now)

    def test_overflow(self):
        """There's gotta be a limit to tasks"""
        # instantiate with limit and then add past that
        # overflow logically follows accept

        max_size = 10
        pq = prioqueue.PrioQueue(max_size=max_size)

        # no exception should be raised here
        for x in range(0, max_size - 1):
            pq.push("dostuff", 0)
            self.assertNotEqual(pq.max_size, pq.count)

        # now we're full, but no overflow yet, we should be fiiiine
        pq.push("dostuff", 0)
        self.assertEqual(pq.max_size, pq.count)

        # and _now_ we should overflow
        with self.assertRaises(ValueError, msg="overflow not trapped"):
            pq.push("dostuff", 0)

        self.assertEqual(pq.max_size, pq.count)
        # TODO : find a task to make sure we didn't corrupt..
        #        this is harder to do and might require internal inspection and is
        #        implicitly done in the complex test below

    def test_underflow(self):
        """Check that we correctly handle underflow as per spec"""
        pq = prioqueue.PrioQueue()
        self.assertEqual(pq.pop(), None, msg="popping from empty did not return None")

        pq.push("dostuff", 0)
        self.assertNotEqual(pq.pop(), None)
        self.assertEqual(pq.pop(), None, msg="popping from empty did not return None")

    def test_ordering(self):
        """Check that our ordering follows both priority and insertion order"""
        pq = prioqueue.PrioQueue()

        tasks = [
            {"command": "a", "priority": 1},
            {"command": "b", "priority": 2},
            {"command": "c", "priority": 3},
            {"command": "d", "priority": 4},
            {"command": "e", "priority": 5},
            {"command": "f", "priority": 6},
            {"command": "aa", "priority": 1},
            {"command": "bb", "priority": 2},
            {"command": "cc", "priority": 3},
            {"command": "dd", "priority": 4},
            {"command": "aaa", "priority": 1},
        ]
        expected_order = ["f", "e", "d", "dd", "c", "cc", "b", "bb", "a", "aa", "aaa"]

        for task in tasks:
            pq.push(**task)

        # would love a dump all, but that'd be just for testing purposes
        # and don't want more code there..
        output_order = [pq.pop()["command"] for x in range(0, len(tasks))]
        self.assertEqual(output_order, expected_order)

        perturbed_tasks = tasks[::-1]
        for task in perturbed_tasks:
            pq.push(**task)
        output_order = [pq.pop()["command"] for x in range(0, len(tasks))]
        self.assertNotEqual(
            output_order,
            expected_order,
            msg="Tasks with same prio inserted in reverse order but output forward order",
        )
