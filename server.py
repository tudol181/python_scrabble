import socket
import threading
import time

def handle_client(client_socket, connected_clients, client_usernames):
    try:
        username = client_socket.recv(1024).decode('utf-8')  # Receive username
        if username:
            client_usernames.append(username)
            connected_clients.append(client_socket)
            print(f"{username} has connected.")
    except (BrokenPipeError, ConnectionResetError):
        pass

def broadcast_status(connected_clients, client_usernames, remaining_time):
    user_list = ', '.join(client_usernames)
    message = f"{remaining_time} seconds left. Connected clients: {len(connected_clients)} ({user_list})"
    for client_socket in connected_clients:
        try:
            client_socket.send(message.encode('utf-8'))
        except (BrokenPipeError, ConnectionResetError):
            connected_clients.remove(client_socket)

def start_server():
    host = '127.0.0.1'
    port = 12345
    max_clients = 4
    min_clients = 2
    wait_time = 20

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(max_clients)

    print(f"Server started on {host}:{port}. Waiting for clients...")

    connected_clients = []
    client_usernames = []
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        remaining_time = max(0, wait_time - int(elapsed_time))

        #accept max 4 and check time
        if remaining_time > 0 and len(connected_clients) < max_clients:
            server_socket.settimeout(1)
            try:
                client_socket, _ = server_socket.accept()
                thread = threading.Thread(
                    target=handle_client,
                    args=(client_socket, connected_clients, client_usernames)
                )
                thread.start()
            except socket.timeout:
                pass

        #get status
        broadcast_status(connected_clients, client_usernames, remaining_time)

        if remaining_time <= 0:
            break

        time.sleep(1)

    #decide if to start
    if len(connected_clients) < min_clients:
        message = "Not enough players."
    else:
        message = "Start"

    for client_socket in connected_clients:
        try:
            client_socket.send(message.encode('utf-8'))
        except:
            pass
        client_socket.close()

    server_socket.close()
    print("Server has shut down.")

if __name__ == "__main__":
    start_server()
