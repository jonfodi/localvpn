import socket

SRC_IP = "10.100.0.10"
DST_IP = "10.142.0.2"
DST_PORT = 12345

print("creating socket")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("socket created, binding")
s.bind((SRC_IP, 0))  # ephemeral source port

# BEFORE connect: local IP known, port assigned
local_ip, local_port = s.getsockname()
print(f"local (pre-connect): {local_ip}:{local_port}")

print("bound, connecting")
s.connect((DST_IP, DST_PORT))

# AFTER connect: full 4-tuple established
local_ip, local_port = s.getsockname()
remote_ip, remote_port = s.getpeername()

print(f"local:  {local_ip}:{local_port}")
print(f"remote: {remote_ip}:{remote_port}")

print("connected, sending")
s.sendall(b"hello over ipsec\n")

data = s.recv(1024)
print("received:", data)

s.close()
