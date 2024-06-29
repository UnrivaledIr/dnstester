import json
import subprocess
import time
import matplotlib.pyplot as plt
import sys
import platform

# Define the DNS servers to test
dns_servers = [
    "google (8.8.8.8):8.8.8.8",
    "google (8.8.4.4):8.8.4.4",
    "cloudflare (1.1.1.1):1.1.1.1",
    "cloudflare (1.0.0.1):1.0.0.1",
    "opendns (208.67.222.222):208.67.222.222",
    "opendns (208.67.220.220):208.67.220.220",
    "comodo (8.26.56.26):8.26.56.26",
    "comodo (8.20.247.20):8.20.247.20"
]


# Define the domains to test
domains = [
    "unrivaled.ir",
    "gnu.org"
]

# Create the JSON output file
output_file = "dns_test_results.json"

# Initialize the JSON output
with open(output_file, "w") as f:
    f.write("[]")

# Function to clear the DNS cache
def clear_dns_cache():
    system = platform.system()
    if system == "Windows":
        subprocess.run(["ipconfig", "/flushdns"], check=True)
    elif system == "Darwin":  # macOS
        subprocess.run(["dscacheutil", "-flushcache"], check=True)
    elif system == "Linux":
        subprocess.run(["sudo", "systemctl", "restart", "systemd-resolved"], check=True)
    else:
        print(f"Unsupported operating system: {system}")

# Check if the "--clear" switch is provided
if "--clear" in sys.argv:
    clear_dns_cache()
    print("DNS cache cleared.")
else:
    print("Running without clearing DNS cache.")

# Loop through the domains and test the DNS servers
for domain in domains:
    # Initialize the domain's JSON object
    domain_json = {"domain": domain, "dns_result": []}

    # Loop through the DNS servers and test the domain
    for dns_server in dns_servers:
        # Extract the DNS server name and IP
        dns_name, dns_ip = dns_server.split(":")

        # Resolve the domain using the DNS server
        start_time = time.time()
        resolved_ip = subprocess.check_output(["dig", "+short", "@" + dns_ip, domain]).decode().strip()
        end_time = time.time()
        query_time = f"{(end_time - start_time) * 1000:.6f}ms"

        # Add the DNS server's result to the domain's JSON object
        domain_json["dns_result"].append({
            "dns_name": dns_name,
            "dns_ip": dns_ip,
            "resolved_ip": resolved_ip,
            "query_time": query_time
        })

    # Append the domain's JSON object to the output file
    with open(output_file, "r") as f:
        data = json.load(f)
    data.append(domain_json)
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)

# Function to find the DNS server with the lowest query time for a domain
def find_fastest_dns(domain):
    with open(output_file, "r") as f:
        data = json.load(f)

    for domain_data in data:
        if domain_data["domain"] == domain:
            fastest_dns = min(domain_data["dns_result"], key=lambda x: float(x["query_time"][:-2]))
            lowset_dns = max(domain_data["dns_result"], key=lambda x: float(x["query_time"][:-2]))
            # Reset: \033[0m
            # Green: \033[92m
            # Red: \033[91m
            # Yellow: \033[93m
            # Blue: \033[94m
            # Magenta: \033[95m
            # Cyan: \033[96m
            print(f"########################################")
            print(f"# \033[94mFastest\033[0m DNS for \033[93m{domain}\033[0m: {fastest_dns['dns_name']} ({fastest_dns['resolved_ip']}, \033[92m{fastest_dns['query_time']}\033[0m)")
            print(f"# \033[94mLowest\033[0m DNS for \033[93m{domain}\033[0m: {lowset_dns['dns_name']} ({lowset_dns['resolved_ip']}, \033[91m{lowset_dns['query_time']}\033[0m)")
            print(f"########################################")
            break

# Function to plot the DNS server query times for each domain
def plot_dns_query_times():
    with open(output_file, "r") as f:
        data = json.load(f)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title("DNS Server Query Times")
    ax.set_xlabel("Domain")
    ax.set_ylabel("Query Time (ms)")

    for domain_data in data:
        domain = domain_data["domain"]
        dns_names = [result["dns_name"] for result in domain_data["dns_result"]]
        query_times = [float(result["query_time"][:-2]) for result in domain_data["dns_result"]]

        # Get the maximum number of DNS servers for any domain
        max_dns_servers = max(len(domain_data["dns_result"]) for domain_data in data)

        # Adjust the x-axis tick labels to accommodate the variable number of DNS servers
        # x_labels = [f"{domain} - {dns_names[i]}" for i in range(max_dns_servers)]
        x_labels = [f"{domain}" for i in range(max_dns_servers)]
        x_pos = [i for i in range(max_dns_servers)]

        # Plot the bars for the current domain
        for i in range(len(dns_names)):
            ax.bar(x_pos[i], query_times[i], label=dns_names[i])

        ax.set_xticks(x_pos)
        ax.set_xticklabels(x_labels, rotation=90)
        ax.legend()

    plt.show()


# Check if the "--graph" switch is provided
if "--graph" in sys.argv:
    plot_dns_query_times()
else:
    for domain in domains:
        find_fastest_dns(domain)
