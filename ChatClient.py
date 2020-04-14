import socket
import threading
import sys
import time

flag = True

ip = '127.0.0.1'
port = 5000

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def user_action():
    global flag
    user_act = input("Please type JOIN to join the Chatroom : ")
    if user_act.lower() == "join":
        flag = True
        server_connection(client_socket)
    # else:
    #     if user_act.lower() == "exit":
    #         client_socket.close()
    #         sys.exit(0)
    else:
        return user_action()


def server_connection(client_socket):
    global flag
    try:
        client_socket.connect((ip, port))
    except Exception as e:
        print(f"Failed to connect to server because: {e}")
    threading.Thread(target=get_client_response, args=(client_socket, (ip, port))).start()
    while True:
        try:
            if flag == False:
                print("Test break")
                break
            client_response = client_socket.recv(1024)
            if client_response.decode().lower() != "one":
                print(client_response.decode())
        except:
            client_socket.close()
            break
    # print("Hogaya connection")
    sys.exit(0)


def get_client_response(client_conn, addr):
    global flag
    # with client_conn:
    while True:
        try:
            if flag == False:
                break
            else:
                user_chat = input()
                client_conn.sendall(user_chat.encode())
                if user_chat.lower() == "leave":
                    flag = False
                    sys.exit(0)
        except:
            client_conn.close()


user_action()

