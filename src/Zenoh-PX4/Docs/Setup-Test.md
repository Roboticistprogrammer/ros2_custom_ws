# Test if Zenoh works

## Terminate ROS 2 daemon started with another RMW
```bash
pkill -9 -f ros && ros2 daemon stop
```
Without this step, ROS 2 CLI commands (e.g. `ros2 node list`) may
not work properly since they would query ROS graph information from the ROS 2 daemon that
may have been started with different a RMW.

### Start the Zenoh router
> [!NOTE]
> Manually launching Zenoh router won't be necessary in the future.
```bash
# terminal 1
ros2 run rmw_zenoh_cpp rmw_zenohd
```
> [!NOTE]
> Without the Zenoh router, nodes will not be able to discover each other since multicast discovery is disabled by default in the node's session config. Instead, nodes will receive discovery information about other peers via the Zenoh router's gossip functionality. 

### Run the `talker`
```bash
# terminal 2
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
ros2 run demo_nodes_cpp talker
```

### Run the `listener`
```bash
# terminal 2
export RMW_IMPLEMENTATION=rmw_zenoh_cpp
ros2 run demo_nodes_cpp listener
```
The listener node should start receiving messages over the `/chatter` topic.

