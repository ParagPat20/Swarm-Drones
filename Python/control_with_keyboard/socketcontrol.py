import socket
import struct
from PIL import Image
import io

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('oxitech.local', 8000))  # Replace with your Raspberry Pi's IP address

connection = client_socket.makefile('rb')

try:
    while True:
        # Read the image size from the server
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]

        # Read the image data from the server
        image_data = connection.read(image_len)

        # Convert the image data to a Pillow image
        image = Image.open(io.BytesIO(image_data))

        # Display the image
        image.show()

except KeyboardInterrupt:
    pass

finally:
    connection.close()
    client_socket.close()
