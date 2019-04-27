import datetime
import sys
import socket
import time
import random

class Client():
    def __init__(self):
        print('Client started')
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_address = '127.0.0.1'
        self.server_port = 9999
        self.simulation_sleep_time=3
        
    def show_options(self):
        self.menu_options = {'READ':'reading from the flight table',
		                'WRITE':'writing a new entry to the flight table',
                                'HELP':'help',
                                'DATA': 'returning the database',
                                'MODIFY': 'modifies an entry',
                                'DELETE': 'deletes an entry',
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
            
            input_msg=self.handle_client_msg(out_msg)
                     

    def handle_client_msg(self,msg):
        """
        Gets and handles clients request
        Returns a string that is the msg prompt
        params:
            request:string
        """
        command=msg.split(" ")
        command=command[0]

        if self.is_not_included_in_options(command):
            input_msg = '(failure on last attempt)--Enter your command: '  
        elif command == 'EXIT':
            self.socket.sendall(msg.encode('utf-8'))
            time.sleep(3)
            self.socket.close()
            sys.exit()
        elif command == 'HELP':
            input_msg='Enter your command: '
            print('\nREAD usage: READ <code>\n'+
                      'WRITE usage WRITE <code> <status> <time>\n'+
                      'DELETE usage DELETE <code>\n'+
                      'MODIFY usage MODIFY <code> <status> <time>\n'+
                      'DATA usage DATA\n'+
                      'EXIT usage EXIT\n')

        else:
            input_msg='Enter your command: '
            print(f'Your message: {msg}')
            print('Message sent \t time: ' + str(datetime.datetime.now().time()))
            self.socket.sendall(msg.encode('utf-8'))
            data = self.socket.recv(1024).decode('utf-8')
            print('reply received \t time: '+str(datetime.datetime.now().time()))
            print(data+'\n')
        return input_msg

    
    def connect_with_server_simulation(self):
        """
            This function tries to simulate a client
            it's either a reader or writer based on luck.
        """
        pass

        #decides the type (writer or reader)
        toss= random.randint(0,3)
        if toss<3:
            client_type=1 #reader
            print('\nReader created!\n')
        else:
            client_type=2 #write
            print('\nWriter created!\n')

        input_msg='Enter your command: '
        
        self.socket.connect((self.server_address,self.server_port))


        #dummy list with options (read/write/modify)
        entries_list=[
            {'code': '1', 'status': 'Arrival', 'time': '03:50'},
            {'code': '2', 'status': 'Departure', 'time': '12:50'},
            {'code': '3', 'status': 'Arrival', 'time': '19:30'},
            {'code': '4' ,'status': 'Departure','time' :'??:??' },
            {'code': '5', 'status': 'Arrival', 'time': '04:20'},
            {'code': '6', 'status': 'Departure', 'time': '07:50'},
            {'code': '7', 'status': 'Arrival', 'time': '09:30'},
            {'code': '8' ,'status': 'Departure','time' :'15:10' }
            ]
        # list with clients commands
        commands_list=['READ ','DELETE ','WRITE ','MODIFY ']

        #reader
        if client_type==1:

            while True:
                #READ+number(1-10) 1-10 cause we want to have codes that
                #will never be in the database
                out_msg = commands_list[0] + str(random.randint(0,10)) 

                self.handle_client_msg(out_msg)
                time.sleep(client_type*self.simulation_sleep_time)
                
        #writer
        else:
           
            while True:
                option=random.randint(1,3)
                if option==1:
                    #DELETE+number(1-10) 1-10 cause we want to have codes that
                    #might not be in the database
                    out_msg=commands_list[option]+str(random.randint(0,10))
                elif option==2:
                    #picking an entry to WRITE
                    entry=entries_list[random.randint(1,8)-1]
                    #creating msg
                    out_msg=commands_list[option]+entry['code']+" "+entry['status']+\
                             " "+entry['time']
                else:
                    #picking an entry to MODIFY
                    entry=entries_list[random.randint(1,8)-1]
                    #2nd entry we need it in order to modify the 1st one
                    entry2=entries_list[random.randint(1,8)-1]
                    #creating msg
                    out_msg=commands_list[option]+entry['code']+" "+entry2['status']+\
                             " "+entry2['time']
                    
                self.handle_client_msg(out_msg)
                
                time.sleep(client_type*self.simulation_sleep_time)


if __name__ == "__main__":
    client = Client()
    client.show_options()
    client.connect_with_server_user()
    #client.connect_with_server_simulation()






























