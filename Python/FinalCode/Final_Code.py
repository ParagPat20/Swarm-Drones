from my_vehicle import MyVehicle
from functions import *

mcu_address = '127.0.0.0:'
cd_address = '0.0.0.0:14550'
sd_address = '0.0.0.0:14660'
link = "192.168.4.2"
link_port = 8888

connectall(mcu_address,cd_address,sd_address,link,link_port)

# data_thread = threading.Thread(target=send_chout, args=(CD, arduino_ip, arduino_port))
# # Start the thread
# data_thread.start()







ch1out, ch2out, ch3out, ch4out = vehicle.chout()
