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

### Default Thresholds Justification
- The DEFAULT_THRESHOLDS in this tool were carefully chosen based on general industry best practices and commonly observed system performance patterns. These values aim to strike a balance between catching potential performance issues and avoiding excessive false positives. Here’s the reasoning behind each value:

####Disk
tps (1000.0):
Disk transactions per second represent the I/O intensity of workloads. Systems with traditional disks or smaller SSDs often experience bottlenecks beyond 1000 TPS. While enterprise-grade SSDs or NVMe devices might sustain higher values, the threshold serves as a baseline for detecting unusual activity in most setups.

rkB/s and wkB/s (500,000.0):
High read/write throughput can indicate heavy workloads, such as database queries or file operations. While high throughput alone is not necessarily bad, sustained rates beyond 500 MB/s are atypical for regular workloads unless dealing with large storage arrays. This threshold serves to flag unexpected spikes.

areq_sz (512.0):
The average request size below 512 KB might indicate a system struggling with inefficiencies in small block I/O operations. Large request sizes (e.g., >1024 KB) can lead to latency under certain storage configurations, and values near the threshold help maintain balance.

aqu_sz (1.0):
Average queue size measures how many requests are waiting in the I/O queue. A queue size above 1.0 often correlates with bottlenecks or poorly optimized storage systems. Modern storage can handle brief spikes, but sustained high values suggest system-level adjustments are needed.

await (10.0 ms):
Latency in I/O operations impacts application performance. A 10 ms threshold is conservative and suitable for most environments, ensuring the tool flags conditions that could cause noticeable degradation.

%util (80.0):
Disk utilization indicates the percentage of time the disk is busy handling requests. Beyond 80%, the likelihood of saturation and queue buildup increases, causing degraded performance.

#### CPU
%user (70.0):
User CPU usage measures how much time the CPU spends executing non-kernel code. Sustained levels above 70% often indicate CPU saturation from user-space processes.

%system (30.0):
System CPU usage reflects kernel operations like I/O handling. Excessive time spent here (>30%) might indicate inefficiencies, misconfigurations, or excessive context switching.

%idle (20.0):
A low idle percentage (<20%) shows that the CPU has little breathing room, suggesting high system load. This threshold helps identify when the system is running at near-capacity.

#### Memory
kbmemfree (50,000.0 KB):
Free memory below 50 MB often indicates memory pressure, potentially leading to swapping or reduced application performance. Modern systems should have enough free memory to handle bursts of demand.

kbmemused (90.0%):
Used memory above 90% signals a system nearing full utilization. While Linux aggressively uses available memory for caching, sustained usage above this threshold warrants investigation.

kbactive (80.0%) and kbinact (20.0%):
Active memory reflects currently used memory for tasks. High active memory with low inactive memory reduces the system’s ability to use caches effectively, impacting overall efficiency.

#### Network
rxkB/s and txkB/s (100,000.0):
Network throughput thresholds correspond to typical performance for 1 Gbps links, which provide up to ~125 MB/s effective bandwidth. Spikes beyond this threshold suggest potential issues in data rates exceeding the network’s capacity.

rxdrop and txdrop (0.0):
Dropped packets are always a concern and often indicate issues with buffer overruns, hardware capacity, or misconfigurations. Any non-zero values should trigger immediate investigation.

rxerrs and txerrs (0.0):
Packet errors often point to faulty network hardware or incorrect configurations. Non-zero values signal a need for troubleshooting.

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
