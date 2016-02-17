#!/usr/bin/python
# -*- coding: utf-8 -*-


import socket
from socket import AF_INET, SOCK_STREAM
import sys
import time


print "-----------------------------------------------------"
print "    Bienvenido a Simulacion de Red 2016 - Servidor"
print "-----------------------------------------------------"
print "\n\n"
print "A continuacion ingrese los datos que se le solicitan"
print "\n\n"

# Variables de ingreso de datos

inter_port = input("Introduzca el puerto de escucha del servidor: ")

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"

debug_mode = False
ack_list = []
expected_sec_num = 1

# -------------------- Definicion de modo --------------------------------------

if user_mode==2:
    debug_mode = True
    
# -------------------- Creacion de archivo de salida ---------------------------

file_created = False

while file_created == False:
    output_file_name = raw_input("Ingrese el nombre de archivo de salida: ")
    try: 
        output_file = open (output_file_name, 'w+') 
    except IOError:
        print 'No se pudo abrir ', output_file_name
    else:
        if debug_mode:
            print 'Se creo archivo de salida de manera exitosa. '
        file_created = True
        
        

    
# -------------------- Extraccion de paquetes ----------------------------------

def clear_list(input_list):
    size = len(input_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del input_list[size-iterator]
        iterator += 1


def extract_acks (initial_package):
    global expected_sec_num
    iterator = 0
    size = len(initial_package)
    clear_list(ack_list)
    acks_in_order = True
    if debug_mode:
        print "# secuencia esperado: " + str (expected_sec_num)
    while (iterator < size and acks_in_order):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_ack = ""
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#' and initial_package[iterator] != ':'):
                #print initial_package[iterator]
                current_ack += initial_package[iterator]
                iterator += 1
            #print "ACk actual en formato de string " + current_ack
            if int(current_ack) == expected_sec_num:
                ack_list.append(current_ack)
                expected_sec_num += 1
                if (initial_package[iterator] == ':'):
                    if (iterator+1 < len(initial_package)):
                        output_file.write(initial_package[iterator+1])
                # Ingresar valor a archivo de salida
                
            else:
                acks_in_order = False
        else:
            iterator+=1
    return ack_list

# ------------------------------------------------------------------------------

# -------------------- Variables globales --------------------------------------


# ------------------------------------------------------------------------------


# --------------------- Socket para ingreso de trafico -------------------------

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', int(inter_port))
if debug_mode:
    print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)
sock.listen(1)

# ------------------------------------------------------------------------------

while True:
    
    connection, client_address = sock.accept()
 
    try:
        
        while True:
            data = connection.recv(1000)
            if debug_mode:
                print >>sys.stderr, 'Mensaje recibido: "%s" \n' % data
            
            
            # Analizar lo recibido y reenviar acks al intermediario
            
            
            if data:
                
                # --------------------- Socket para envio de trafico -------------------------

                socket_intermediario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('localhost', 10002)
                if debug_mode:
                    print >>sys.stderr, 'conectando a %s puerto %s' % server_address
                socket_intermediario.connect(server_address)
                
                # ------------------------------------------------------------------------------
                
                try:
                    message = data
                    extract_acks(message)
                    iterator = 0 
                    for iterator in range(0, len(ack_list)):
                            socket_intermediario.sendall("#"+ack_list[iterator])
                            if debug_mode:
                                print "Enviando al cliente el ACK: " + ack_list[iterator]
                    
                finally:
                    socket_intermediario.close()
                
            else:
                if debug_mode:
                    print >>sys.stderr, 'no hay mas datos', client_address
                break
             
    finally:
        # Cerrando conexion
        connection.close()
