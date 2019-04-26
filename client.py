import datetime
import sys
import socket
import time


class Client():
    def __init__(self):
        print('Client started')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = '127.0.0.1'
        self.server_port = 9999
        
    def show_options(self):
        self.menu_options = {'READ':'reading from the flight table',
		                'WRITE':'writing a new entry to the flight table',
                                'HELP':'help',
                                'PRINT': 'returning the database',
		                'EXIT':'closing the connection and exiting'
                                }
						
        for key in self.menu_options:
            print(f'\n{key} is msg code for {self.menu_options[key]}')
        print('\n')
        
    def is_not_included_in_options(self,msg):
        return not msg in self.menu_options
	
	
    def connect_with_server_user(self):
        input_msg='Enter your command: '
        
        self.socket.connect((self.server_address,self.server_port))
        
        while True:
            out_msg = input(input_msg)
            
            command=out_msg.split(" ")
            command=command[0]

            if self.is_not_included_in_options(command):
                input_msg = '(failure on last attempt)--Enter your command: '  
            elif command == 'EXIT':
                self.socket.sendall(out_msg.encode('utf-8'))
                time.sleep(3)
                self.socket.close()
                sys.exit()
            elif command == 'HELP':
                input_msg='Enter your command: '
                print("READ usage: READ <code>\n"+
                      "WRITE usage WRITE <code> <status> <time>")

            else:
                input_msg='Enter your command: '
                print('request sent \t time: ' + str(datetime.datetime.now().time()))
                self.socket.sendall(out_msg.encode('utf-8'))
                data = self.socket.recv(1024).decode('utf-8')
                print('reply received \t time: '+str(datetime.datetime.now().time()))
                print(data+'\n')
                     
    
    def connect_with_server_simulation(self):
        pass


if __name__ == "__main__":
    client = Client()
    client.show_options()
    client.connect_with_server_user()































