#! python3
import socket
import threading
import json
import time
import random
import datetime
import sys

class Server(object):
    def __init__(self):
        print("SERVER started")
        self.lock = threading.Lock()
        self.address = '127.0.0.1'
        self.port = 9999
        self.flights = [
            {'code': '1', 'status': 'Arrival', 'time': '03:50'},
            {'code': '2', 'status': 'Departure', 'time': '12:50'},
            {'code': '3', 'status': 'Arrival', 'time': '19:30'},
            {'code': '4' ,'status': 'Departure','time' :'??:??' }
        ]
        self.min_read_time = 2
        self.min_write_time = 3
        self.min_delete_time = 2
        self.min_modify_time = 2
        self.delay=2 


    def set_params(self):

        if len(sys.argv)==6:
            self.min_read_time = sys.argv[1] 
            self.min_write_time = sys.argv[2]
            self.min_delete_time = sys.argv[3]
            self.min_modify_time = sys.argv[4]
            self.delay=sys.argv[5]
        elif len(sys.argv)==1:
            #default values
            pass
        else:
         print("Read readme\nThis is not the proper way to run it\n"+
              "!!!servert.py or client.py <arg1> <arg2> <arg3> <arg4>"+
               "<arg5>!!!\n"
              "<arg1>=READ extra sleep time\n"+
               "<arg2>=WRITE extra sleep time\n"+
               "<arg3>=DELETE extra sleep time\n"+
               "<arg4>=MODIFY extra sleep time\n"+
               "<arg5>= general delay for every action\n")
         sys.exit()
        

    def get_flight(self, flight_code):
        """
        Search in the "database" to find the flight with the
        given code.  If not found,returns 'RERR' else 'ROK'+flight info.

        params: flight_code: string 
        """
        # self.lock.acquire()
        with self.lock:  # acquire and release the lock
            time.sleep(random.randrange(0, self.delay)+self.min_read_time)
            
            for flight in self.flights:
                if flight_code == str(flight['code']):
                    flight_info=" "+str(flight['code'])+" "+\
                    str(flight['status'])+" "+\
                    str(flight['time'])
                    return 'ROK'+flight_info

        # self.lock.release()
        return 'RERR flight does not exist' 


    def flight_index(self,flight_code):
        """
        Get flight code and returns none if it doesnt exit
        and index of list  if it does.

        params:
            code:string
        """
        index=0
        for flight in self.flights:
            if flight_code == str(flight['code']):
                return index
            index=index+1
        return None

    
    def append_flight(self, code, status, flight_time):
        """
        Gets the flight data and if code is unique append a new dictionary
        to the list.
        Returns WOK if appended or WERR if not.
        params:
            code: string
            status: string
            flight_time: string
        """
        with self.lock:
            # delay the write
            time.sleep(random.randrange(0, self.delay)+self.min_write_time)  
            if self.flight_index(code) is None:
                new_flight = {
                    'code': code,
                    'status': status,
                    'time': flight_time
                    }
                self.flights.append(new_flight)
                return 'WOK'
            else:
                return 'WERR flight already exists'
            
    def delete_flight(self,code):
        """
        Deletes a flight if the code exists
        Returns DOK if succeed or DERR if not
        params:
            code: string
        """
        
        with self.lock:
            #delay
            time.sleep(random.randrange(0, self.delay)+self.min_delete_time)
            index=self.flight_index(code)
            if index is None:
                return 'DERR flight doesnt exist'
            else:
                del self.flights[index]
                return 'DOK'

    def modify_flight(self,code,status,flight_time):
        """
        Gets code and if flight exists modifies it.
        If succeed returns MOK else MERR
        params:
            code: string
            status: string
            flight_time:string
        """
        with self.lock:
            #delay
            time.sleep(random.randrange(0, self.delay)+self.min_modify_time)
            index=self.flight_index(code)
            if index is None:
                return 'MERR flight doesnt exist'
            else:
                self.flights[index]={'code': code ,'status': status,'time' : flight_time }
                return 'MOK'

        
        
    def return_all_flights(self):
        """
        Return a string that contains
        our database
        """
        with self.lock:
            time.sleep(1)
            flight_info="\n"
            for f in self.flights:
                flight_info=flight_info+str(f['code'])+" "+\
                        str(f['status'])+" "+\
                        str(f['time'])+"\n"
        return(flight_info)

    
    def handle_client(self, connection):
        """
        Gets the client's message via conncetion socket
        and handles it (calls the proper function).

        params:
        connection: socket 

        """
        while True:
            try:
                in_msg = connection.recv(1024).decode('utf-8')
                
                time=str(datetime.datetime.now().time())
                print(f'received msg : {in_msg} \t time: {time}')
                
                if 'EXIT'==in_msg:
                    connection.close()
                
                elif 'READ'==in_msg[:4]:
                    try:
                        _, flight_code = in_msg.split()
                        out_msg = self.get_flight(flight_code)
                    except:
                        out_msg='RERR check HELP'
                    connection.sendall(out_msg.encode('utf-8'))
                    
                elif 'WRITE'== in_msg[:5]:
                    try:
                        _, code, status, flight_time = in_msg.split()
                        out_msg=self.append_flight(code, status, flight_time)
                    except:
                        out_msg='WERR check HELP'
                    connection.sendall(out_msg.encode('utf-8'))
                    
                elif 'DATA'==in_msg[:4]:
                    try:
                        out_msg=self.return_all_flights()
                    except:
                        out_msg='DATAERR check HELP'
                    connection.sendall(out_msg.encode('utf-8'))

                elif 'MODIFY'==in_msg[:6]:
                    try:
                        _, code, status, flight_time = in_msg.split()
                        out_msg=self.modify_flight(code, status, flight_time)
                    except:
                        out_msg='MERR check HELP'
                    connection.sendall(out_msg.encode('utf-8'))
                        
                elif 'DELETE'==in_msg[:6]:
                    try:
                        _, code= in_msg.split()
                        out_msg=self.delete_flight(code)
                    except:
                        out_msg='DERR check HELP'
                    connection.sendall(out_msg.encode('utf-8'))
            except:
                connection.close()
                 
                
            

    def start_listening(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as connection_sock:
            # socket.SO_REUSEADDR--> if in TIME_WAIT then you can reuse the port
            connection_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)            
            connection_sock.bind((self.address, self.port))
            connection_sock.listen(5) #max queue 5 

            while True:
                connection, address = connection_sock.accept()
                print(f'Connection oppened for {address}')
                threading.Thread(
                    target=self.handle_client,
                    args=(connection,)).start()
        



if __name__ == "__main__":
    SERVER = Server()
    SERVER.set_params()
    SERVER.start_listening()
    
        
