# following will not cresh if module flask doesn't exists. it will install it from the execption
# and the import of the module will be defined just after this block
import os

flaska = 0
if flaska == 0: 
    try:
        from flask import Flask
        flaska = 1
    except:
        os.system("pip install flask")
        flaska = 0
else:
    pass

from flask import Flask
app = Flask(__name__)
count = 0

def increment_counter():
    global count
    count = count + 1


# post method and increment by one for each post request
@app.route('/counter', methods=['POST'])
def post_counter():
    increment_counter() #"incremented counter by 1"
    return


# get method display the number of post requests 
@app.route('/counter', methods=['GET'])
def get_counter():
    return "POST Counter result: %d" % count


if __name__ == "__main__":
    try:
        host_name = "10.100.102.215"
        port_number = 443
        app.run(debug=True, host=host_name, port=port_number)

    except Exception as e:
        if 'getaddrinfo failed' in e:
            print("ERROR: Please input a valid IP address or Hostname")
        else:
            print(e)
