#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Programa Servidor
# Fuente original de este codigo: www.pythondiario.com
# Utilizado para fines academicos en el curso CI-1320 

import socket
import sys
 
# Creando el socket TCP/IP
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Enlace de socket y puerto
client_port = input("Introduzca el puerto para comunicarse con el cliente:  ")
server_port = input ("Introduzca puerto para comunicarse con el servidor: " )
#client_port = 10001
server_address = ('localhost', client_port) #con cliente
print >>sys.stderr, 'empezando a levantar %s puerto %s' % server_address
sock.bind(server_address)



# Escuchando conexiones entrantes
sock.listen(1)
 
while True:
	# Esperando conexion
	print >>sys.stderr, 'Esperando para conectarse'
	connection, client_address = sock.accept()

	try:
		print >>sys.stderr, 'concexion desde', client_address

		# Recibe los datos en trozos y reetransmite
		while True:
			data = connection.recv(1000)
			print >>sys.stderr, 'recibido "%s"' % data
			if data:
				sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				server_address = ('localhost', server_port)
				print >>sys.stderr, 'conectando a %s puerto %s' % server_address
				sock2.connect(server_address)

				try:
					message = data
					print >>sys.stderr, 'enviando al servidor"%s"' % message
					sock2.send(message)
					
					#print 'Enviando puerto al servidor' 
					try:
						amount_received = 0
						amount_expected =1# len(message)
						while amount_received < amount_expected:
							data = sock2.recv(19)
							amount_received += 1 #len(data)
							print >>sys.stderr, 'recibiendo "%s"' % data
							connection.send(data)
							print "Enviando " +data +" al cliente"
							
					finally:
						print 'listo'
				finally:
					print >>sys.stderr, 'cerrando socket'
					#sock2.close()
			else:
				print >>sys.stderr, 'no hay mas datos', client_address
				break

	finally:
		# Cerrando conexion
		# connection.close()
		# sock2.close()
		print 'nada2'