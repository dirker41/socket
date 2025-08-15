import socket
import optparse
import time
import threading

timeout_cnt=0

class UdpClient(threading.Thread):
    def __init__(self, reply_entry, reply_addr, ip, data):
        threading.Thread.__init__(self)
        self.reply_entry=reply_entry
        self.reply_addr=reply_addr
        self.ip=ip
        self.data=data

    def run(self):
        HOST=self.ip
        PORT=123
        data=self.data

        server_addr=(HOST, PORT)
        #for i in range(0, (len(data)//4)-1):
        # print(hex(data[i*4+0])[2:].zfill(2)+" "+hex(data[i*4+1])[2:].zfill(2)+" "+hex(data[i*4+2])[2:].zfill(2)+" "+hex(data[i*4+3])[2:].zfill(2)+" ")
        client=socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.bind(('10.96.1.1', 0))

        client.settimeout(2)
        client.sendto(data, server_addr)
        try:
            indata, addr=client.recvfrom(1024)

            self.reply_entry.sendto(indata, self.reply_addr)
            self.ret=0

            print("get rsp from server")
        except Exception as e:
            global timeout_cnt
            timeout_cnt+=1
            print(e)

        client.close()

if  __name__=='__main__':
    udps=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    udps.bind(('10.96.1.2',123))
    
    try:
        while 1:
            data, addr=udps.recvfrom(1024)
            #print(addr)

            if(addr[0]=="10.96.1.1"):
                pass
            else:
                print("reject"+addr)
                continue

            server="185.125.190.57"
            UdpClient(udps, addr, server, data).start()

            
    except KeyboardInterrupt:
        udps.close()