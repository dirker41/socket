import socket
import optparse
import time
import threading

timeout_cnt=0

def append_cors_pattern(in_bytes):
    in_bytearray = bytearray(in_bytes)
    header_end=0

    for i in range(1, len(in_bytearray)):
        #instr=instr.replace("\r\n\r\n", "\r\nAccess-Control-Allow-Origin: *\r\n\r\n")
        if(in_bytearray[i]==13 and in_bytearray[i+1]==10 and in_bytearray[i+2]==13 and in_bytearray[i+3]==10 ): # match ASCII 13 /r, ASCII 10 /n
            header_end=i
            break

    out_bytearrray=in_bytearray[:header_end+2]+b'Access-Control-Allow-Origin: *\r\n'+ in_bytearray[header_end+2:]
    print("append_cors_pattern done")
    return bytes(out_bytearrray)

class TcpClient(threading.Thread):
    def __init__(self, src_conn, src_addr, dst_server, data):
        threading.Thread.__init__(self)
        self.reply_entry=src_conn
        self.reply_addr=src_addr
        self.ip=dst_server
        self.data=data

    def run(self):
        HOST=self.ip
        PORT=80
        data=self.data

        #for i in range(0, (len(data)//4)-1):
        # print(hex(data[i*4+0])[2:].zfill(2)+" "+hex(data[i*4+1])[2:].zfill(2)+" "+hex(data[i*4+2])[2:].zfill(2)+" "+hex(data[i*4+3])[2:].zfill(2)+" ")
        tcpClient=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        tcpClient.settimeout(10)

        tcpClient.connect((HOST, PORT))
        tcpClient.send(data)
        try:
            indata=tcpClient.recv(1024)

            indata_bytearray = bytearray(indata)

            print("get rsp from server")

            out_data=append_cors_pattern(indata)

            print(out_data)
            
            self.reply_entry.send(out_data)
            self.ret=0

        except Exception as e:
            global timeout_cnt
            timeout_cnt+=1
            print(e)
        except KeyboardInterrupt:
            tcpClient.close()

        tcpClient.close()

if  __name__=='__main__':
    tcps=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    port=8181
    tcps.bind(('127.0.0.1', port))
    tcps.listen()

    print("port="+str(port))
    
    try:
        while 1:
            src_conn, src_addr = tcps.accept()
            data=src_conn.recv(1024)
            #print(addr)

            #if(addr[0]=="127.0.0.1"):
            #    pass
            #else:
            #    print("reject"+addr)
            #    continue

            print(data)

            dst_server="172.41.5.231"
            dst_server="127.0.0.1"
            #dst_server="172.253.118.99"
            TcpClient(src_conn, src_addr, dst_server, data).start()

            
    except KeyboardInterrupt:
        tcps.close()
        print("keyboard kill")

    tcps.close()