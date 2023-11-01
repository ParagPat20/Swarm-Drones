import socket
import struct
import cv2
import numpy as np

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.12.122', 8888))  # Replace with your Raspberry Pi's IP address

connection = client_socket.makefile('rb')

try:
    while True:
        # Read the image size from the server
        image_len_data = connection.read(struct.calcsize('<L'))
        if not image_len_data:
            break  # Break the loop if no image data is received
        image_len = struct.unpack('<L', image_len_data)[0]

        # Read the image data from the server
        image_data = connection.read(image_len)

        # Convert the image data to a NumPy array
        image_array = np.frombuffer(image_data, dtype=np.uint8)

        # Decode the image as a color image (you may need to adjust the format)
        if image_array.size > 0:
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
            cv2.imshow('Video Stream', image)

        # Press 'q' to quit the video stream
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

except KeyboardInterrupt:
    pass

except Exception as e:
    print(e)

