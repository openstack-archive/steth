..
      Copyright 2011-2013 OpenStack Foundation
      All Rights Reserved.

      Licensed under the Apache License, Version 2.0 (the "License"); you may
      not use this file except in compliance with the License. You may obtain
      a copy of the License at

          http://www.apache.org/licenses/LICENSE-2.0

      Unless required by applicable law or agreed to in writing, software
      distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
      WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
      License for the specific language governing permissions and limitations
      under the License.

Welcome to Steth's developer documentation!
=============================================

Stetho is an inspection tool that can aid in pinpointing issues before deployment and during operation of an OpenStack environment.


Quick start
================
Steth is a network inspection tool for OpenStack. 
And Steth is modelled as agent(s)/client in which a controller interacts with
agents deployed in your environment. Let me introduce how to use steth.

* Download code

  Download the latest code from git repository. And run **python setup.py install**
  to install steth. After running that, you can **steth - -help** to confirm Steth
  is installed correctly.


* Deploy Steth Agent

  Steth Agent listen in 0.0.0.0:9698 in any nodes you want. And it is waiting for
  the RPC request. For now, we support CentOS 6.5, CentOS 7.0 and CentOS 7.1 only.
  In CentOS 6.5, you should run **service steth-agent start** to start steth-agent.
  In CentOS 7.0 and 7.1, you should run **systemctl start steth** to start steth-agent.

* Deploy Steth Client

  Steth Client is a stateless program. You can run **steth - -help** to show all steth
  commands that you can run.

* Configuration File
  Steth Client will read a configuration file when we run steth commands. By default configuration
  file located at /etc/steth/steth.conf.
