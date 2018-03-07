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
    ERROR logs of the service will be written to "/var/log/counter-service-error.log"

Example:
        POST -> http://localhost:8443/counter -> Return: "Increment counter by 1"
        GET -> http://localhost:8443/counter -> Return: "POST Counter result: 6"

"""
import os
import logging
from flask import Flask

app = Flask(__name__)
service_error_log_file = "/var/log/counter-service-error.log"
logging.basicConfig(filename=service_error_log_file, level=logging.DEBUG)
count = 0  # this will be used for the first time only
hostname_or_ip = ""  # hostname or ip address for reaching to host
port_number = 8443  # port number that the service will be listening on
host_partition = "/counter"  # the folder name for sending and receiving POST and GET requests
service_path = "/var/lib/jenkins/workspace/Micro_Service_Post_Counter/service/counter-service.log"


"""
'def read_file' method read and return the post requests number from counter-service.log
"""
def read_file():
    counter = open(service_path, "r")
    count_r = int(counter.read().split(" ")[-1])
    return count_r

"""
'def write_file' method write the incremention by 1 every post request to counter-service.log
"""
def write_file(count):
    counter_file = open(service_path, "w")
    counter_file.write("Increment counter by " + str(count))
    counter_file.close()


"""
next if checking if the counter-service.log file exists for continue the counting process
"""
if os.path.isfile(service_path):
    count = read_file()
else:
    write_file(count)


"""
next if checking if the file counter-service-error.log exists for serive error logs and creates this file if not
"""
if os.path.isfile(service_error_log_file) == False:
    error_logs = open(service_error_log_file, "w")
    error_log.close()

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

@app.route(host_partition, methods=['POST'])
def post_counter():
    increment_counter()
    return "Increment counter by 1"


"""
'def get_counter' method displays the number of post requests from the counter-service.log
"""

@app.route(host_partition, methods=['GET'])
def get_counter():
    count_r = read_file()
    return "POST Counter result: %d" % count_r


if __name__ == "__main__":
    try:
        app.run(debug=True, host=hostname_or_ip, port=port_number)

    except Exception as e:
        if 'getaddrinfo failed' in e:
            print("ERROR: Please input a valid IP address or Hostname")
        else:
            print(e)
