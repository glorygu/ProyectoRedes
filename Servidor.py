#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Servidor
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
import sys

server_port = input ("Introduzca el puerto para comunicar al servidor con el intermediario: ")
# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto
server_address = ('localhost',server_port)
print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)

# Escuchando conexiones entrantes
sock.listen(1)
biggest_ack = 0 
while (True): #while True:
    # Esperando conexion
    print >>sys.stderr, 'Esperando para conectarse'
    connection, client_address = sock.accept()
 
    try:
        print >>sys.stderr, 'concexion desde', client_address
 
        # Recibe los datos en trozos y reetransmite
        while (True): #while True
            data = connection.recv(4)
            
            
            if data:
                print >>sys.stderr, 'Paquete recibido "%s"' % data
                if len(data)>1:
                    current_ack = data[1] #port_number = int(data)
                    print >>sys.stderr, 'enviando ack "%s" de vuelta al intermediario' % current_ack
                    connection.sendall(current_ack)
                if current_ack > biggest_ack:
                    biggest_ack = current_ack
            else:
                print >>sys.stderr, 'no hay mas datos', client_address
                break
             
    finally:
        # Cerrando conexion
        connection.close()
        

#print 'Puerto recibido:  ', port_number
