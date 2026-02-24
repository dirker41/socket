import socket
import time
import threading

if  __name__=='__main__':
    tcps=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
            rcv_str=data.decode('ascii')
            print(rcv_str)

            relpy_str="client:"+str(src_addr)+". send:"+rcv_str
            relpy_data=relpy_str.encode("ascii")
            src_conn.send(relpy_data)

            
    except KeyboardInterrupt:
        tcps.close()
        print("keyboard kill")

    tcps.close()