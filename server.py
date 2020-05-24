from datetime import datetime
import socket
from threading import Thread

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 15_000))
server.listen()

# server info
server_ip = "118.25.10.0"
server_mac = "51:75:03:31:6E:AF"

# routers info
router_a_ip = "118.25.10.5"
router_a_mac = "E7:3B:E0:A1:11:59"

router_b_ip = "118.25.10.9"
router_b_mac = "21:E8:12:BD:B1:43"

router_a = None
router_b = None

while router_a is None:  # or router_b is None:
    router_connection, address = server.accept()

    if router_a is None:
        router_a = router_connection
    elif router_b is None:
        router_b = router_connection


# reset the connection file log
with open("connectionLog.txt", "w") as connection_log:
    connection_log.write("")
connection_log.close()


# management of the router A message receiving
def router_a_management():
    while True:
        original_message = router_a.recv(2048).decode("utf-8")

        # check if is a login or logout message, else send message to destination
        current_time = str(datetime.now())
        print(original_message)

        if original_message[50:52] == "IN":
            with open("connectionLog.txt", "a") as connection_log:
                connection_log.write(
                    f"{current_time}" + "\t" + original_message[39:50] + " has connected to the server\n")
                print(current_time + "\t" + original_message[39:50] + " has connected to the server\n")
        elif original_message[56:59] == "OUT":
            with open("connectionLog.txt", "a") as connection_log:
                connection_log.write(
                    current_time + "\t" + {original_message[28:39]} + " has disconnected from the server")
                print(current_time + "\t" + original_message[28:39] + " has disconnected from the server\n")
        else:
            pass
            #router_b.send(bytes(original_message, "utf-8"))


# management of the router B message receiving
def router_b_management():
    while True:
        original_message = router_b.recv(2048).decode("utf-8")

        # check if is a login or logout message, else send message to destination
        current_time = datetime.now()
        print(original_message)

        if original_message[50:52] == "IN":
            with open("connectionLog.txt", "a") as connection_log:
                connection_log.write(
                    f"{current_time}" + "\t" + original_message[39:50] + " has connected to the server\n")
                print(current_time + "\t" + original_message[39:50] + " has connected to the server\n")
        elif original_message[56:59] == "OUT":
            with open("connectionLog.txt", "a") as connection_log:
                connection_log.write(current_time + "\t" + {original_message[28:39]} + " has disconnected from the server")
                print(current_time + "\t" + original_message[28:39] + " has disconnected from the server\n")
        else:
            router_a.send(bytes(original_message, "utf-8"))

if __name__ == '__main__':
    thread_router_a = Thread(target=router_a_management)
    #thread_router_b = Thread(target=router_b_management)

    thread_router_a.start()
    #thread_router_b.start()