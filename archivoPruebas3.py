# Archivo pruebas introduccion de Cliente, Intermediario, Servidor

import sys


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

# -------------------- Servidor --------------------

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

# -------------------- Intermediario --------------------

print "-----------------------------------------------------"
print "    Bienvenido a Simulacion de Red 2016 - Intermediario"
print "-----------------------------------------------------"
print "\n\n"
print "A continuacion ingrese los datos que se le solicitan"
print "\n\n"

# Variables de ingreso de datos

inter_server_port = input("Introduzca el puerto de escucha del servidor: ")
inter_client_port = input("Introduzca el puerto de escucha del cliente: ")
probability = input("Introduzca la probabilidad de perdida de paquetes: ")

# Modo de trabajo

print "-----------------------------------------------------"
print "    Antes de iniciar, por favor indique el modo de ejecucion"
user_mode = input(" (1) Modo Normal (2) Modo Debug :  ")
print "\n\n"









