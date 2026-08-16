
import socket

def check_port(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

if check_port(11434):
    print("Ollama service is likely running.")
else:
    print("Ollama service is likely down.")
