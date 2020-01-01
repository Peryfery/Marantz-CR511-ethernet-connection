import sys
import socket
import os
import time

# checking ping whether TV is ON or OFF
def check_ping(tvIP):
    # definition of global variable in called function
    global tvOff

    # ping command for Windows
    response = os.system("ping " + tvIP + " -n 1")

    # checking disconnection with this counter
    if (response == 1 and tvOff < 10):
        tvOff += 1

    # when TV is OFF
    elif (tvOff >= 10):
        tvOff = 10

    # when TV is ON
    elif (response == 0 and tvOff < 10):
        tvOff = 0

    return response, tvOff

# connection to Marantz and send turn ON command
def marantz_turn_on(amplifierIP):
    # Create a TCP/IP socket
    marantzConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Set IP and port - where to connect
    serverAddress = (amplifierIP, 23)
    print('***starting up on %s port %s ***' % serverAddress)
    marantzConnection.settimeout(5.0)

    try:
        # connecting to Marantz
        marantzConnection.connect(serverAddress)

        # Send data to Marantz
        message = b"PWSTANDBY\r"
        print('sending "%s"' % message)
        marantzConnection.sendall(message)

        # response check
        receivedData = 0
        expectedData = len(message)
        while receivedData < expectedData:
            data = marantzConnection.recv(16)
            receivedData += len(data)
            print('received "%s"' % data)

    # error exception
    except socket.error as err:
        print(err, "***Impossible to connect, please check your connection or IP address***")

    # closing connection even error occured
    finally:
        print('***Connection closed, bad motherfucker***')
        marantzConnection.close()

    return


if __name__ == '__main__':
    tvOff = 0

    # infinity loop
    while True:
        # calling ping function
        networkResult = check_ping("192.168.0.10")

        if (networkResult[0] == 0):
            print("***TV is ON")

            if(tvOff == 10): # turning ON amplifier when TV is turned ON
                marantz_turn_on("192.168.0.102")
                print("***Turning on receiver...")
                tvOff = 0
                time.sleep(15)

        else:
            print("***TV is OFF or disconnected from your network.")

        # wait for 2 seconds
        time.sleep(2)