# stetho
[![Build Status](https://travis-ci.org/unitedstack/stetho.svg?branch=master)](https://travis-ci.org/unitedstack/stetho)

Stetho is a sophisticated debug bridge for OpenStack Neutron.

## Stetho Agent
Linstening in 0.0.0.0:9698 waiting for rpc request.

For get_interface() api, we use ifconfig to get complete information. But
output of ifconfig varis from a linux distribution to another, the api has been
tested on centos 6.5 and 7.0, and not for any other distributions.
