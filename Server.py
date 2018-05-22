import socket
import random
import select
import sys

def within (value, goal, num):
    dif = abs(value - goal) 
    if dif == 0:
        return "Correct"

    elif dif < num:
        return True
    
    else:
        return False


##Connection

ConnList = []
TCP_IP = '127.0.0.1'

## svsC = SerVer Socket Client, binds to port: 4000

svsC = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
svsC.bind((TCP_IP , 4000))
svsC.listen(5)

## svsA = SerVer Socket Admin, binds to port: 4001

svsA = socket.socket(socket.AF_INET,socket.SOCK_STREAM) 
svsA.bind((TCP_IP , 4001))
svsA.listen(5)

print('\n\n Waiting...connection...')
print("Server IP: " + TCP_IP)

ConnList = [svsC , svsA]
Clist = []; ##Clist = Client List
rn = []; ##rn = Random Number
num = 3

while True:
    
    (SockRead , SockWrite , SockError) = select.select(ConnList , ConnList , ConnList)
    
    for Sock in SockRead:
           
##Connection to new Client

        if Sock == svsC:
            (conn , a) = svsC.accept()
            ConnList.append(conn)
            print(conn)
            print("Client (%s, %s) connected" % a)
            Clist.append(a);
            print(Clist)
            rn.append(random.randrange(0,31))
            print(rn)
            
##print("Received connection from", a)

            try:
                dt = conn.recv(80).decode() ## dt = data
            except OSError as msg:
                dt = None
                continue
            
##print(dt)

            if dt == "Hello\r\n":
                conn.send("Greetings\r\n".encode())
            else:
                print ('<<Hello\\r\\n>> is not matched!!..adopting the connection for <<'+ conn.getpeername()[0] + '>>')
                del ConnList[ConnList.index(conn)]
                del rn[Clist.index(conn.getpeername())]
                del Clist[Clist.index(conn.getpeername())]
                conn.close()
                continue
            try:
                dt = conn.recv(80).decode()
            except OSError as msg:
                dt = None
                continue

            if dt == "Game\r\n":
                conn.send("Ready\r\n".encode())
            else:
                print ('<<Game\\r\\n>> is not matched!!..adopting the connection for <<'+ conn.getpeername()[0] + '>>')
                del ConnList[ConnList.index(conn)]
                del rn[ConnList.index(conn.getpeername())]
                del Clist[Clist.index(conn.getpeername())]
                conn.close()
                continue

            
##Connection to ADMIN

        elif Sock == svsA:
            (conn,a) = svsA.accept()
            try:
                dt = conn.recv(80).decode()
            except OSError as msg:
                dt = None
                continue
            
 ##print(dt)

            if dt == "Hello\r\n":
                conn.send("Admin-Greetings\r\n".encode())
                try:
                    dt = conn.recv(80).decode()
                except OSError as msg:
                    print('Time out!!')
                    print('Connection for <<' + conn.getpeername()[0] +'>> has been dropped') 
                    continue
                
##print(dt)

                if dt == "Who\r\n":
                    conn.send(("%d"%len(Clist)+'\r\n').encode())
                    if (len(Clist)==0):
                        conn.send('No Player in the list!!\r\n'.encode())
                    else:
                        for i in range(0,len(Clist)):
                            adrr = "%s %s\r\n" % Clist[i] 
                            conn.send(adrr.encode())
                else:
                    print ('<<Who\\r\\n>> is not matched!!..adopting the connection for <<'+ conn.getpeername()[0] + '>>')
                    conn.close()
                    continue
            conn.close()

            
##Proccessing to the Game

        else:
            try:
                xx = Sock.recv(80).decode()
                
            except OSError as msg:
                print('Connection for <<' + Sock.getpeername()[0] +'>> has been dropped')
                del ConnList[ConnList.index(Sock)]
                del rn[Clist.index(Sock.getpeername())]
                del Clist[Clist.index(Sock.getpeername())]
                Sock.close()
                continue
            
            if (xx[0:13]=='My Guess is: ' and xx[len(xx)-2:]=='\r\n'):
                try:
                    res = within (int(xx[12:len(xx)-2]), rn[Clist.index(Sock.getpeername())], num)
                except:
                    print ('Wrong guessing number format!!!')
                    print ('Connection for <<' + Sock.getpeername()[0] +'>> has been dropped')
                    del ConnList[ConnList.index(Sock)]
                    del rn[Clist.index(Sock.getpeername())]
                    del Clist[Clist.index(Sock.getpeername())]
                    Sock.close()

##print(Clist)

                if res == True:
                    away = "Close\r\n"
                    Sock.send(away.encode())
                elif res == False:
                    Sock.send("Far\r\n".encode())
                elif res == "Correct":
                    correct = "Correct\r\n" 
                    Sock.send(correct.encode())
                    del ConnList[ConnList.index(Sock)]
                    del rn[Clist.index(Sock.getpeername())]
                    del Clist[Clist.index(Sock.getpeername())]
                    Sock.close()
            else:
                print('User guess number format is wrong!!')
                del ConnList[ConnList.index(Sock)]
                del rn[Clist.index(Sock.getpeername())]
                del Clist[Clist.index(Sock.getpeername())]
                Sock.close()
                continue
