import socket
import time
import sys
from threading import Thread

client_ip = "175.55.40.7"
client_mac = "2A:11:C4:AD:FF:C2"

router = ("localhost", 20_200)
router_mac = "E7:3B:E0:A1:11:59"

# creating client socket
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# binding the socket to a port
client.bind(("localhost", 20_001))

# connecting the socket to the router
client.connect(router)

# saying the router that the client is connected. It will communicate the event to the server
client.send(bytes(client_mac + client_ip, "utf-8"))

# dictionary of all the available clients
available_clients = {1: "175.55.40.7", 2: "175.55.40.8", 3: "175.55.40.9", 4: "120.32.24.2", 5: "120.32.24.3", 6: "120.32.24.4"}
received_message = ""


# a simple function to unpack the message
def get_message(source_message):
    source_mac = source_message[0:17]
    source_ip = source_message[17:28]
    destination_ip = source_message[28:39]
    destination_mac = source_message[39:56]
    source_message = source_message[56:]
    return source_mac, source_ip, destination_mac, destination_ip, source_message


# function threaded to receive messages constantly
def receive():
    while True:
        try:
            original_message = client.recv(2048).decode("utf8")
            print("\n\nMessage received from: " + original_message[34:45] + "\n\t >>> " + original_message[56:])
        except socket.error as error:
            print(error)
            break


def send():
    while True:
        print("\nScegli l'IP a cui inviare il messaggio inserendo il numero corrispondente: ")
        destination_ip = int(input("1. \t 175.55.40.7\n"
                                   "2. \t 175.55.40.8\n"
                                   "3. \t 175.55.40.9\n"
                                   "4. \t 120.32.24.2\n"
                                   "5. \t 120.32.24.3\n"
                                   "6. \t 120.32.24.4\n"
                                   ">>> "))

        if 0 < destination_ip < 7:
            message = input("\nScrivi il tuo messaggio oppure scrivi QUIT se vuoi uscire:\n >>> ")

            # sending the message to the router
            client.send(bytes(client_mac + client_ip + available_clients[destination_ip] + router_mac + message, "utf-8"))

            # client.send(bytes(available_clients[destination_ip], "utf-8"))
            if message.casefold() == "quit":
                client.close()
                sys.exit()
                break
        else:
            print("IP non valido, inserisci un numero compreso tra 1 e 6")


Thread(target=receive).start()
Thread(target=send).start()
