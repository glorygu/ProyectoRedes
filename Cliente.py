#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Cliente
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
from socket import AF_INET, SOCK_STREAM
import sys
import time

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
inter_port = input("Introduzca el puerto para comunicarse con el intermediario: ")
user_time = input("Escriba la cantidad de milisegundos que desea: ")
user_miliseconds = float(user_time)

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"


if user_mode == 1:
    debug_mode = False
else:
    debug_mode = True
    
# --------------------- Inicializacion de variables ----------------------------

content_list = []
#received_acks_list = []
file_opened = False
content_iterator = 0
sec_num = 1
sent_packages = 0
# ------------------------------------------------------------------------------

# ------------------------------ Analisis de archivo ---------------------------

while  file_opened == False: 
    if debug_mode:
        print "Abriendo archivo: ", file_name
    try: 
        fo = open (file_name, "r")
        content = fo.read()                             # Mete el contenido el string content
        
    except IOError:
        print "Error al abrir el achivo. Debe introducir el nombre del archivo. "
        file_name = raw_input("Introduzca el nombre del archivo: ")
    else:
        if debug_mode:
            print 'Se abrio el archivo de manera exitosa. '
        file_opened = True
    
    
# Pasa contenido de archivo de string a una lista
for char in content:
    content_list.append(char)
    
    # Mete todo el contenido en un array 
    
# Cierra archivo
fo.close( )
 
# ------------------------------------------------------------------------------


# ---------------- Creacion de socket hacia Intermediario ----------------------


socket_intermediario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(inter_port)
server_address = ('localhost', port)
print >>sys.stderr, 'conectando a %s puerto %s' % server_address
socket_intermediario.connect(server_address)

# ------------------------------------------------------------------------------

# ---------------- Limpieza de listas ------------------------------------------

def clear_list(input_list):
    size = len(input_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del input_list[size-iterator]
        iterator += 1

# ------------------------------------------------------------------------------

# ---------------- Variables globales ------------------------------------------

expected_ack = 1
count_received_acks = 0

# ------------------------------------------------------------------------------


# ---------------- Separacion de ACK -------------------------------------------

received_ack_list = []

def clear_list():
    size = len(received_ack_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del received_ack_list[size-iterator]
        iterator += 1

def extract_acks (initial_package):
    iterator = 0
    size = len(initial_package)
    clear_list()
    while (iterator < size):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_ack = ""
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#'):
                #print initial_package[iterator]
                current_ack += initial_package[iterator]
                iterator += 1
            received_ack_list.append(current_ack)
        else:
            iterator+=1


# ------------------------------------------------------------------------------

file_end = False


# ---------------- Funcion para envio de mensajes a Intermediario --------------

try:
    
    while (content_iterator < len(content_list) and sec_num <= len(content_list)):                               # Iterador de archivo
    
        
        # -------------- Envio de paquetes -------------------------------------
        
        count_received_acks = 0
        window_start = content_iterator
        window_end = content_iterator + window_size
        print "Enviando ventana nueva"
        
        for it in range (0, window_size):
            sent_packages = 0
        #Enviando contenidos de la ventana
            if (content_iterator+it < len(content_list)):
                package = "#"+ str(sec_num)+":"+content_list [content_iterator+it]
                socket_intermediario.sendall(package)
                sent_packages += 1
                if debug_mode:
                    print ("Enviando "+ package)
                sec_num = sec_num + 1
                #time.sleep(2)
            
                
        # --------------- Fin de envio de paquetes -----------------------------
        
        
        # --------------- Recepcion de ACK ---------------------------------------------
        
        if debug_mode: 
            print "Empezando a recibir ACKs"
                
        print >>sys.stderr, 'Estoy esperando'
        data = ""
        
        time_start = time.time()
        millis = int(round(time.time() * 1000))
        keep_running = True
    
        while keep_running and count_received_acks < sent_packages :
            try:
                millis = float(round(time.time() - time_start, 4)) * 1000
                
                try:
                    data = socket_intermediario.recv(1000)
                    print "Datos recibidos " + data
                    extract_acks(data)
                    for index in range(0,len(received_ack_list)):
                        print "Examinando el ack: " +received_ack_list[index]
                        if (int(received_ack_list[index]) == expected_ack):
                            expected_ack += 1
                            count_received_acks += 1
                    if debug_mode:
                        print "ACKs recibidos: "+ str(count_received_acks) + " . Ultimo ack: " + str(expected_ack-1)
                    sec_num = window_start + count_received_acks + 1
                    content_iterator += count_received_acks
                    print "Numero de secuencia: " + str(sec_num)
                    nthing = raw_input("nothing")
                except socket.timeout:
                    print >>sys.stderr, ''
                
                
                if millis >= user_miliseconds:
                    keep_running = False
                    sec_num = window_start + 1
               
            except KeyboardInterrupt, e:
                break
        
        print >>sys.stderr, 'Sale de timer'
        
finally:                                                                        # Fin iterador de archivo
    print >>sys.stderr, 'Cliente cerrando socket'
    socket_intermediario.close()

# ------------------------------------------------------------------------------

