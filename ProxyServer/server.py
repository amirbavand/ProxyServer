from threading import Thread
import os,socket
import re
import ipaddress
import glob
import shutil
import datetime



ceit = socket.gethostbyname('ceit.aut.ac.ir')
path = 'files/'


class Ftp_server(Thread):

    def  __init__(self,control_conn,data_conn,ip,port):
        Thread.__init__(self)

        print("dlkf;sjldsg")
        self.control_conn=control_conn
        self.data_conn=data_conn
        self.secrot=False

   #     now=datetime.datetime.now()

        log= open('logs.txt', 'a+')
        log.write("client "+ ip+str(port)+" connected at "+datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
 + "\n")
        log.close()






    def run(self):
        a=False
        while(a==False):
         #   s=self.control_conn.split()
            s=control_conn.recv(1024).decode().split()

            if(s[1]=="root" and s[2]=="root"):
                control_conn.send("True".encode())
                a=True
            elif(s[1]=="admin" and s[2]=="admin"):
                control_conn.send("True".encode())
                a = True
                self.secrot=True


            else:
                control_conn.send("False".encode())




        while True:

            s=control_conn.recv(1024).decode().split()
            if(s[0]=="RMD"):
                self.RMD()
            elif(s[0]=="DELE"):
                self.DELE(s[1])
            elif(s[0]=="LIST"):
                self.LISTFILE()
            elif(s[0]=="RETR"):
                self.RETR(s[1])









        #    self.lis("dsf")
    #    self.download_from_ceit("flower.jpeg")
    #    self.RETR("lab.pptx")
     #   self.RMD()


    def LISTFILE(self):
        requ = "GET /~94131090/CN1_Project_Files/ HTTP/1.1\r\nHost: " + host + "\r\n\r\n"
        s_socket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s_socket.getsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s_socket.connect((ceit,80))
        s_socket.send(requ.encode())
        result=self.recvall(s_socket).decode()

        if(result[9:12]=='200'):
            regex=re.compile("<a.*>(.*)</a>")
            rose = regex.findall(result)
            sended_msg = ""
            for ros in rose:
                if (ros != "Description" and ros != "Parent Directory"):
                    sended_msg = sended_msg + str(ros) + "\r\n"
            self.control_conn.send("List Of Files Are Sending!".encode())
            self.data_conn.send(sended_msg.encode())
        else:
            print("THIS REQUEST IS WRONG")




    def recvall(self,sock):
        total_data = bytes()
        while True:
            data = sock.recv(1024)
            if not data: break
            total_data = total_data + data
            print("is downloading")
        return total_data




    def RETR(self,filename):
        if(filename[0:6]=="secret"):
            if(self.secrot==False):

                self.control_conn.send("you have not permition".encode())

                return


        fn=os.path.join(path,filename)
        if(not os.path.isfile(fn)):
            print("in file vojood nadarad")
            self.download_from_ceit(filename)
        else:
            print("in file vojjod darad")

        file=open(path+filename, 'rb')
        data=file.read()
        self.control_conn.send(str(len(data)).encode())
        self.data_conn.send(data)







    def download_from_ceit(self,file_name):

        file_name=file_name.replace(" ","%20")
        request = "GET /~94131090/CN1_Project_Files/" + str(file_name) + " HTTP/1.1\r\nHost: " + ceit + "\r\n\r\n"
        w_socket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        w_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        w_socket.connect((ceit,80))
        w_socket.send(request.encode())
        result=self.recvall(w_socket)
      # if(result[10:12]=='200'):
        hb = re.compile(b'\r\n\r\n')

        junk = (hb.split(result, 1))
        data = junk[1]
        file_name = file_name.replace('%20', ' ')
        file=open(path+str(file_name), 'wb+')

        file.write(data)
        log = open('logs.txt', 'a+')
        log.write("proxi download " + file_name+ datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                  + "\n")
        log.close()

        return True
     #   else:
      #      print("vojood nadarad")
       #     return False





    def DELE(self,filename):
        file_path = os.path.join(path, filename)
        if (os.path.isfile(file_path)):
            os.remove(file_path)
            self.control_conn.send("done".encode())
        else:
            self.control_conn.send("this is not exist".encode())

    def RMD(self):

        contents = [os.path.join(path, i) for i in os.listdir(path)]

        [os.remove(i) if os.path.isfile(i) or os.path.islink(i) else shutil.rmtree(i) for i in contents]
        control_conn.send("done".encode())


host=socket.gethostbyname(socket.gethostname())
control_port=11344
data_port=11345

clients=[]
controllsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controllsocket.bind((host,control_port))
datasocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
datasocket.bind((host,data_port))

while True :
    controllsocket.listen(5)
    datasocket.listen(5)
    print("waiting for connections")
    (control_conn,address)=controllsocket.accept()
    (data_conn,address)=datasocket.accept()

    t=Ftp_server(control_conn,data_conn,address[0],address[1])
    t.start()
    clients.append(t)



#s= socket.socket()
#host=socket.gethostbyname(socket.gethostname())
#port= 12344
#s.bind((host, port))
#s.listen(5)
#while (True):
#    c, addr = s.accept()
#    print(c)
#    print(addr)
#    print("got connection from", addr)
#    c.send('thank you for connecting'.encode())
#    c.close()

