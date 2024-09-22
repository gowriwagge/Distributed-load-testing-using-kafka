from kafka import KafkaProducer, KafkaConsumer

from collections import defaultdict

import json

import time

import uuid

import requests

import sys

import threading

from datetime import datetime





ip_address = sys.argv[1]



# Kafka configurations

bootstrap_servers = 'localhost:9092'



# Kafka topics

register_topic = 'register'

test_config_topic = 'test_config'

trigger_topic = 'trigger'

heartbeat_topic = 'heartbeat'

metrics_topic = 'metrics'



global_latencies = defaultdict(list)



driver_id = str(uuid.uuid4())



def register_driver(producer):

    register_msg = {

        "node_id": driver_id,

        "node_IP": "192.168.0.1",  # Replace with actual IP

        "message_type": "DRIVER_NODE_REGISTER"

    }

    producer.send(register_topic, json.dumps(register_msg).encode('utf-8'))



def send_requests():

    print("In send_requests")



    # Assuming the variables are already defined: test_config_topic, bootstrap_servers

    consumer1 = KafkaConsumer(

        test_config_topic,

        bootstrap_servers=bootstrap_servers,

        group_id='test_details_group',

        value_deserializer=lambda x: json.loads(x.decode('utf-8'))

    )



    for message1 in consumer1:

        test_config1 = message1.value



        if test_config1['test_type'] == 'AVALANCHE':

            print("Avalanche")

            count = test_config1['message_count_per_driver']

            ping_endpoint = '/ping'

            target_server = f'http://{ip_address}'

            

            for i in range(count):

                start_time = time.time()

                response = requests.get(target_server + ping_endpoint)

                end_time = time.time()

                append_latencies(start_time, end_time)



                if response.status_code == 200:

                    print('Ping successful!')

                else:

                    print('Failed to ping the server.')



        if test_config1['test_type'] == 'TSUNAMI':

            print("Tsunami")

            count = test_config1['message_count_per_driver']

            interval = test_config1['test_message_delay']

            ping_endpoint = '/ping'

            target_server = f'http://{ip_address}'

            

            for i in range(count):

                start_time = time.time()

                response = requests.get(target_server + ping_endpoint)

                end_time = time.time()

                append_latencies(start_time, end_time)



                if response.status_code == 200:

                    print('Ping successful!')

                else:

                    print('Failed to ping the server.')

                    

                time.sleep(interval)

                

        calculate_metrics(test_config1['test_id'])



 



def append_latencies(start_time,end_time):

    latency = end_time - start_time

    global global_latencies

    global_latencies['all_latencies'].append(latency)

    

    

def calculate_metrics(test_id):

    latencies = global_latencies['all_latencies']



    if latencies:

        max_latency = max(latencies)

        min_latency = min(latencies)

        mean_latency = sum(latencies) / len(latencies)

        median_latency = sorted(latencies)[len(latencies) // 2]



        node_id = str(uuid.uuid4())

        report_id = str(uuid.uuid4())



        metrics_msg = {

            "node_id": node_id,

            "test_id": test_id,

            "report_id": report_id,

            "metrics": {

                "mean_latency": mean_latency,

                "median_latency": median_latency,

                "min_latency": min_latency,

                "max_latency": max_latency

            }

        }

        print(metrics_msg)

        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

        producer.send(metrics_topic, json.dumps(metrics_msg).encode('utf-8'))



        





def publish_heartbeat(producer):

    while True:

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        heartbeat_msg = {

            "node_id": driver_id,

            "heartbeat": "YES",

            "timestamp": current_time

        }

        producer.send(heartbeat_topic, json.dumps(heartbeat_msg).encode('utf-8'))

        time.sleep(5) 



def main():

    producer = KafkaProducer(bootstrap_servers=bootstrap_servers)



    register_driver(producer)

    heartbeat_producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

    heartbeat_thread = threading.Thread(target=publish_heartbeat, args=(heartbeat_producer,))

    heartbeat_thread.daemon = True

    heartbeat_thread.start()

    

    consumer = KafkaConsumer(

        trigger_topic,

        bootstrap_servers=bootstrap_servers,

        group_id='test_group',

        value_deserializer=lambda x: json.loads(x.decode('utf-8'))

    )



    for message in consumer:

        test_config = message.value

        if test_config['trigger'] == 'YES':

            print("Trigger Message recieved")

            send_requests()







if __name__ == '__main__':

    main()
