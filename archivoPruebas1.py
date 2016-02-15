import time
import sys

# Archivo de prueba para Timer de Cliente

def correr_timer():

    time_start = time.time()
    millis = int(round(time.time() * 1000))
    keep_running = True
    
    while keep_running:
        try:
            millis = float(round(time.time() - time_start, 4)) * 1000
            if millis >= user_miliseconds:
                sys.stdout.write("\r{millis} MiliSegundos transcurridos\n".format(millis=millis))
                print "Se reenvia la ventana"
                keep_running = False
        except KeyboardInterrupt, e:
            break



user_input = input("Escriba la cantidad de milisegundos que desea: ")
user_miliseconds = float(user_input)

while True:
    correr_timer()



    
    
    
    
    
    
    
    
    
    
    
    