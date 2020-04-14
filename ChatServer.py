import socket
import threading


ip = '127.0.0.1'
port = 5000
# print_lock = threading.Lock()
# while True:
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_list = {}
exit_flag = False
port_thread ={}


def close_server(socket_server,):
    global exit_flag
    msg = input()
    while exit_flag == True:
        break
    if msg.lower() == "exit":
        socket_server.close()
        exit_flag = True
    else:
        print("Incorrect command")


def new_client_connection(client_conn, address):
    # try:
        user_name = "USER"+str(address[1])
        client_conn.sendall("Welcome to the chatroom!".encode())
        print(f"{user_name} has joined the chat")
        if len(client_list) > 1:
            for client in client_list.keys():
                if client != client_conn:
                    client.sendall(f"{user_name} has joined the chat".encode())
        while True:
            message = client_conn.recv(1024)
            if message:
                if message.decode().lower() == "leave":
                    client_conn.close()
                    del client_list[client_conn]
                    break
                print(f'{user_name}: {message.decode()}')
                if len(client_list) > 1:
                    for client in client_list.keys():
                        if client != client_conn:
                            client.sendall(f"{user_name}: {message.decode()}".encode())
                else:
                    for client in client_list.keys():
                        if client == client_conn:
                            client.sendall("ONE".encode())
            else:
                del client_list[client_conn]
                client_conn.close()
                break

        print(f"{user_name} has left the chat")
        for client in client_list.keys():
            client.sendall(f"{user_name} has left the chat".encode())
    # except:
    #     print("except new_client_connection")
    #     client_conn.close()


# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    server_socket.bind((ip, port))
    server_socket.listen(10)
    print(f"Listening on {ip}:{port}")  # embed expressions
except Exception as e:
    print(f"Failed to bind on {ip}:{port} because: {e}")
while True:
    try:
        client_socket, addr = server_socket.accept()
        client_list[client_socket] = addr
        t1 = threading.Thread(target=new_client_connection, args=(client_socket, addr))
        port_thread[addr[1]] = t1
        t1.start()
        # threading.Thread(target=close_server, args=(server_socket,)).start()
    except Exception as e:
        print(e)
#     client_list.append(client_socket)
#     client_addr_list.append(addr)
#     print(i)
#     i = i+1

# print(client_list)
# print(client_addr_list)
print("Server has stopped accepting connections")