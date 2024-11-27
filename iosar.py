import subprocess
import argparse

# Default Thresholds
DEFAULT_THRESHOLDS = {
    "disk": {
        "tps": 1000.0,       # Transactions per second: Alert when above this value in regular workloads.
        "rkB/s": 500000.0,   # Read throughput in KB/s: Very high for most workloads; adjust for large storage arrays.
        "wkB/s": 500000.0,   # Write throughput in KB/s: Similar logic to `rkB/s`.
        "areq_sz": 512.0,    # Average request size in KB: Below this may indicate inefficiency or small I/O.
        "aqu_sz": 1.0,       # Average queue size: Above this suggests I/O bottlenecks.
        "await": 10.0,       # Average wait time in ms: Alert when above this; latency increases at higher values.
        "%util": 80.0        # Utilization: Alert above 80% to detect I/O saturation.
    },
    "cpu": {
        "%user": 70.0,       # User time: High sustained user time can indicate CPU saturation.
        "%system": 30.0,     # System time: High kernel overhead may indicate misconfigurations or inefficiency.
        "%idle": 20.0        # Idle time: Below 20% suggests a high CPU load.
    },
    "memory": {
        "kbmemfree": 50000.0,    # Free memory in KB: Alert when below this value; adjust for large memory systems.
        "kbmemused": 90.0,       # Used memory as % of total: Above 90% indicates potential memory pressure.
        "kbactive": 80.0,        # Active memory as % of total: High active memory usage often correlates with low free memory.
        "kbinact": 20.0,         # Inactive memory as % of total: Low inactive memory suggests reduced cache efficiency.
    },
    "network": {
        "rxkB/s": 100000.0,      # Receive throughput in KB/s: Adjust based on network bandwidth capacity.
        "txkB/s": 100000.0,      # Transmit throughput in KB/s: Adjust based on network bandwidth capacity.
        "rxdrop": 0.0,           # Dropped received packets: Any drops suggest issues; investigate immediately.
        "txdrop": 0.0,           # Dropped transmitted packets: Same as `rxdrop`.
        "rxerrs": 0.0,           # Receive errors: Non-zero errors suggest hardware or driver problems.
        "txerrs": 0.0            # Transmit errors: Same as `rxerrs`.
    }
}


# SAR Options and Metrics
METRIC_OPTIONS = {
    "disk": "-d", 
    "cpu": "-u", 
    "memory": "-r", 
    "network": "DEV"  # Looking for a fix (Error running SAR command: Command '['sar', '-t', '-n DEV', '-f', 'sa20241016']' returned non-zero exit status 1.)
}

COLUMN_NAMES = {
    "disk": ["tps", "rkB/s", "wkB/s", "areq-sz", "aqu-sz", "await", "%util"],
    "cpu": ["%idle", "%user", "%system"],
    "memory": ["kbmemfree", "kbmemused", "kbactive", "kbinact"],
    "network": ["rxpck/s", "txpck/s", "rxkB/s", "txkB/s", "rxcmp/s", "txcmp/s", "rxmcst/s", "%ifutil"]
}


def run_sar_command(file_path, sar_option):
    """Executes the SAR command for a specific metric."""
    try:
        if sar_option == "DEV":
            command = ["sar", "-t", "-n", sar_option, "-f", file_path]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
            return result.stdout
        else:    
            command = ["sar", "-t", sar_option, "-f", file_path]
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, check=True)
        return result.stdout
    
    except subprocess.CalledProcessError as error:
        print(f"Error running SAR command: {error}")
        return None


def find_column_index(header_line, column_name):
    """Finds the index of a specific column in the header."""
    columns = header_line.split()
    try:
        return columns.index(column_name)
    except ValueError:
        return -1


def analyze_metrics(parts, header, thresholds, metric_type, verbose=False):
    """
    Analyzes various metrics (disk, cpu, memory, etc.) and provides hints on performance issues.
    """
    thresholds = thresholds or DEFAULT_THRESHOLDS[metric_type]
    hints = []

    try:
        # Parse values based on header indices
        values = {}
        for col in COLUMN_NAMES[metric_type]:
            index = header.split().index(col)
            values[col] = float(parts[index])

        if verbose:
            print(f"Metrics analyzed: {values}")

    except (ValueError, IndexError) as e:
        if verbose:
            print(f"Error parsing metrics: {e}")
        return None

    # Disk-specific analysis
    if metric_type == "disk":
        util = values.get("%util", 0)
        await_time = values.get("await", 0)
        aqu_sz = values.get("aqu-sz", 0)
        tps = values.get("tps", 0)
        areq_sz = values.get("areq-sz", 0)

        if util >= thresholds["%util"]:
            if await_time > thresholds["await"] and aqu_sz > thresholds["aqu_sz"]:
                hints.append("I/O contention detected (high %util, await, and aqu-sz). Consider optimizing workloads or checking queue depths.")
            elif tps > thresholds["tps"]:
                hints.append("High %util with high TPS suggests efficient disk handling. Check for burst workloads.")
            else:
                hints.append("High %util detected. Monitor I/O patterns and workload intensity.")

        if aqu_sz > thresholds["aqu_sz"]:
            hints.append("High aqu-sz indicates queued I/O operations. Check if workloads can be optimized or parallelized.")

        if await_time > thresholds["await"]:
            if util > 1.0 and tps > 1.0:
                hints.append("High await time suggests possible disk latency. Investigate storage backend or disk health.")

        if areq_sz < thresholds["areq_sz"]:
            if util > 70.0 or tps > 500.0:
                hints.append(
                    "Low areq-sz detected along with high %util and TPS. This might indicate inefficiency in handling small block sizes. Consider workload optimization."
                )
        elif areq_sz > 1024.0:  # Example threshold for very large block sizes
            hints.append(
                "Large areq-sz detected. Verify if this aligns with workload expectations, as large I/O sizes may amplify latency in some cases."
            )

    # CPU-specific analysis
    elif metric_type == "cpu":
        idle = values.get("%idle", 100)

        if idle < thresholds["%idle"]:
            hints.append("High CPU usage detected (low %idle). Investigate processes consuming high CPU resources.")

    # Memory-specific analysis
    elif metric_type == "memory":
        free_mem = values.get("kbmemfree", 0)

        if free_mem < thresholds["kbmemfree"]:
            hints.append("Low free memory detected. Investigate processes consuming excessive memory.")

    # Network-specific analysis
    elif metric_type == "network":
        interface = parts[0]  # Get the interface name (e.g., eth0, lo)
        rxkB = values.get("rxkB/s", 0)
        txkB = values.get("txkB/s", 0)
        rxdrop = values.get("rxdrop", 0)
        txdrop = values.get("txdrop", 0)
        rxerrs = values.get("rxerrs", 0)
        txerrs = values.get("txerrs", 0)

        if rxdrop > thresholds["rxdrop"] or txdrop > thresholds["txdrop"]:
            hints.append(f"Packet drops detected on {interface}. Investigate network hardware or configuration.")

        if rxerrs > thresholds["rxerrs"] or txerrs > thresholds["txerrs"]:
            hints.append(f"Packet errors detected on {interface}. Check for issues with network interface or driver.")

        if rxkB > thresholds["rxkB/s"]:
            hints.append(f"High receive throughput detected on {interface}: {rxkB} kB/s. Ensure network bandwidth is sufficient.")

        if txkB > thresholds["txkB/s"]:
            hints.append(f"High transmit throughput detected on {interface}: {txkB} kB/s. Ensure network bandwidth is sufficient.")

    if hints:
        return "\n".join(hints)
    return None


def filter_sar_output(output, metric, thresholds, verbose=False):
    """Filters SAR output based on a specific metric and threshold."""
    lines = output.splitlines()
    header = None
    problematic_lines = []

    for line in lines:
        if "Average" in line or "Media" in line:
            continue
        if any(name in line.lower() for name in COLUMN_NAMES[metric]):
            header = line
            break

    if not header:
        print(f"Header for '{metric}' not found.")
        return [], None

    for line in lines:
        if line.startswith("Average") or line.startswith("Media"):
            continue
        parts = line.split()
        if len(parts) < len(header.split()):
            continue  # Skip lines that do not match header format
        try:
            detailed_analysis = analyze_metrics(parts, header, thresholds, metric, verbose)
            if detailed_analysis:
                problematic_lines.append((line, detailed_analysis))

        except ValueError as e:
            if verbose:
                print(f"Error processing line: {e}")
            continue

    return problematic_lines, header


def generate_report(problematic_lines, header, metric):
    """Generates a report for problematic lines in the SAR output."""
    if not problematic_lines:
        print("No performance issues detected.")
        return

    print("\nPerformance Issues Report:")
    for line, detailed_analysis in problematic_lines:
        print(f"\nAnalyzing issue in line:\n{header}\n{line}")
        print(f"\nDetailed Analysis: {detailed_analysis}")

    print("\nEnd of report.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SAR Data Processor")
    parser.add_argument("-f", "--file", required=True, help="Path to SAR binary file")
    parser.add_argument("-m", "--metric", required=True, choices=["disk", "cpu", "memory", "network"], help="Metric to analyze")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    metric = args.metric
    output = run_sar_command(args.file, METRIC_OPTIONS[metric])
    if output:
        problematic_lines, header = filter_sar_output(output, metric, DEFAULT_THRESHOLDS[metric], args.verbose)
        generate_report(problematic_lines, header, metric)
