import pandas as pd
import matplotlib.pyplot as plt

# Load the generated benchmark data
try:
    dds_data = pd.read_csv("metrics_MicroXRCEAgent.csv")
    zenoh_data = pd.read_csv("metrics_rmw_zenohd.csv")
except FileNotFoundError:
    print("Please run both benchmark scripts first to generate the CSV files.")
    exit()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

# Plot CPU Comparisons
ax1.plot(dds_data['Timestamp'], dds_data['CPU_Percent'], label='XRCE Agent (DDS Bridge)', color='red')
ax1.plot(zenoh_data['Timestamp'], zenoh_data['CPU_Percent'], label='rmw_zenohd (Zenoh Router)', color='blue')
ax1.set_title('Middleware CPU Usage Over Time')
ax1.set_xlabel('Seconds')
ax1.set_ylabel('CPU %')
ax1.grid(True)
ax1.legend()

# Plot Memory Comparisons
ax2.plot(dds_data['Timestamp'], dds_data['Memory_MB'], label='XRCE Agent (DDS Bridge)', color='red')
ax2.plot(zenoh_data['Timestamp'], zenoh_data['Memory_MB'], label='rmw_zenohd (Zenoh Router)', color='blue')
ax2.set_title('Middleware Memory Footprint')
ax2.set_xlabel('Seconds')
ax2.set_ylabel('RAM (MB)')
ax2.grid(True)
ax2.legend()

plt.tight_layout()
plt.savefig('zenoh_vs_dds_efficiency.png')
plt.show()

