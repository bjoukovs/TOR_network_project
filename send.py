import socket
 
UDP_IP = "localhost"
UDP_PORT = 9001
MESSAGE = "Hello, World!"

print("TCP target IP:", UDP_IP)
print ("TCP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock = socket.socket(socket.AF_INET, # Internet
                      socket.SOCK_STREAM) # UDP
sock.connect((UDP_IP,UDP_PORT))
sock.sendall(MESSAGE.encode())
print("message sent")
sock.close()
