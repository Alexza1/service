"""
Prerequisites:
    pip install flask

Description:
    counter-service is a nano-service that counting the number of post requests to localhost in port 8443.
    this service will be started by jenkins job in systemd("/etc/systemd/system/counter.service") folder.
    restart the service only when the service process does not exit cleanly(on-failure).
    this service is about to create a log file in the service_path to keep the requests number,
    and if the service will fail or restarted, it will continue the counting from the last time that the service was up
    and running.

"""
import os
from flask import Flask

app = Flask(__name__)
count = 0  # this will be used for the first time only
service_path = "/var/lib/jenkins/workspace/Micro_Service_Post_Counter/service/counter-service.log"


def read_file():
    counter = open(service_path, "r")
    count_r = int(counter.read().split(" ")[-1])
    return count_r


def write_file(count):
    counter_file = open(service_path, "w")
    counter_file.write("Increment counter by " + str(count))
    counter_file.close()


"""  
next if checking if the counter-service.log file exists for continue the counting process 
"""
if os.path.isfile(service_path):
    read_file()
else:
    write_file(count)

""" 
'def increment_counter' is incrementing the count value by 1 
"""

def increment_counter():
    global count
    count = count + 1
    write_file(count)


""" 
'post_counter' method increment by 1 for each post request by using the 'def increment_counter'
"""

@app.route('/counter', methods=['POST'])
def post_counter():
    increment_counter()
    return "Increment counter by 1"


"""
'get_counter' method displays the number of post requests from the counter-service.log
"""

@app.route('/counter', methods=['GET'])
def get_counter():
    count_r = read_file()
    return "POST Counter result: %d" % count_r


if __name__ == "__main__":
    try:
        port_number = 8443  # port number that the service will be listening on
        app.run(debug=True, host="", port=port_number)

    except Exception as e:
        if 'getaddrinfo failed' in e:
            print("ERROR: Please input a valid IP address or Hostname")
        else:
            print(e)
