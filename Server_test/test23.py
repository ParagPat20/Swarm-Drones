import server
import time
import threading
from server import start_server

server_thread = threading.Thread(target=start_server)
server_thread.start()
# Sending messages to the server
server.send("hello")
server.send("Ok, it's working")
time.sleep(5)
server.send("Waited and refreshed")
