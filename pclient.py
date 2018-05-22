import socket

cls = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

##cls = CLient Socket

cls.connect(("127.0.0.1", 4001))

#Connects to the Localhost server, port:4001

print ('\n Connect to:', "127.0.0.1,4001")

cls.send("Hello".encode()) 

#sending message to the server (TCP 3 way handshake)

respond = cls.recv(90).decode() #receiveing Respond from server 
print(respond)
msg = input('Type "Game" if you wish to play the game: \r\n')

#sends message expecting the client to press "Enter" in order to play the game.

cls.send(msg.encode())
print(cls.recv(90).decode())

while True:
    gnum = input("Please enter your guess: \r\n") #gnum = Guessing Number
    cls.send(gnum.encode())
    svmsg = cls.recv(90).decode()
    print(svmsg)
    if svmsg == ("Your guess is right! \r\n"):
        break
    
cls.close()
