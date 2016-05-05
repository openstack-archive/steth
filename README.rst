=====
Steth
=====

A network inspection tool for OpenStack.


  * License: Apache License, Version 2.0
  * Source: https://git.openstack.org/cgit/openstack/steth
  * Bugs: https://bugs.launchpad.net/steth
  * Wiki: https://wiki.openstack.org/wiki/Steth
  * Docs: http://steth.readthedocs.org/


-----------
Description
-----------

Steth is an inspection tool that can aid in pinpointing issues before deployment
and during operation of an OpenStack environment.

It is modelled as agent(s)/client in which a controller interacts with agents
deployed in your environment.


----------
Background
----------

OpenStack networking can be deloyed as different architectures, such as ML2 with
OVS(legacy and DVR), Linux bridge, OVN, Dragonflow and so forth. However, they
all need enviromental prerequisites. For instance, VLAN needs to be configured
as we expect; bandwidth should meet our requirements; connection between nodes
should be active, etc.

Besides, with some well-deployed architectures, troubleshooting for VM
networking is difficult. For instance, why VM cannot get an IP address; or why
it cannot connect to Internet, etc. Steth integrates useful scripts and third
party tools(like iperf, tcpdump, etc.) to help operators keep tracking on VM
networking.


-------
Mission
-------

Steth is an introspection tool for OpenStack networking. Only proved to be
working in ML2 with OVS for now.


------------
Contributing
------------

All kinds of contributions are welcomed, such as documentation, bug fixes and
new features. If you have a new feature or idea, ask for feedback first before
spending lots of time on something.

Please search issues and merge requests before adding something new to avoid
duplicating efforts and conversations. Especially, when working on a bug you
should assign it to yourself before starting to work on it.

You can also post message in the OpenStack Developer mailinglist, prefixed
with [steth].
