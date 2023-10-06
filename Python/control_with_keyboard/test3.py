from dronekit import connect

# Connect to the drone
d1 = connect('tcp:127.0.0.1:5762')


# Close the vehicle object before exiting
print("Close vehicle object")
d1.close()
