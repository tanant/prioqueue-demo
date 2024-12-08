# prioqueue

## Description
Simple priority queue - assumes an incoming stream of dictionaries containing two keys; command to be executed and priority. Priority is an integer value [0, 10], where work items of the same priority are processed in the order they are received. 

0 is considered *low* priority and 10 is considered high (to be executed first)

## Design notes

### Priority mangling
For the PrioQueue we'll be trying to operate in a safe method expecting this to be something that's directly behind an artist frontend so it'll try conform priority inputs as much as possible (because an artist might try crank prio to 11, or split the difference between 5 and 6).

What this means is non-integer priorites will all be integerized towards zero, rather than throw errors. E.g:

- priority 100, 10.5 -> 10
- priority 1, 1.2, 1.9 -> 1
- priority -1 -> 0

### Boundary conditions (no tasks, and too many)
When pushing a new task onto the priority queue an overflow condition is considered an exception to signal out as the action can't be completed.

Consistent with the niceness in the priority mangling, when popping from an empty queue, this is _not_ considered an issue - a None will be returned. Caller clients can decide if this is fatal and exception-worthy.


## Developer notes

### Datastructures
#### Container
As we're using integer priorites for ease of storage (and also lookup/sorting) there is a memory bucket that a dict keyed by the discrete priorities that are allowed. Within each bucket commands are in a a deque so we can deal with things at the front/back easily. 

#### Command 'object'
Each command is a dict rather than a tuple
```
{ "command": the command string, 
  "priority": the priority requested
  "add_time": the date when this command was added (for forensics)
  }
```
Note: this is not an object, it's just a key/value package for simplicity