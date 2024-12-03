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
