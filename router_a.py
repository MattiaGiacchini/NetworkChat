from datetime import datetime
import socket
import time
from threading import Thread

# creating basic arp table for IP and MAC addresses
ip_arp_table = {}
mac_arp_table = {}

# dictionary of all the available clients
available_clients = {1: "175.55.40.7", 2: "175.55.40.8", 3: "175.55.40.9", 4: "120.32.24.2", 5: "120.32.24.3", 6: "120.32.24.4"}

# router mac address
router_mac = "E7:3B:E0:A1:11:59"  # to change

# socket for communication with server
router_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
router_in_ip = "118.25.10.5"  # to change

# socket for communication with clients
router_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
router_out_ip = "175.55.40.1"  # to change

# binding sockets
router_in.bind(("localhost", 20_100))  # 30_100
router_out.bind(("localhost", 20_200))  # 30_200

# Server port
server = ("localhost", 15_000)
server_ip = "118.25.10.0"

# connecting to the server
router_in.connect(server)

# enabling connections
router_out.listen()


# a simple function to unpack message
def get_message(message):
    source_mac = message[0:17]
    source_ip = message[17:28]
    destination_ip = message[28:39]
    destination_mac = message[39:56]
    message = message[56:]
    return source_mac, source_ip, destination_mac, destination_ip, message


def accept():
    while True:
        if len(ip_arp_table) < 3:
            # accept the client
            client, address = router_out.accept()
            connect_message = client.recv(2048).decode("utf-8")

            # insert the client in the arp tables
            ip_arp_table[connect_message[17:28]] = client
            mac_arp_table[connect_message[17:28]] = connect_message[0:17]

            # notify the server of a new connection
            print(router_mac + router_in_ip + server_ip + connect_message[17:28] + "IN")
            router_in.send(bytes(router_mac + router_in_ip + server_ip + connect_message[17:28] + "IN", "utf-8"))


def message_routing(original_message):
    source_mac, source_ip, destination_mac, destination_ip, message = get_message(original_message)

    # notify the server of a lost connection
    if message.casefold() == "quit":
        del ip_arp_table[source_ip]
        del mac_arp_table[source_ip]

        print(router_mac + router_in_ip + server_ip + source_mac + "OUT")
        router_in.send(bytes(router_mac + router_in_ip + server_ip + source_mac + "OUT", "utf-8"))
        return

    else:
        print(str(datetime.now()) + "Message sent by: " + source_ip + ":\n\t" + message)

    # checking that the destination ip is internal to the current router
    if destination_ip in ip_arp_table:
        ip_arp_table[destination_ip].send(bytes(original_message, "utf-8"))

    # check if the destination should be internal to the router net
    elif destination_ip[0:10] == router_out_ip[0:10]:
        router_in.send(bytes(router_mac + router_in_ip + source_ip + source_mac + "L'utente " +
                             destination_ip + " non è online al momento", "utf-8"))

    else:
        router_in.send(bytes(router_mac + router_in_ip + source_ip + source_mac + message, "utf-8"))


def receive_messages_a1():
    while True:
        if available_clients[1] in ip_arp_table.keys():
            message = ip_arp_table[available_clients[1]].recv(2048).decode("utf-8")
            print(message)
            message_routing(message)


def receive_messages_a2():
    while True:
        if available_clients[2] in ip_arp_table.keys():
            message = ip_arp_table[available_clients[2]].recv(2048).decode("utf-8")
            print(message)
            message_routing(message)


def receive_messages_a3():
    while True:
        if available_clients[3] in ip_arp_table.keys():
            message = ip_arp_table[available_clients[3]].recv(2048).decode("utf-8")
            print(message)
            message_routing(message)


# launching all the functions as thread
if __name__ == '__main__':
    thread_start = Thread(target=accept)
    thread_a1 = Thread(target=receive_messages_a1)
    thread_a2 = Thread(target=receive_messages_a2)
    thread_a3 = Thread(target=receive_messages_a3)

    thread_start.start()
    thread_a1.start()
    thread_a2.start()
    thread_a3.start()
