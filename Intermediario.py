#!/usr/bin/python
# -*- coding: utf-8 -*-


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
probability = input("Introduzca la probabilidad de perdida de paquetes: ")

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"
 


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
        print "Inicia el servicio: " + self.name
        runThreads(self.name, self.thread_number)
        print "Fin del servicio " + self.name


# ------------------------------------------------------------------------------

# --------------- Socket compartido de escucha y envio a cliente ---------------

socket_listen_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(inter_client_port))
socket_listen_client.bind(server_address)
print "Se ha levantado hilo desde cliente hasta servidor"
socket_listen_client.listen(1)
print "Esperando conexion desde cliente"
connectionC, client_address = socket_listen_client.accept()

# ------------------------------------------------------------------------------

# ----------------- Funciones para el manejo de paquetes -----------------------

package_list = []

def clear_list():
    size = len(package_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del package_list[size-iterator]
        iterator += 1

def split_packages (initial_package):
    iterator = 0
    size = len(initial_package)
    clear_list ()
    while (iterator < size):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_package = "#"
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#'):
                #print initial_package[iterator]
                current_package += initial_package[iterator]
                iterator += 1
            print "indice: " + str(iterator)
            if iterator-1 >= 0 and iterator < size:
                if initial_package[iterator] == '#' and initial_package[iterator-1]==':':
                    current_package += initial_package[iterator]
                    iterator += 1
            package_list.append(current_package)
        else:
            iterator+=1

# ------------------------------------------------------------------------------


# ----- Método encargado de activar los hilos y preparar la escucha de datos ---

def runThreads(name, thread_number):
    if thread_number == 0:
    	# Levanta el hilo 0
    	
    	while True:
    		
    		try:
    			# print >>sys.stderr, 'Conexion desde el cliente: ', client_address
    			
    			while True:
    				data = connectionC.recv(1000)
    				if data:
    					socket_send_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				        server_address = ('localhost', int(inter_server_port))
				        socket_send_server.connect(server_address)
				        
				        try:
				        	message = data
				        	
				        	split_packages(message)  							# Se analiza el paquete
				        	for index in range(len(package_list)):
				        	    
				        	    random_number = random.randint(100,10000) * 0.010
				        	    if random_number >= probability:
				        	        print "Se envia paquete"
				        	        socket_send_server.sendall(package_list[index])
				        	    else:
				        	        print "Se pierde el paquete"
				        	clear_list()										# Limpia el buffer temporal
				        	
				        finally:
				        	# print >>sys.stderr, 'Envio de dato a server'
				        	socket_send_server.close()
				        	
    		finally:
    			# connectionC.close()
    			print >>sys.stderr, '.'
    			# socket_send_server.close()
    	
    elif thread_number == 1: 
    	
    	# Levanta el hilo 1    	
    	
    	socket_listen_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    	server_address = ('localhost', 10002)
    	socket_listen_server.bind(server_address)
    	
    	print "Se ha levantado hilo desde servidor hasta cliente"
    	
    	socket_listen_server.listen(1)
    	
    	
    	while True:
    		print "Esperando conexion desde servidor"
    		connection, client_address = socket_listen_server.accept()
    		
    		try:
    			print >>sys.stderr, 'Conexion desde el servidor: ', client_address
    			
    			while True:
    				data = connection.recv(1000)
    				if data:
    					# socket_send_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				        # server_address = ('localhost', 10001)
				        # socket_send_client.connect(server_address)
				        
				        try:
				        	message = data
					        connectionC.sendall(message)
					        print >>sys.stderr, 'Mensaje de server: ', message
				        finally:
				        	print >>sys.stderr, 'Reenvia mensaje'
				        	# socket_send_client.close()
				        	
    				else:
    					break
				        	
				        	
    		finally:
    			# connection.close()
    			print >>sys.stderr, 'Reenvia mensaje a cliente'
    			# socket_send_client.close()
    	


# ------------------------------------------------------------------------------

# Creacion de hilos

thread0 = myThread("Hilo Cliente a Servidor", 0)
thread1 = myThread("Hilo Servidor a Cliente" ,  1)

# Inicio de los hilos

thread0.start()
thread1.start()