import uuid, time
import socket
import traceback, os, sys
from threading import *

package_size = 4096
host = ''
port = 12345
alive_client = {}
transfer_client = {}

def gen_key():
    return str(uuid.uuid1()).split('-')[0]

def handle_heatbeat():
    while 1:
        for client_key in alive_client.keys():
            try:
                item = alive_client[client_key]
                print 'send heart beat to ', client_key, ' size', item['size']
                item['sock'].sendall('ALIVE\n')
            except:
                print 'client close'
                del(alive_client[client_key])
                continue
        time.sleep(5)

def handle_new_client(clientsock):
    print 'New Client Coming...'
    data = clientsock.recv(1024)
    if data.split(' ')[0] == 'FILE':
        length = data.split(' ')[1]
    key = gen_key()
    alive_client[key] = {'sock':clientsock, 'size':length}
    clientsock.sendall('KEY ' + key + '\n')
    print 'insert To waiting list'


if __name__ == '__main__':
    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    heatbeat = Thread(target = handle_heatbeat, args = [])
    heatbeat.setDaemon(1)
    heatbeat.start()

    while 1:
        try:
            clientsock, clientaddr = s.accept()
        except KeyboardInterrupt:
            s.close()
            break;
        except:
            continue
        t= Thread(target = handle_new_client, args = [clientsock])
        t.setDaemon(1)
        t.start()
