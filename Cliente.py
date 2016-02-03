#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Cliente
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
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

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"
 
 
# ----------------- Apertura de archivo para envio ----------------------------------------------

print "Analizando archivo: ", file_name
time.sleep(2)
print "..."
time.sleep(2)
print "..."
time.sleep(2)
print "Fin de análisis, archivo seguro"
time.sleep(2)
print "\n\n"

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

# ------------------------- Fin de analisis de archivo ---------------------------------------------


# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#    ------     Control de Ventana     -------
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


server_address = ('localhost', 10001)
print >>sys.stderr, 'conectando a %s puerto %s' % server_address
sock.connect(server_address)

try:
     
    # Enviando datos
    message = 'Este es el mensaje.  Se repitio.'
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


