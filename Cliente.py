#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Cliente
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
import sys
 
 

file_name = raw_input("Introduzca el nombre del archivo: ")
print file_name
# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print "Abriendo archivo: ", file_name

access_mode = "r" # r access mode is for reading only. File pointer is at the beginning of file 

fo = open (file_name, access_mode)

content = fo.read() #mete todo el conenido en la string content
content_list = []
for char in content:
    content_list.append(char)
    #mete todo el contenido en un array 

#verificar contenido    
#for x in range (0, len(content_list)):
    #print content_list[x]
    
fo.close( )

#------Mover Ventana-------
window_size =  input("Introduzca el tamanio de ventana")
x = 0
sec_num = 1
while (x < len(content_list)):
    acked_segs = 0
    for it in range (0, window_size):
        if (x+it < len(content_list)):
            print ("Sending item #"+ str(sec_num)+":"+content_list [x+it])
            sec_num = sec_num + 1
        #else:
            #print "All items have been sent"
    acked_segs = input("ACKed segs")
    if (acked_segs>window_size):
        acked_segs = window_size #acked_segs lo va aindicar el intermediario
    sec_num=sec_num-(window_size-acked_segs)
    x = x + acked_segs
    print "current value of x: ", x 




# Conecta el socket en el puerto cuando el servidor esté escuchando

port = input ("puerto cliente: ")
server_address = ('localhost', port)
print >>sys.stderr, 'conectando a %s puerto %s' % server_address
sock.connect(server_address)

try:
     
    # Enviando datos
    message =raw_input("Introduzca el numero de puerto")
    print >>sys.stderr, 'enviando "%s"' % message
    sock.sendall(message)
 
    # Buscando respuesta
    amount_received = 0
    amount_expected = len(message)
     
    while amount_received < amount_expected:
        data = sock.recv(19)
        amount_received += len(data)
        print >>sys.stderr, 'recibiendo "%s"' % data
 
finally:
    print >>sys.stderr, 'cerrando socket'
    sock.close()


