# DISTRIBUTED LOAD TESTING USING KAFKA	
1) Developed a distributed load testing system using Kafka to facilitate communication between orchestrator and driver nodes, using Tsunami and Avalanche testing.

2) Designed and implemented modules for orchestrator, driver, and target server, incorporating heartbeat monitoring,  request handling, and performance metrics collection using Flask and Kafka.


## Prerequisites

Ensure that you have the following installed on your system:
- [Kafka](https://kafka.apache.org/downloads)
- Python 3.x

![image](https://github.com/user-attachments/assets/59e079f9-7b97-4e27-ae76-8f282bbe4abc)

## How to Run the System
# Step 1: Start Kafka and Zookeeper
sudo systemctl start kafka
sudo systemctl start zookeeper

# Step 2: Run Target Server
python3 target_server.py

# Step 3: Run Orchestrator Node
python3 orchestrator.py

# Step 4: Run Driver Nodes (in multiple terminals)
python3 driver.py
python3 driver.py  # (Additional driver node, in a new terminal)
python3 driver.py  # (Additional driver node, in a new terminal)


