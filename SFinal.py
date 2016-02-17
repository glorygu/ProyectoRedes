#!/usr/bin/python
# -*- coding: utf-8 -*-


import socket
import sys


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


ack_list = []
expected_sec_num = 1

# -------------------- Extraccion de paquetes ----------------------------------

def clear_list(input_list):
    size = len(input_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del input_list[size-iterator]
        iterator += 1


def extract_acks (initial_package):
    print "Extrayendo ACKS"
    global expected_sec_num
    iterator = 0
    size = len(initial_package)
    clear_list(ack_list)
    acks_in_order = True
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
            print "ACk actual en formato de string " + current_ack
            if int(current_ack) == expected_sec_num:
                ack_list.append(current_ack)
                expected_sec_num += 1
                
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
print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)
sock.listen(1)

# ------------------------------------------------------------------------------

while True:
    
    connection, client_address = sock.accept()
 
    try:
        
        while True:
            data = connection.recv(1000)
            print >>sys.stderr, 'Mensaje recibido: "%s" \n' % data
            
            
            # Analizar lo recibido y reenviar acks al intermediario
            
            
            if data:
                
                # --------------------- Socket para envio de trafico -------------------------

                socket_intermediario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_address = ('localhost', 10002)
                print >>sys.stderr, 'conectando a %s puerto %s' % server_address
                socket_intermediario.connect(server_address)
                
                # ------------------------------------------------------------------------------
                
                try:
                    message = data
                    extract_acks(message)
                    iterator = 0 
                    for iterator in range(0, len(ack_list)):
                            socket_intermediario.sendall("#"+ack_list[iterator])
                            print "Enviando al cliente el ACK: " + ack_list[iterator]
                    
                finally:
                    socket_intermediario.close()
                
            else:
                print >>sys.stderr, 'no hay mas datos', client_address
                break
             
    finally:
        # Cerrando conexion
        connection.close()