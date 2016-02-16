import sys
import random

probability = input ("Introduzca la probabilidad de perdida de paquetes: ") 

random_number = random.randint(100,10000) * 0.010

if random_number >= probability:
    print "Se envia paquete: " + str(random_number)
else:
    print "Se pierde el paquete: " + str (random_number)
