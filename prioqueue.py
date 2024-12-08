"""prioqueue.py

initial notes - class, works as the scheduling logic behind executor. N

no exec capacity, pure queue with accept/n'accept stuff

assumes need for datetime or some kind of internal timing chop

probably wa

[ ]: testing


for the purposes of the module, default design 
"""

import datetime
import logging
import math
import collections

LOGGER = logging.getLogger(__name__)

# TODO: pushback in case of an accdiental pop?

class PrioQueue(object):
    """A container of commands to execute and their priority from 0
    to the defined maximum - note that 0 is considered LOW 

    time is from datetime and is stored for forensics purposes
    
    NOTE: does not deal with execution
    """

    def __init__(self, max_size: int = None, highest_priority: int = 10):
        """Raises an exception for sizes < 1
        does NOT raise an exception for a highest priority that is 0 which is the degenerate case of a list (but will warn)
        
        """
        if max_size is not None:
            self.max_size = math.floor(max_size) 
            if self.max_size < 1:
                raise ValueError("Max PrioQueue size requested is < 1") # that's.. not a queue.
        else:
            self.max_size = None
        
        self._highest_priority = self._conform_priority(highest_priority, on_init=True)
        if self._highest_priority == 0:
            LOGGER.warning("Highest priority allowed is 0, this is effectively a list?")

        self._task_dict = {x:collections.deque() for x in range(0,self.max_prio+1)}
        self._taskcount = 0

    def _conform_priority(self, priority: int, on_init=False):
        """Given a priority, return the correct integerized number
        
        Effectively, this is a truncate-to-zero function with an upper
        range set at module init time.

        Raises TypeError if you supply a non-conformable priority (like 'NOW')
        """

        # always range out negatives. this step will also catch the issue of
        # malformed priority codes
        try:
            if priority < 0:
                return 0
        except TypeError: # 
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

    
    ### admin/info functions
    @property
    def count(self):
        """how many commands are stored?"""
        return self._taskcount

    @property
    def max_prio(self):
        """what is the maxium priority
        Protected as we don't want people to mangle max prio once instantiated."""
        return self._highest_priority
    
    def _build_command(self, command, priority):
        """Build out our command dict, including conforming the priority"""

    def push(self, command, priority):
        """put the command into storage into it's correct priority ordering
        
        Raises ValueError if the queue is full.
        
        Returns the command dict with the timestamp accepted, this allows checking of the conformed priority"""
        command_dict = {"command": command,
         "priority": self._conform_priority(priority),
         "add_time": datetime.datetime.now()}
        
        if self.max_size is not None and self.count == self.max_size:
            raise ValueError(f"PrioQueue at capacity {self.max_size}, cannot add")
        
        self._task_dict[command_dict["priority"]].append(command_dict)
        self._taskcount+=1

        return command_dict

    def pop(self):
        """Attempt to get the next task that this queue thinks should be executed. 
        can return a Nonevalue

        will return a command
        """
        
        # early bail, since the other case we walk backwards through the dict
        if self.count < 1:
            return None

        # walk backwards
        for priority in range (self.max_prio, -1, -1):  # this really still bugs me I need a -1
            try:
                next_task = self._task_dict[priority].popleft()
            except IndexError:
                continue # nothing in this prio level
            self._taskcount-=1
            return next_task
        
        # if you have a working self.count trap, this clause
        # can't be hit
        # else:
        #     return None


    
