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
user_miliseconds = float(user_time)

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"
 
 
# ----------------- Apertura de archivo para envio ----------------------------------------------

print "Analizando archivo: ", file_name
# time.sleep(2)
print "..."
# time.sleep(2)
print "..."
print "Fin de análisis, archivo seguro"
# time.sleep(2)
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

# ------------------------- Fin de analisis de archivo -------------------------


# ---------------- Creacion de socket hacia Intermediario ----------------------


socket_intermediario = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(inter_port)
server_address = ('localhost', port)
print >>sys.stderr, 'conectando a %s puerto %s' % server_address
socket_intermediario.connect(server_address)

# ------------------------------------------------------------------------------




# ---------------- Funcion para envio de mensajes a Intermediario --------------

def run_timer(mensaje, numero):
    time_start = time.time()
    millis = int(round(time.time() * 1000))
    keep_running = True
    
    while keep_running:
        try:
            millis = float(round(time.time() - time_start, 4)) * 1000
            if millis >= user_miliseconds:
                sys.stdout.write("\r{millis} MiliSegundos transcurridos\n".format(millis=millis))
                
                message1 = "#"+str(numero)+":H"
                message2 = "#"+str((numero+1))+":o"
                message3 = "#"+str((numero+2))+":l"
                message4 = "#"+str((numero+3))+":a"
                socket_intermediario.sendall(message1)
                socket_intermediario.sendall(message2)
                socket_intermediario.sendall(message3)
                socket_intermediario.sendall(message4)
                
                # Se escucha si fueron recibidos los mensajes ---
                
                message_received = socket_intermediario.recv(1000)
                print >>sys.stderr, 'Mensaje recibido: "%s"' % message_received
                
                # connection, client_address = sock.accept()
                # message_received = connection.recv(1000)
                # print >>sys.stderr, 'Mensaje recibido: "%s"' % message_received
                
                # -----------------------------------------------
                
                keep_running = False
        except KeyboardInterrupt, e:
            break
# ------------------------------------------------------------------------------

try:
    
    contador = 1
    
    while True:
        
        run_timer("Hola Mundo", contador)
        contador += 4
        
 
finally:
    print >>sys.stderr, 'cerrando socket'
    socket_intermediario.close()