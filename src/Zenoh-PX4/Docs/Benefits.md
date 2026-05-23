# Advantages of using Zenoh

the absence of the Micro-XRCE-DDS Agent is a massive advantage. In traditional PX4-ROS 2 setups, the agent acts as a heavy "middleman." It receives custom serialized data from the flight controller, translates it into DDS packets, and broadcasts it. By embedding Zenoh natively inside PX4, you have eliminated an entire layer of software architecture. This slashes translation latency, removes a single point of failure, and cuts CPU/RAM usage on your companion computer. For example if you flood the network with variety of packaets from vision,communication etc still rc control and other modules can connect instantly.

Zenoh's superiority is network discovery traffic, reconnection speed, and Wi-Fi reliability. 
While standard DDS (like CycloneDDS or FastDDS) is excellent on wired LANs, it often struggles with the "discovery storms" and connection timeouts common in drone operations.