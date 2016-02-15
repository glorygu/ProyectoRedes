#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Servidor
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

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
                    socket_intermediario.sendall("ACK: "+message)
                    
                finally:
                    socket_intermediario.close()
                
            else:
                print >>sys.stderr, 'no hay mas datos', client_address
                break
             
    finally:
        # Cerrando conexion
        connection.close()
