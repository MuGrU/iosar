# SAR Data Processor

## Overview
The **SAR Data Processor** is a Python script designed to analyze performance metrics from **System Activity Report (SAR)** files. It parses metrics related to **disk**, **CPU**, **memory**, and **network** performance, compares them against configurable thresholds, and generates alerts if any values exceed the defined limits.

The script is useful for system administrators or performance engineers who want to automate the analysis of SAR logs to monitor and troubleshoot system performance.

## Features
- Supports analysis of **disk**, **CPU**, **memory**, and **network** metrics from SAR logs.
- Generates alerts when any metric exceeds the predefined thresholds.
- Provides insights into potential performance bottlenecks, such as high disk I/O, CPU load, memory pressure, or network issues.
- Flexible thresholds for each metric to accommodate different system configurations.
- Option to run in verbose mode for detailed insights.

## Metrics & Thresholds
The script evaluates several performance metrics for each system resource, with predefined thresholds. Below is a summary of the key metrics and their associated thresholds:

### Disk Metrics:
- **tps**: Transactions per second. *Alert if greater than 1000*.
- **rkB/s**: Read throughput in KB/s. *Alert if greater than 500,000 KB/s*.
- **wkB/s**: Write throughput in KB/s. *Alert if greater than 500,000 KB/s*.
- **areq_sz**: Average request size in KB. *Alert if below 512 KB*.
- **aqu_sz**: Average queue size. *Alert if above 1*.
- **await**: Average wait time in ms. *Alert if greater than 10 ms*.
- **%util**: Disk utilization. *Alert if greater than 80%*.

### CPU Metrics:
- **%user**: User time. *Alert if greater than 70%*.
- **%system**: System time. *Alert if greater than 30%*.
- **%idle**: Idle time. *Alert if less than 20%*.

### Memory Metrics:
- **kbmemfree**: Free memory in KB. *Alert if below 50,000 KB*.
- **kbmemused**: Used memory as a percentage of total. *Alert if greater than 90%*.
- **kbactive**: Active memory as a percentage of total. *Alert if greater than 80%*.
- **kbinact**: Inactive memory as a percentage of total. *Alert if below 20%*.

### Network Metrics:
- **rxkB/s**: Receive throughput in KB/s. *Alert if greater than 100,000 KB/s*.
- **txkB/s**: Transmit throughput in KB/s. *Alert if greater than 100,000 KB/s*.
- **rxdrop**: Dropped received packets. *Alert if greater than 0*.
- **txdrop**: Dropped transmitted packets. *Alert if greater than 0*.
- **rxerrs**: Receive errors. *Alert if greater than 0*.
- **txerrs**: Transmit errors: Same as *rxerrs*.

- ## Usage:
- python3 iosar.py -f FILE -m {disk,cpu,memory,network} [--verbose]

```console
foo@bar:~$ python3 iosar.py -f SAfile -m disk --verbose
[...]
Metrics analyzed: {'tps': 15.11, 'rkB/s': 116.01, 'wkB/s': 778.38, 'areq-sz': 59.17, 'aqu-sz': 0.02, 'await': 1.49, '%util': 2.71}
Metrics analyzed: {'tps': 1828.27, 'rkB/s': 96399.45, 'wkB/s': 10975.81, 'areq-sz': 58.73, 'aqu-sz': 2.84, 'await': 1.55, '%util': 98.55}
Metrics analyzed: {'tps': 0.99, 'rkB/s': 0.03, 'wkB/s': 6.96, 'areq-sz': 7.09, 'aqu-sz': 0.0, 'await': 2.78, '%util': 0.13}
Metrics analyzed: {'tps': 0.78, 'rkB/s': 0.0, 'wkB/s': 6.24, 'areq-sz': 7.97, 'aqu-sz': 0.0, 'await': 1.12, '%util': 0.13}
Metrics analyzed: {'tps': 1.7, 'rkB/s': 0.07, 'wkB/s': 1591.48, 'areq-sz': 934.82, 'aqu-sz': 0.02, 'await': 12.96, '%util': 0.38}
Metrics analyzed: {'tps': 16.23, 'rkB/s': 16.07, 'wkB/s': 1938.5, 'areq-sz': 120.41, 'aqu-sz': 0.03, 'await': 1.7, '%util': 3.55}
Metrics analyzed: {'tps': 2749.03, 'rkB/s': 85361.37, 'wkB/s': 6803.07, 'areq-sz': 33.53, 'aqu-sz': 4.94, 'await': 1.8, '%util': 98.68}

Performance Issues Report:


Analyzing issue in line:
12:00:01 AM       DEV       tps     rkB/s     wkB/s   areq-sz    aqu-sz     await     svctm     %util
09:50:01 PM   dev8-32    544.34  59024.86    203.53    108.81      0.72      1.31      0.99     53.94

Detailed Analysis: Low areq-sz detected along with high %util and TPS. This might indicate inefficiency in handling small block sizes. Consider workload optimization.

Analyzing issue in line:
12:00:01 AM       DEV       tps     rkB/s     wkB/s   areq-sz    aqu-sz     await     svctm     %util
10:10:01 PM   dev8-32   1207.14 163818.12    474.53    136.10      2.86      2.37      0.73     88.21

Detailed Analysis: High %util with high TPS suggests efficient disk handling. Check for burst workloads.
High aqu-sz indicates queued I/O operations. Check if workloads can be optimized or parallelized.
Low areq-sz detected along with high %util and TPS. This might indicate inefficiency in handling small block sizes. Consider workload optimization.

End of report.
```
