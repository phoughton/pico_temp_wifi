from time import sleep
import socket
import network
import machine
from  creds import password, ssid


HEADER="HTTP/1.1 200 OK\nServer: Pico W\nContent-Type: application/json\n\n"


def connect():
    """
    Connect to WLAN
    """

    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    for _ in range(10):
        if wlan.isconnected() is False:
            print('Waiting for connection...')
            sleep(1)
    if wlan.isconnected() is False:
        print("Failed to connect to WiFi")
        exit(1)
    print(wlan.ifconfig())
    ip_address = wlan.ifconfig()[0]
    print(f'Connected on {ip_address}')
    return ip_address

def open_socket(ip_address):
    """
    Open a socket
    """
    address = (ip_address, 80)
    socket_connection = socket.socket()
    socket_connection.bind(address)
    socket_connection.listen(1)
    return socket_connection

def serve(socket_connection, msg_maker):
    """
    Start serving
    """
    while True:
        client = socket_connection.accept()[0]
        request = client.recv(1024)
        request = str(request)
        print(request)
        client.send(msg_maker)
        client.close()

def msg_build():
    """
    Create response message
    """
    body = str({"temp": 99})
    response = HEADER + body

    print("Response: "+response)
    return response


try:
    ip = connect()
    connection = open_socket(ip)
    serve(connection, msg_build)

except KeyboardInterrupt:
    machine.reset()

