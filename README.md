# DISTRIBUTED LOAD TESTING USING KAFKA	
1) Developed a distributed load testing system using Kafka to facilitate communication between orchestrator and driver nodes, using Tsunami and Avalanche testing.

2) Designed and implemented modules for orchestrator, driver, and target server, incorporating heartbeat monitoring,  request handling, and performance metrics collection using Flask and Kafka.


## Prerequisites

Ensure that you have the following installed on your system:
- [Kafka](https://kafka.apache.org/downloads)
- Python 3.x


## How to Run the System

### 1. Start Kafka

To start Kafka, use the following command:

```bash


Start kafka using sudo systemctl start kafka

Run our intermediate Kafka Node using python3 kafka_intermediate.py

Now we can run our driver node on terminal using python3 driver.py

Note : We can run multiple driver nodes by running this code on multiple terminal instances which will act as individual processes.
We can now run our Orchestrator node using python3 orch.py

You will now be presented with 4 options:

1.Avalanche Testing

2.Tsunami Testing

3.Node Data

4.Exit

/metrics -> which will show the total number of requests and responses made to the server

/ping -> returns a "pong" message to show server is active
