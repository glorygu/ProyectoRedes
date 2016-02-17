# 
#   Universidad de Costa Rica
#
#   Desarrollado por: Gloriana Garro
#                     Jose Pablo Urena Gutierrez
#


import socket
import sys
import threading
import random
 
 
print "-----------------------------------------------------"
print "    Bienvenido a Simulacion de Red 2016 - Intermediario"
print "-----------------------------------------------------"
print "\n\n"
print "A continuacion ingrese los datos que se le solicitan"
print "\n\n"

# Variables de ingreso de datos

inter_server_port = input("Introduzca el puerto de escucha del servidor: ")
inter_client_port = input("Introduzca el puerto de escucha del cliente: ")
probability = ""

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n"

debug_mode = True
dummy = False

if user_mode == 1:
    debug_mode = False
    probability = input("\nIntroduzca la probabilidad de perdida de paquetes: ")
else:
    debug_mode = True 


# --------------  Creacion de la clase para hilos ------------------------------

# Hilo 0 -- Desde cliente hasta servidor
# Hilo 1 -- Desde servidor hasta cliente

class myThread (threading.Thread):
    def __init__(self, name, thread_number):
        threading.Thread.__init__(self)
        self.name = name
        self.thread_number = thread_number
        
        # Procedimiento al correr el hilo
        
    def run(self):
        
        runThreads(self.name, self.thread_number)

# ------------------------------------------------------------------------------

# --------------- Socket compartido de escucha y envio a cliente ---------------

socket_listen_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(inter_client_port))
socket_listen_client.bind(server_address)
socket_listen_client.listen(1)
connectionC, client_address = socket_listen_client.accept()

# ------------------------------------------------------------------------------

# ----------------- Funciones para el manejo de paquetes -----------------------

package_list = []

def clear_list():
    size = len(package_list) 
    iterator = 1
    while iterator <= size:
        del package_list[size-iterator]
        iterator += 1

def split_packages (initial_package):
    iterator = 0
    size = len(initial_package)
    clear_list ()
    while (iterator < size):
        if initial_package[iterator] == '#':
            current_package = "#"
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#'):
                current_package += initial_package[iterator]
                iterator += 1
            package_list.append(current_package)
        else:
            iterator+=1

# ------------------------------------------------------------------------------


# ----- Metodo encargado de activar los hilos y preparar la escucha de datos ---

def runThreads(name, thread_number):
    if thread_number == 0:
    	# Levanta el hilo 0
    	
    	while True:
    		
    		try:
    			
    			while True:
    				data = connectionC.recv(1000)
    				if data:
    					socket_send_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				        server_address = ('localhost', int(inter_server_port))
				        socket_send_server.connect(server_address)
				        
				        try:
				        	message = data
				        	
				        	split_packages(message)  							# Se analiza el paquete
				        	
				        	if user_mode == 1:
				        	    
				        	    for index in range(len(package_list)):
				        	        random_number = random.randint(100,10000) * 0.010
				        	        if random_number >= probability:
				        	            socket_send_server.sendall(package_list[index])
				        	        else:
				        	            print >>sys.stderr, 'El siguiente paquete se ha perdido: ', package_list[index]
				        	    clear_list()									
				        	
				        	else:                                               # Se permite eliminar paquetes
				        	    
				        	    for index in range(len(package_list)):
				        	        choice = raw_input("Desea eliminar el siguiente paquete? : "+package_list[index]+" (Y, N): ")
				        	        if choice == "y" or choice == "Y":
				        	            print >>sys.stderr, 'El siguiente paquete se ha eliminado: ', package_list[index]
				        	        else:
				        	            socket_send_server.sendall(package_list[index])
				        	            
				        	    clear_list()
				        	
				        finally:
				        	socket_send_server.close()
				        	
    		finally:
    			dummy = False
    	
    elif thread_number == 1: 
    	
    	# Levanta el hilo 1    	
    	
    	socket_listen_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	server_address = ('localhost', 10002)
    	socket_listen_server.bind(server_address)
    	socket_listen_server.listen(1)
    	
    	
    	while True:
    		
    		connection, client_address = socket_listen_server.accept()
    		
    		try:
    			
    			while True:
    				data = connection.recv(1000)
    				if data:
				        
				        try:
				        	message = data
					        connectionC.sendall(message)
					        
				        finally:
				        	dummy = False
				        	
    				else:
    					break
				        	
				        	
    		finally:
    			
    			dummy = False

# ------------------------------------------------------------------------------

# Creacion de hilos

thread0 = myThread("Hilo Cliente a Servidor", 0)
thread1 = myThread("Hilo Servidor a Cliente" ,  1)

# Inicio de los hilos

thread0.start()
thread1.start()