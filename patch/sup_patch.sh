#!/bin/bash
patch -p0 ../env/lib/python2.7/site-packages/paramiko/transport.py paramiko_transport.patch
