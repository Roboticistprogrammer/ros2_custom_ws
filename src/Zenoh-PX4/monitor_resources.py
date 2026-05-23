import psutil
import time
import csv
import sys

# Define the process names we want to track depending on the test
# For DDS run: ['MicroXRCEAgent']
# For Zenoh run: ['rmw_zenohd']
TARGET_PROCESSES = sys.argv[1:] 

if not TARGET_PROCESSES:
    print("Usage: python3 monitor_resources.py <process_name1> <process_name2>")
    sys.exit(1)

output_file = f"metrics_{'_'.join(TARGET_PROCESSES)}.csv"

print(f"Monitoring targets: {TARGET_PROCESSES}. Writing to {output_file}...")

with open(output_file, mode='w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["Timestamp", "Process", "CPU_Percent", "Memory_MB"])

    start_time = time.time()
    
    # Run the monitor for a fixed duration (e.g., 60 seconds)
    while time.time() - start_time < 60:
        elapsed = time.time() - start_time
        
        for proc in psutil.process_iter(['name', 'cpu_percent', 'memory_info']):
            try:
                if proc.info['name'] in TARGET_PROCESSES:
                    cpu = proc.cpu_percent(interval=None)
                    # Convert bytes to Megabytes
                    ram = proc.info['memory_info'].rss / (1024 * 1024) 
                    
                    writer.writerow([round(elapsed, 2), proc.info['name'], cpu, round(ram, 2)])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
                
        time.sleep(0.1) # 10Hz sampling

print("Monitoring complete.")

