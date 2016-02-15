#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Servidor
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
import sys


def extract_ack(message):
    #print "-------------------------Iterando por paquete-------------------------"
    #print message
    message_to_send = ""
    iterator = 0
    ack_not_found = True 
    while iterator < len (message) and ack_not_found:
        
        if (message[iterator] == '#'):
            iterator+=1
            while ( iterator < len (message) and message[iterator] != ':'  ):
                message_to_send += message[iterator]
                iterator+=1
            if message[iterator] == ':':
                ack_not_found = False
        iterator+=1
    return message_to_send
def create_output_file():
    output_file_name = raw_input("Ingrese el nombre de archivo de salida: ")
    try: 
        file = open (output_file_name, 'w+') 
    except IOError:
        print 'No se pudo abrir ', output_file_name
    else:
        print 'Se creo archivo de salida de manera exitosa. '
        
# Ingreso de datos
server_port = input ("Introduzca el puerto para comunicar al servidor con el intermediario: ")
create_output_file()

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"
if user_mode == 1:
    debug_mode = False
else:
    debug_mode = True

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
            data = connection.recv(1000)
            
            
            if data:
                print >>sys.stderr, 'Paquete recibido "%s"' % data
                current_ack = extract_ack(data)
                connection.send(current_ack)
                print >>sys.stderr, 'enviando ack "%s" de vuelta al intermediario' % current_ack
                #falta meterlo en el archivo de salida
                '''current_ack = int(message_to_send)
                if current_ack > biggest_ack:
                    biggest_ack = current_ack'''
            else:
                print >>sys.stderr, 'no hay mas datos', client_address
                break
             
    finally:
        # Cerrando conexion
        connection.close()
        

#print 'Puerto recibido:  ', port_number
