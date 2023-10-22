import socket
import struct
import cv2
import numpy as np
import time

# Create a socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('oxitech2.local', 8000))  # Replace with your Raspberry Pi's IP address

connection = client_socket.makefile('rb')

# Define a function to detect and classify color balls
def detect_and_classify_color_balls(frame):
    """Detects and classifies color balls in the given frame.

    Args:
        frame: A numpy array representing the image frame.

    Returns:
        A list of dictionaries, where each dictionary contains the (x, y) coordinates of the center of the detected ball, its radius, and its color.
    """
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges for Red, Yellow, Blue, and Green balls (you can adjust these ranges)
    color_ranges = [
        (np.array([0, 100, 100]), np.array([10, 255, 255]), "Red"),
        (np.array([20, 100, 100]), np.array([30, 255, 255]), "Yellow"),
        (np.array([90, 100, 100]), np.array([130, 255, 255]), "Blue"),
        (np.array([35, 100, 100]), np.array([85, 255, 255]), "Green"),
    ]

    balls = []

    for color_range in color_ranges:
        lower, upper, color_name = color_range
        mask = cv2.inRange(hsv, lower, upper)

        # Find contours in the mask image
        contours = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[0]

        for c in contours:
            # Filter out small contours
            if cv2.contourArea(c) > 100:
                # Fit a circle to the contour
                (x, y), radius = cv2.minEnclosingCircle(c)
                center = (int(x), int(y))

                # Calculate the distance from the center of the frame in both x and y directions
                x_distance = center[0] - frame.shape[1] / 2
                y_distance = center[1] - frame.shape[0] / 2

                balls.append({"center": center, "radius": int(radius), "color": color_name, "x_distance": x_distance, "y_distance": y_distance})

    return balls

try:
    while True:
        # Read the image size from the server
        image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]

        # Read the image data from the server
        image_data = connection.read(image_len)

        # Convert the image data to a numpy array and decode it
        image = np.frombuffer(image_data, dtype=np.uint8)
        frame = cv2.imdecode(image, 1)

        # Detect and classify color balls in the frame
        balls = detect_and_classify_color_balls(frame)

        if balls:
            # Select the ball with the shortest distance from the center
            closest_ball = min(balls, key=lambda ball: abs(ball["x_distance"]) + abs(ball["y_distance"]))

            center, radius, color, x_distance, y_distance = closest_ball["center"], closest_ball["radius"], closest_ball["color"], closest_ball["x_distance"], closest_ball["y_distance"]

            # Annotate the selected ball with its color and distance
            print(f"Selected Ball: {color} (X: {int(x_distance)}, Y: {int(y_distance)})")

            # Suggest camera movements to center the selected ball
            if abs(x_distance) > 20:
                if x_distance < 0:
                    print("Move the camera to the Left")
                else:
                    print("Move the camera to the Right")
            if abs(y_distance) > 20:
                if y_distance < 0:
                    print("Move the camera down")
                else:
                    print("Move the camera up")


except Exception as e:
    print("Error:", e)

finally:
    connection.close()
    client_socket.close()
