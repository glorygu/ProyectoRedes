#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Cliente
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
import sys
import time

user_input = input("Escriba la cantidad de milisegundos que desea: ")
user_miliseconds = float(user_input)



# ---------------- creacion de socket

# Creando un socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
 
# Conecta el socket en el puerto cuando el servidor esté escuchando
server_address = ('localhost', 10001)
print >>sys.stderr, 'conectando a %s puerto %s' % server_address
sock.connect(server_address)

# ---------------------------------



# --------------------------- envio de msj

def correr_timer(mensaje, numero):
    time_start = time.time()
    millis = int(round(time.time() * 1000))
    keep_running = True
    
    while keep_running:
        try:
            millis = float(round(time.time() - time_start, 4)) * 1000
            if millis >= user_miliseconds:
                sys.stdout.write("\r{millis} MiliSegundos transcurridos\n".format(millis=millis))
                # print "Se reenvia la ventana"
                
                # Enviando datos
                message = mensaje +" "+ str(numero)
                # print >> "Enviando mensaje: "+message
                sock.sendall(message)
                
                keep_running = False
        except KeyboardInterrupt, e:
            break

# --------------------------------------------

try:
    
    contador = 1
    
    while True:
        correr_timer("Hola Mundo", contador)
        
        contador += 1
 
finally:
    print >>sys.stderr, 'cerrando socket'
    sock.close()


