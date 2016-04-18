-----------------------
Multi-node Architecture
-----------------------

::

                                                                     note that steth does not save
                                                                     any state, it acts as a rpc
                                                                     client which makes requests to steth
                                      +--------------------------+   agent(s) and analyses the result.
                                      |                          |
                                      |   +------CLI---------+   |
                                      |   |                  |   |
               +--------------------------+     steth        +--------------------------+
               |                      |   |                  |   |                      |
               |                      |   +--------+---------+   |                      |
               |                      |            |             |                      |
               |                      +--------------------------+                      |
               |                                   |                                    |
               v                                   v                                    v
  +-------+port:9698---------+        +-------+port:9698---------+         +-------+port:9698---------+
  |            ^             |        |            ^             |         |            ^             |
  |            |             |        |            |             |         |            |             |
  | +----------+-------+     |        | +----------+-------+     |         | +----------+-------+     |
  | |                  |     |        | |                  |     |         | |                  |     |
  | |   steth-agent    |     |        | |   steth-agent    |     |         | |   steth-agent    |     |
  | |                  |     |        | |                  |     |         | |                  |     |
  | +-----------+------+     |        | +-----------+------+     |         | +-----------+------+     |
  |             |            |        |             |            |         |             |            |
  |             |            |        |             |            |         |             |            |
  |  +----------v----------+ |        |  +----------v----------+ |         |  +----------v----------+ |
  |  | run command like:   | |        |  | run command like:   | |         |  | run command like:   | |
  |  | ping, iperf, tcpdump| |        |  | ping, iperf, tcpdump| |         |  | ping, iperf, tcpdump| |
  |  | or use scapy to send| |        |  | or use scapy to send| |         |  | or use scapy to send| |
  |  | packet              | |        |  | packet              | |         |  | packet              | |
  |  +---------------------+ |        |  +---------------------+ |         |  +---------------------+ |
  |                          |        |                          |         |                          |
  |                          |        |                          |         |                          |
  +--------------------------+        +--------------------------+         +--------------------------+


In a scenario using multiple nodes, Steth is a stateless CLI and controller.
It knows each steth agent and will read config files, interact with OpenStack,
and sending instructions to agents when needed.

Steth Agent is introduced to manage processes or run commands. It should be
installed in each compute and network node, and their IPs should be specified
in the config file of steth controller.


-----------
Steth Agent
-----------

Listening on 0.0.0.0:9698 and waiting for the rpc request.

Note: for get_interface() agent API, we use ifconfig to get full information.
However, the output of ifconfig varies from a Linux distribution to another.
The API has only been tested on CentOS 6.5 and 7.0. Any other distribution has
not been tested. If it works, please let us know.


