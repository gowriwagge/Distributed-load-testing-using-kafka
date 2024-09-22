from flask import Flask, jsonify

app = Flask(__name__)

# Counter for requests received
request_counter = 0
response_counter = 0

@app.route('/ping')
def ping():
    global request_counter
    request_counter += 1
    return 'Server is alive'

@app.route('/metrics')
def metrics():
    global request_counter, response_counter
    return jsonify({
        'requests_received': request_counter,
        'responses_sent': response_counter
    })

if __name__ == '__main__':
    app.run(debug=True)
