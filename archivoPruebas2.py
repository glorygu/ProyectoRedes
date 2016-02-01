# Archivo de pruebas para dos hilos, Intermediario

import threading
import time

# Creacion de sub clase para hilos

class myThread (threading.Thread):
    def __init__(self, name, source, destination, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.source = source
        self.destination = destination
        self.delay = delay
    def run(self):
        print "Inicia el servicio: " + self.name
        print_stadistic(self.name, self.source, self.destination, self.delay)
        print "Fin del servicio " + self.name

# Funcion que imprime las estadisticas del hilo

def print_stadistic(threadName, source, destination, delay):
    number_paquets = 20
    while number_paquets:
        print "Recibi un paquete de " + source + " ---> Reenvio a " + destination
        time.sleep(delay)
        number_paquets -= 1

# Creacion de hilos
thread1 = myThread("Escucha de Cliente - Reenvio a Server", "Cliente", "Server", 1)
thread2 = myThread("Escucha de Server - Reenvio a Cliente", "Server", "Cliente" ,  3)

# Start new Threads
thread1.start()
thread2.start()

