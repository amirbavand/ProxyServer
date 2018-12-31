import socket


host=socket.gethostbyname(socket.gethostname())
control_port=11344
data_port=11345

controllsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controllsocket.connect((host,control_port))
datasocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datasocket.connect((host,data_port))
path='c_files/'
a="False"
while True:

    while a=="False":
        username=input("enter username\n")
        password=input("enter password\n")
        str="LOGIN"+" "+username+" "+password
        controllsocket.send(str.encode())
        print("yes")
        ack=controllsocket.recv(1024).decode()
        a=ack

    inp=input("enter command")

    controllsocket.send(inp.encode())

    sp=inp.split()

    if(sp[0]=="RMD"):
        print(controllsocket.recv(1024).decode())

    elif(sp[0]=="DELE"):
        print(controllsocket.recv(1024).decode())

    elif(sp[0]=="LIST"):
        print(controllsocket.recv(1024).decode())
        print(datasocket.recv(2048).decode())
    elif(sp[0]=="RETR"):

        size=controllsocket.recv(1024).decode()
        if(size=="you have not permition"):
            print("you have not permition")
        else:
            size=(int)(size)
            data=datasocket.recv(size)
            file = open(path+sp[1], 'wb+')
            file.write(data)
            print("file downloaded successfully!")





    else:
        print("worng command")


















#s=socket.socket()
#host=socket.gethostbyname(socket.gethostname())

#port=12344

#s.connect((host,port))

#print(s.recv(1024))

#s.close()











