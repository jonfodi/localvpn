import socket

SRC_IP = "10.100.0.10"
DST_IP = "10.142.0.2"
DST_PORT = 12345  # replace with an open port on the GCP VM

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# This is the critical line — same idea as `ping -S`
s.bind((SRC_IP, 0))   # 0 = ephemeral source port

s.connect((DST_IP, DST_PORT))

s.sendall(b"hello over ipsec\n")
data = s.recv(1024)

print("received:", data)
s.close()
