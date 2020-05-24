from datetime import datetime
import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 15_000))
server.listen()

# server info
server_ip = "118.25.10.0"
server_mac = "71:25:83:05:5A:5B"

# routers info
router_a_ip = "118.25.10.5"
router_a_mac = "D3:A0:0D:59:F5:36"

router_b_ip = "118.25.10.9"
router_b_mac = "45:1D:B0:04:0A:5E"

# socket passed from socket.accept function to communicate with routers
router_a = None
router_b = None


# set delimiter for new information in current time
with open("connectionLog.txt", "a") as connection_log:
    time = str(datetime.now())
    connection_log.write("\n\n\n\n\n"
                         "====================================\n"
                         "==\t" + time + "\t ==\n"
                         "====================================\n\n")
connection_log.close()


# function to write connections or send message to router
def manage_message(original_message, router):
    print(original_message)
    current_time = str(datetime.now())

    # check if is a login or logout message, else send message to destination
    if original_message[50:52] == "IN":
        with open("connectionLog.txt", "a") as connection_log:
            connection_log.write(
                f"{current_time}" + "\t" + original_message[39:50] + " has connected to the server\n")
            print(current_time + "\t" + original_message[39:50] + " has connected to the server")
    elif original_message[56:59] == "OUT":
        with open("connectionLog.txt", "a") as connection_log:
            connection_log.write(
                current_time + "\t" + original_message[28:39] + " has disconnected from the server\n")
            print(current_time + "\t" + original_message[28:39] + " has disconnected from the server")
    else:
        router.send(bytes(original_message, "utf-8"))


# management of the router A message receiving
def router_a_management():
    while True:
        original_message = router_a.recv(2048).decode("utf-8")
        if len(original_message) > 0:
            manage_message(original_message, router_b)


# management of the router B message receiving
def router_b_management():
    while True:
        original_message = router_b.recv(2048).decode("utf-8")
        if len(original_message) > 0:
            manage_message(original_message, router_a)


if __name__ == '__main__':

    thread_router_a = Thread(target=router_a_management)
    thread_router_b = Thread(target=router_b_management)


while router_a is None or router_b is None:
    router_connection, address = server.accept()

    if router_a is None:
        router_a = router_connection
        thread_router_a.start()

    elif router_b is None:
        router_b = router_connection
        thread_router_b.start()
