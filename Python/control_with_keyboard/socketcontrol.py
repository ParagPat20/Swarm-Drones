import socket
import struct
import cv2
import numpy as np

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

        # Convert the image data to a numpy array and decode it
        image = np.frombuffer(image_data, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)

        # Display the video feed on the laptop
        cv2.imshow('Video Feed', frame)
        cv2.waitKey(1)

finally:
    connection.close()
    client_socket.close()
