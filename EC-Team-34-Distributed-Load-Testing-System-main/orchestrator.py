from flask import Flask, jsonify, request, render_template

from kafka import KafkaProducer, KafkaConsumer

import json

import uuid

import time

import threading

from threading import Lock





app = Flask(__name__)



# Kafka configurations

bootstrap_servers = 'localhost:9092'



# Kafka topics

register_topic = 'register'

test_config_topic = 'test_config'

trigger_topic = 'trigger'

heartbeat_topic = 'heartbeat'

metrics_topic = 'metrics'





global_metrics = {

    "metrics": {

        "mean_latency": 0,

        "median_latency": 0,

        "min_latency": 0,

        "max_latency": 0

    }

}

heartbeat_data = {}

active_nodes = set()



metrics_lock = Lock()





def send_test_configuration(producer, test_id,test_type, test_message_delay, message_count_per_driver):

    test_config_msg = {

        "test_id": test_id,  # Replace with unique test ID

        "test_type": test_type,  # Replace with actual test type

        "test_message_delay": test_message_delay,  # Replace with actual delay value

        "message_count_per_driver": message_count_per_driver  # Replace with actual message count

    }

    producer.send(test_config_topic, json.dumps(test_config_msg).encode('utf-8'))

    

   





def display_statistics():

    

    consumer = KafkaConsumer(

        metrics_topic,

        bootstrap_servers=bootstrap_servers,

        group_id='metrics_group',

        value_deserializer=lambda x: json.loads(x.decode('utf-8'))

    )

    

    metrics_data = []  # To accumulate the received metrics

    for message in consumer:

        register_data = message.value

        metrics_lock.acquire()

        try:

            global_metrics["metrics"]["mean_latency"] = register_data["metrics"]["mean_latency"]

            global_metrics["metrics"]["median_latency"] = register_data["metrics"]["median_latency"] 

            global_metrics["metrics"]["min_latency"] = register_data["metrics"]["min_latency"]

            global_metrics["metrics"]["max_latency"] = register_data["metrics"]["max_latency"] 

        finally:

            # Release the lock after updating global_metrics

            metrics_lock.release() 

        print("Revieced data new", global_metrics)

    



def display_heart():

    global heartbeat_data, active_nodes

    consumer = KafkaConsumer(

        heartbeat_topic,

        bootstrap_servers=bootstrap_servers,

        group_id='metrics_group',

        value_deserializer=lambda x: json.loads(x.decode('utf-8'))

    )

    while True:

        for message in consumer:

            node_id = message.value.get("node_id")

            heartbeat_timestamp = message.value.get("timestamp")



            # Store the data in the global dictionary

            heartbeat_data[node_id] = heartbeat_timestamp

            active_nodes.add(node_id)

    

def check_inactive_nodes():

    global active_nodes



    while True:

        current_time = datetime.now()

        inactive_nodes = [node_id for node_id, timestamp_str in heartbeat_data.items() if timestamp_str and (

            current_time - datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S")

        ).total_seconds() > 10]

        for node_id in inactive_nodes:

            active_nodes.discard(node_id)

        time.sleep(1)  # Check for inactive nodes every 5 seconds



def start_check_inactive_nodes():

    thread = threading.Thread(target=check_inactive_nodes)

    thread.daemon = True

    thread.start()







def start_heart():

    thread2 = threading.Thread(target=display_heart)

    thread2.daemon = True

    thread2.start()   





@app.route('/heart', methods=['GET'])

def view_node_heart():

    start_heart()

    start_check_inactive_nodes()

    node_heart_data = [{"node_id": node_id, "heartbeat": timestamp} for node_id, timestamp in heartbeat_data.items()]

    return render_template('heartbeat.html', node_heart_data=node_heart_data)





@app.route('/trigger-test', methods=['GET', 'POST'])

def trigger_test():

    

    if request.method == 'POST':

        test_id = str(uuid.uuid4())  # Generate a unique test ID here

        test_type = request.form['test_type']

        test_message_delay = int(request.form['test_message_delay'])

        message_count_per_driver = int(request.form['message_count_per_driver'])

        

        producer = KafkaProducer(bootstrap_servers=bootstrap_servers)

        send_test_configuration(

            producer,

            test_id,  # Pass the generated test_id here

            test_type,

            test_message_delay,

            message_count_per_driver  # Set a default message count or take it as input as well

        )



        trigger_msg = {

            "test_id": test_id,

            "trigger": "YES"

        }



        producer.send(trigger_topic, json.dumps(trigger_msg).encode('utf-8'))



        



    return render_template('index.html')



def start_display_statistics():

    thread = threading.Thread(target=display_statistics)

    thread.daemon = True

    thread.start()   

    

@app.route('/test-statistics', methods=['GET'])

def test_statistics():

    start_display_statistics()

    metrics_lock.acquire()

    try:

        metrics = global_metrics.copy()

    finally:

        # Release the lock after accessing global_metrics

        metrics_lock.release()

    

    return render_template('test_statistics.html', global_metrics=metrics)







@app.route('/', methods=['GET'])

def main():

    return '''

    <div style="margin: 20px; border: 2px solid black; padding: 20px;">

    <h1 style="text-align: center;">Distributed Load Testing System</h1>

    <h3 style="text-align: center; margin-bottom: 200px;">Big Data Project 2023 @ PES University</h3>

    <div style="display: flex; justify-content: center; gap: 20px;">

        <form action="/test-statistics">

            <input type="submit" value="View Test Statistics">

        </form>

        <form action="/trigger-test">

            <input type="submit" value="Trigger Test">

        </form>

        <form action="/heart">

            <input type="submit" value="HeartBeat ">

        </form>

    </div>

</div>



    '''

    consumer2= KafkaConsumer(

        register_topic,

        bootstrap_servers=bootstrap_servers,

        group_id='metrics_group',

        value_deserializer=lambda x: json.loads(x.decode('utf-8'))

    )

    for message in consumer2:

    	register_data=message.value

    	print("REcived Registration message", register_data)

    



if __name__ == '__main__':

    app.run(debug=True, port=8000)  # Run the Flask app	

    main()

