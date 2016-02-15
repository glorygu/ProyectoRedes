#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Cliente
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
import sys
import time 
 
def clear_list(input_list):
    size = len(input_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del input_list[size-iterator]
        iterator += 1
# ------------------ Cliente ----------------------

print "-----------------------------------------------------"
print "    Bienvenido a Simulacion de Red 2016 - Cliente"
print "-----------------------------------------------------"
print "\n\n"
print "A continuacion ingrese los datos que se le solicitan"
print "\n\n"

# Variables de ingreso de datos
file_name = raw_input("Introduzca el nombre del archivo: ")
window_size =  input("Introduzca el tamano de la ventana: ")
client_port = input("Introduzca el puerto para comunicarse con el intermediario: ")
user_time = input("Escriba la cantidad de milisegundos que desea: ")

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"
if user_mode == 1:
    debug_mode = False
else:
    debug_mode = True
    
# Inicializacion de variables
content_list = []
received_acks_list = []
file_opened = False
content_iterator = 0
sec_num = 1
# Abrir archivo 
while  file_opened == False: 
    print "Abriendo archivo: ", file_name
    try: 
        fo = open (file_name, access_mode)
        content = fo.read() #mete todo el conenido en la string content
        file_opened == True
    except IOError:
        print "Error al abrir el achivo. Debe introducir el nombre del archivo correctamente. "
        file_name = raw_input("Introduzca el nombre del archivo: ")
    
    
# Pasa contenido de archivo de string a una lista
for char in content:
    content_list.append(char)
    #mete todo el contenido en un array 
# Cierra archivo
fo.close( )


# Conexion
# Conecta el socket en el puerto cuando el servidor esté escuchando
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', client_port)
print >>sys.stderr, 'conectando a %s puerto %s' % server_address
sock.connect(server_address)

try:
     
    # Enviando datos
    #message =raw_input("Introduzca elnumero de puerto mensjae")
    #print >>sys.stderr, 'enviando "%s"' % message
    #sock.sendall(message)
    while (content_iterator < len(content_list)):
        acked_segs = 0
        window_start = content_iterator
        window_end = content_iterator + window_size
        for it in range (0, window_size):
        #Enviando contenidos de la ventana
            if (content_iterator+it < len(content_list)):
                package = "#"+ str(sec_num)+":"+content_list [content_iterator+it]
                sock.send(package)
                print ("Enviando "+ package)
                sec_num = sec_num + 1
                #time.sleep(2)
                
        
        #Recibe Acks
        try:
            clear_list(received_acks_list)
            it = 0
            while it < window_size:
                amount_received = 0
                amount_expected = 1
                # Recibe datos del intermediario
                while amount_received < amount_expected:
                    data = sock.recv(19)
                    amount_received += 1
                    received_acks_list.append(int(data))
                    print >>sys.stderr, 'recibiendo "%s"' % data
                it+=1
        finally:
            print "ACKS recibidos " + str(len(received_acks_list))
            min_ack = min(received_acks_list)
            print "El ack mas pequeno es: " + str(min_ack)
        #Cuenta ACKs recibidos
        '''acked_segs = input("ACKed segs")
        if (acked_segs>window_size):
            acked_segs = window_size #acked_segs lo va aindicar el intermediario
        sec_num=sec_num-(window_size-acked_segs)
        '''
        #--------------Corre Ventana---------------------
        if min_ack <= window_end and min_ack >= window_start:
            acked_segs = min_ack - window_start
            sec_num = min_ack + 1
        else:
            acked_segs = 0
            sec_num = window_start + 1
            
        print "ACKed segs " + str(acked_segs) + "sec_num: "+ str(sec_num)        
        content_iterator = content_iterator + acked_segs
        print "current value of content_iterator: ", content_iterator 
        # Buscando respuesta
finally:
    print >>sys.stderr, 'cerrando socket'
    sock.close()