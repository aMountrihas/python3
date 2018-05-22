import socket
import sys
import errno

#Define socket,ip, buffer size from admin side

s_ip_address= '127.0.0.1'       
s_port = 4001                
bSize = 80                

#In case of an error

def Error():          
    adminSocket.close()          
    sys.exit()

def players(conn):                     
   try:
       data = conn.recv(bSize).decode()     
   except socket.error as e:                      
       if e.errno == errno.ECONNRESET:            
           print("Error in data transmission!")
           return ''
   return data.strip()                         

             
def dImport(conn):                    
   try:
       data = conn.recv(bSize).decode()     
   except socket.error as e:                     
       if e.errno == errno.ECONNRESET:          
           print("Error in data transmission!")
           Error()                           
   return data.strip()                            

def dExport(sock , text):                  
  try:
      tmp = str(text) + '\r\n'
      sock.send(tmp.encode())                  
  except socket.error as e:                  
      if e.errno == errno.ECONNRESET:          
          print("Error in data transmission!")
          Error() 
                       
#opening socket     
  
try:       
   adminSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)  
except socket.error:
    print("Unable to open socket")                        
    sys.exit()
    
#Connecting to the server

try:
    adminSocket.connect((s_ip_address, s_port))    
except socket.error:
    print("Failed to connect")                   
    sys.exit()
    
dExport(adminSocket , "Hello")                   
      
data = dImport(adminSocket)                   
if data != "Greetings":                  
     print("Error in data transmission")         
     Error()

dExport(adminSocket , "Who")    

lines = []

while True:
    data = players(adminSocket)
    if len(data) == 0:
        break
    lines.append(data)

print("The players currently connected are:") 

if len(lines) == 0:
    print("0")
else:
    for player in lines:
        print(str(player))

adminSocket.close()
sys.exit()                                    




