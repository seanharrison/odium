# Odium: Remote Execution / Distributed Application Framework

## Dependencies:

* Python 3 (>= 3.5) and git are installed.

## Features:

* Remote execution: Arbitrary execution of code on remote systems under the connected user account.
* Job queue & distribution: Hub can push jobs to the queue, which are distributed among connected nodes.
* Versioned state: Each version of the configuration state has a unique id (hash of the state declaration), so that remotely executed commands can ensure the correct state for that command, thus ensuring that the calculation is done with the expected code / library / application / version.
* Any instance is both a hub and a node. It is a node to its source hub, it is a hub to any nodes that have connected to it.
* All communication encrypted between hub and node.

## Design:

* JSON for all messages.
* ZeroMQ for all network messaging.
* TCP port: default 18202, but configurable.
  (2018-02-02 = date of "Past Life" Agents of S.H.I.E.L.D. episode, first reference to odium)
* Node and hub communicate using PUB/SUB (broadcast/query => nodes), REQ/REP (query => hub)
  Also PUSH/PULL (job queue => nodes), and PULL/PUSH (result collection => hub).
  	* PUB / SUB @ 18202 (2/2 = first reference to odium)
    * REQ / REP @ 18242 (42 = the answer to ... everything)
    * PUSH / PULL @ 18222 (222... = an unending stream of pairs)
* Instance uses relational database to store configuration state, job queue, log, ... 
  (sqlite in the simple case)
* All communication includes the current configuration state id for the sending instance.
* Configuration state id = Application's current git commit hash.
* Configuration state includes: pip & system packages installed, state / environment data
* Commands (broadcast and queued) are executed in the application environment using multiprocess & subprocess. Results, logs, and errors are collected and returned via REQ => hub or PUSH => hub
* Asynchronous and multiprocessing:
	* node listens on a main thread for instructions, then pushes instructions to other threads for processing. It can thus handle an unlimited number of instructions before the first have finished.
	* hub listens on a main thread for requests, then pushes request processing to other threads.
	* hub & node both send messages on main thread.
* Communication encryption:
  * node REQ/keys with its public key (cleartext and signed), hub REP with its public key and node-encrypted AES key.
  * all other communication with the hub encrypted with the current AES key.
  * if the hub expires the current AES key, the node won't be able to send or receive messages, so will need to update AES by REQ/keys again (which is the only endpoint that is not encrypted).
