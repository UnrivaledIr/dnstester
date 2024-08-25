# DNS Benchmarking Script
==========================

A Python script to benchmark the performance of different DNS servers base on your network setting. so you can determine which dns server is best for you!

## Overview

This script tests the query time of multiple DNS servers for a list of specified domains. It uses the `dig` command to resolve the domains and measures the time taken for each query. The results are stored in a JSON file and can be used to compare the performance of different DNS servers.

## Features

* Tests multiple DNS servers for a list of specified domains
* Measures the query time for each DNS server
* Stores results in a JSON file
* Can clear the DNS cache before running the tests
* Can plot the query times for each domain using matplotlib

## Usage

### Running the Script

1. Clone the repository and navigate to the directory.
2. Install the required dependencies: `matplotlib` and `json`.
3. Edit the `dns_servers` and `domains` lists in the script to specify the DNS servers and domains you want to test.
4. Run the script using `python main.py`.
5. Use the `--clear` switch to clear the DNS cache before running the tests.
6. Use the `--graph` switch to plot the query times for each domain.

### Example Output

The script will output the fastest and slowest DNS servers for each domain, along with the query time. For example:
Running without clearing DNS cache.
```
########################################
# Fastest DNS for unrivaled.ir: google (8.8.4.4) (116.202.96.103, 122.762680ms)
# Lowest DNS for unrivaled.ir: opendns (208.67.222.222) (116.202.96.103, 644.473553ms)
########################################
########################################
# Fastest DNS for gnu.org: google (8.8.8.8) (209.51.188.116, 113.784313ms)
# Lowest DNS for gnu.org: cloudflare (1.1.1.1) (209.51.188.116, 366.569519ms)
########################################
```
If you use the `--graph` switch, the script will display a bar chart showing the query times for each DNS server for each domain.

### Example Run

To run the script and plot the query times, use the following command:
`python dns_benchmark.py --graph`

To run the script with both options, use the following command:
`python dns_benchmark.py --clear --graph`

### Requirements

- Python 3.x
- `matplotlib` library
- `json` library
- `dig` command (usually installed by default on Linux and macOS systems)

### License
This project is licensed under the **GNU General Public License**, version 3.0 (**GPL-3.0**). See the [LICENSE](LICENSE) file for details.
