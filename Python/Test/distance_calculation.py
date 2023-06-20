import time

def update_position(position, velocity, acceleration, time_delta):
    # Update the position components
    position[0] += velocity[0]*time_delta + 0.5*acceleration[0]*time_delta**2
    position[1] += velocity[1]*time_delta + 0.5*acceleration[1]*time_delta**2
    position[2] += velocity[2]*time_delta + 0.5*acceleration[2]*time_delta**2

    return position

# Example initial values
initial_position = [0, 0, 0]
velocity = [0, 0, 0]
acceleration = [0, 0, 0]

# Start time
start_time = time.time()

while True:
    # Calculate the elapsed time
    current_time = time.time()
    elapsed_time = current_time - start_time

    # Update the position
    position = update_position(initial_position, velocity, acceleration, elapsed_time)

    # Print the location
    print("Time:", elapsed_time)
    print("Position (x, y, z):", position)
    print()

    # Wait for a small interval (e.g., 1 second) before the next iteration
    time.sleep(1)
