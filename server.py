import socket
import threading
import os
filename = "new.txt" 
def RetrFile(name, sock):
    sock.send("This is a Text File\n \n")
    with open(filename, 'rb') as f:
        bytesToSend = f.read(1024)
        sock.send(bytesToSend)
        while bytesToSend != "":
            bytesToSend = f.read(1024)
            sock.send(bytesToSend)
            
    
    
    sock.close()

def main():
    host = '127.0.0.1'
    port = 5000

    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print "Server Started."
    while True:
        c, addr = s.accept()
        data = c.recv(1024)
        print "client connected from ip: <" + str(addr) +">"
        print(data)
        t = threading.Thread(target=RetrFile, args=("retrThread", c))
        t.start()
    s.close()

if __name__ =='__main__':

    main()
             
