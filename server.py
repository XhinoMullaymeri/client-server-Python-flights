import socket
import threading
import json
import time
import random
import datetime

class Server(object):
    def __init__(self):
        print("SERVER started")
        self.lock = threading.Lock()
        self.address = '127.0.0.1'
        self.port = 9999
        self.flights = [
            {'code': 1, 'status': 'Arrival', 'time': '03:50'},
            {'code': 2, 'status': 'Departure', 'time': '12:50'},
            {'code': 3, 'status': 'Arrival', 'time': '19:30'},
            {'code': 17 ,'status': 'Departure','time' :'??:??' }
        ]
        self.min_read_time = 2
        self.min_write_time = 4
        self.delay=2 


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


    def flight_already_exists(self,flight_code):
        """
        Get flight code and returns none if it doesnt exit
        and "exists" if it does.

        params:
            code:string
        """
        for flight in self.flights:
            if flight_code == str(flight['code']):
               return 'exists'
        return None

    
    def append_flight(self, code, status, flight_time):
        """
        Get the flight data and if code is unique append a new dictionary
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
            if self.flight_already_exists(code) is None:
                new_flight = {
                    'code': code,
                    'status': status,
                    'time': flight_time
                    }
                self.flights.append(new_flight)
                return 'WOK'
            else:
                return 'WERR flight already exists'


    def return_all_Flight(self):
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
                
                if 'READ'==in_msg[:4]:
                    try:
                        _, flight_code = in_msg.split()
                        out_msg = self.get_flight(flight_code)
                    except:
                        out_msg='RERR check HELP'
                    connection.sendall(out_msg.encode('utf-8'))
                    
                if 'WRITE'== in_msg[:5]:
                    try:
                        _, code, status, flight_time = in_msg.split()
                        out_msg=self.append_flight(code, status, flight_time)
                    except:
                        out_msg='WERR check HELP'
                    connection.sendall(out_msg.encode('utf-8'))
                    
                if 'PRINT'==in_msg:
                    out_msg=self.return_all_Flight()
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
    SERVER.start_listening()
