"""Demonstrator class to accept command/priority pairs and maintain them in order.
"""

import datetime
import logging
import math
import collections

LOGGER = logging.getLogger(__name__)


class PrioQueue(object):
    """
    A container of commands to execute and their priority from 0
    to the defined maximum. 0 is considered low-priority (last to execute).
    """

    def __init__(self, max_size=None, highest_priority=10):
        """Initialise the PrioQueue with range limits.

        Note a highest priority of 0 _can_ be provided so this effectively
        becomes a FIFO queue...

        Args:
            max_size: the limit of tasks this should store before raising an error (default None)
            highest_priority: the maximum integer priority class (default: 10)

        Raises:
            ValueError: size requested < 1
        """
        if max_size is not None:
            self.max_size = math.floor(max_size)
            if self.max_size < 1:
                raise ValueError(
                    "Max PrioQueue size requested is < 1"
                )  # that's.. not a queue.
        else:
            self.max_size = None

        self._highest_priority = self._conform_priority(highest_priority, on_init=True)
        if self._highest_priority == 0:
            LOGGER.warning("Highest priority allowed is 0, this is effectively a list?")

        self._task_dict = {x: collections.deque() for x in range(0, self.max_prio + 1)}
        self._taskcount = 0

    def _conform_priority(self, priority, on_init=False):
        """Given a priority, return the correct integerized number.

        Effectively, this is a truncate-to-zero function with an upper
        value from the value provided at module init time.

        Args:
            priority: value to conform
            on_init: whether or not to range the value back to thhe internal maxium for the class

        Raises:
            TypeError: if priority is non-conformable (like 'NOW')
        """

        # always range out negatives. this step will also catch the issue of
        # malformed priority codes
        try:
            if priority < 0:
                return 0
        except TypeError:  #
            raise TypeError(f"Priority '{priority}' is not a valid priority.")

        # if at initialisation, we have no state information so let it through
        # TODO: find a more elegant way to do this. Maybe classmethod with a param
        #       but that's kinda overcooking the design I swear.
        if on_init:
            return math.floor(priority)

        if priority > self.max_prio:
            return self.max_prio
        else:
            return math.floor(priority)

    @property
    def count(self):
        """How many commands are stored?"""
        return self._taskcount

    @property
    def max_prio(self):
        """what is the maxium priority level?

        Explicitly protected as the datastructure relies on this being set at init
        time and we cannot change it."""
        return self._highest_priority

    def push(self, command, priority):
        """Store a command, adding it to the correct priority ordering.

        Returns:
            A dict with the command, conformed priority and the timestamp accepted

        Args:
            command: the object (text string?) describing the command
            priority: a numerical value for the command's desired priority

        Raises:
            ValueError: if the queue is full.
        """
        command_dict = {
            "command": command,
            "priority": self._conform_priority(priority),
            "add_time": datetime.datetime.now(),
        }

        if self.max_size is not None and self.count == self.max_size:
            raise ValueError(f"PrioQueue at capacity {self.max_size}, cannot add")

        self._task_dict[command_dict["priority"]].append(command_dict)
        self._taskcount += 1

        return command_dict

    def pop(self):
        """Return the next command to be processed.

        Returns:
            A dict with the command, conformed priority and the timestamp the command was or None if there are no tasks.
        """

        # early bail, since the other case we walk backwards through the dict
        if self.count < 1:
            return None

        # walk backwards
        for priority in range(
            self.max_prio, -1, -1
        ):  # this really still bugs me I need a -1
            try:
                next_task = self._task_dict[priority].popleft()
            except IndexError:
                continue  # nothing in this prio level
            self._taskcount -= 1
            return next_task

        # if you have a working self.count trap, this clause
        # can't be hit
        # else:
        #     return None
