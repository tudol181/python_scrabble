import socket
import pygame
import threading

def receive_updates(client_socket, status):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message == "Start" or message == "Not enough players.":
                status["final_message"] = message
                break
            # Parse server updates
            time_left, clients_info = message.split(" seconds left. Connected clients: ")
            clients_connected, usernames = clients_info.split(" (")
            usernames = usernames.rstrip(")")
            status["time_left"] = int(time_left)
            status["clients_connected"] = int(clients_connected)
            status["usernames"] = usernames
        except:
            break

def start_client():
    host = '127.0.0.1'
    port = 12345

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 400))
    pygame.display.set_caption("Enter Username")
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    # Text input variables
    input_active = True
    username = ""
    input_box = pygame.Rect(150, 150, 300, 50)
    color_inactive = pygame.Color('gray')
    color_active = pygame.Color('white')
    color = color_inactive

    while input_active:
        screen.fill((30, 30, 30))
        text = font.render("Enter your username:", True, (255, 255, 255))
        screen.blit(text, (150, 100))

        # Draw input box
        color = color_active if username else color_inactive
        pygame.draw.rect(screen, color, input_box, 2)
        txt_surface = font.render(username, True, color)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        input_box.w = max(300, txt_surface.get_width() + 10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Submit username on Enter key
                    if username.strip():  # Ensure the username is not empty
                        input_active = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]  # Remove the last character
                else:
                    username += event.unicode  # Append the typed character

        pygame.display.flip()
        clock.tick(30)

    # Connect to the server
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    # Send the username to the server
    client_socket.send(username.encode('utf-8'))

    # Shared status
    status = {"time_left": 10, "clients_connected": 0, "usernames": "", "final_message": None}

    # Start a thread to receive server updates
    threading.Thread(target=receive_updates, args=(client_socket, status), daemon=True).start()

    # Main game interface
    pygame.display.set_caption("Waiting for Game Start")
    running = True

    while running:
        screen.fill((30, 30, 30))

        # Display messages
        time_text = font.render(f"Time left: {status['time_left']}s", True, (255, 255, 255))
        clients_text = font.render(f"Connected clients: {status['clients_connected']}", True, (255, 255, 255))
        usernames_text = font.render(f"Players: {status['usernames']}", True, (255, 255, 255))
        screen.blit(time_text, (100, 100))
        screen.blit(clients_text, (100, 180))
        screen.blit(usernames_text, (100, 260))

        # Final message (if available)
        if status["final_message"]:
            final_message_text = font.render(status["final_message"], True, (255, 0, 0))
            screen.blit(final_message_text, (100, 300))
            pygame.display.flip()
            pygame.time.delay(3000)  # Display for 3 seconds
            running = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    client_socket.close()

if __name__ == "__main__":
    start_client()
