import network
import socket
from time import sleep
import machine
from  creds import *



header="HTTP/1.1 200 OK\nServer: Pico W\nContent-Type: application/json\n\n"


def connect():
    #Connect to WLAN
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    for tries in range(10):
        if wlan.isconnected() == False:
            print('Waiting for connection...')
            sleep(1)
    if wlan.isconnected() == False:
        print("Failed to connect to WiFi")
        exit(1)
    print(wlan.ifconfig())
    ip = wlan.ifconfig()[0]
    print(f'Connected on {ip}')
    return ip
   
def open_socket(ip):
    # Open a socket
    address = (ip, 80)
    connection = socket.socket()
    connection.bind(address)
    connection.listen(1)
    return connection

def serve(connection, msg_maker):
    while True:
        client = connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        client.send(msg_maker)
        client.close()

def msg_build():
    body = str({"temp": 99})
    response = header + body
    
    print("Response: "+response)
    return response
    
    
try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection, msg_build)

except KeyboardInterrupt:
    machine.reset()

    
    
    

