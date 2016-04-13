-----------------------
Multi-node Architecture
-----------------------

```
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
```

In a scenario using multiple nodes, Steth is a stateless CLI and controller.
It knows each steth agent and will read config files, interact with OpenStack,
and sending instructions to agents when needed. 

Steth Agent is introduced to manage processes or run commands. It should be
installed in each compute and network node, and their IPs should be specified
in the config file of steth controller.


