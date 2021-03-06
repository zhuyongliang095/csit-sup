Packet Throughput Graphs
========================

Plotted results are generated by multiple executions of the same CSIT
performance tests across three physical testbeds within LF FD.io labs.
To provide a descriptive summary view, Box-and-Whisker plots are used to
display variation in measured throughput values, without making any
assumptions of the underlying statistical distribution.

For each plotted test case, Box-and-Whisker plots show the quartiles
(Min, 1st quartile / 25th percentile, 2nd quartile / 50th percentile /
mean, 3rd quartile / 75th percentile, Max) across collected data set
(data set size stated in the note below). Outliers are plotted as
individual points. Min and max values are plotted as bottom and top
Whiskers respectively. 2nd and 3rd quartiles are plotted as bottom and
top edge of the box. If multiple samples match only two values, and all
samples fall between them, then no whiskers are plotted. If all samples
have the same value, only a horizontal line is plotted.

*Title of each graph* is a regex (regular expression) matching all
throughput test cases plotted on this graph, *X-axis labels* are indices
of individual test suites executed by
`FD.io test executor dpdk performance jobs`_ jobs that created result output
files used as data sources for the graph, *Y-axis labels* are measured Packets
Per Second [pps] values, and the *Graph legend* lists the plotted test suites
and their indices.

.. note::

    Test results have been generated by
    `FD.io test executor dpdk performance jobs`_ with Robot Framework result
    files csit-dpdk-perf-\*.zip `archived here <../../_static/archive/>`_.
    Plotted data set size per test case is equal to the number of job executions
    presented in this report version: **10**.

.. toctree::

    l2
    ip4
