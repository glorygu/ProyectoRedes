import sys

list1, list2, list3, list4, list5 = [900,566,433,200,556,4555,4345,7], [1,2,3,4], [55,865467,434444,3], ['a','c','d','e'], [int("1"), int("2"), int ("55")]

print "El minimo es: "+ str(min(list1))
print "El minimo es: "+ str(min(list2))
print "El minimo es: "+ str(min(list3))
print "El minimo es: "+ str(min(list4))
print "El minimo es: "+ str(min(list5))


def clear_list(input_list):
    size = len(input_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del input_list[size-iterator]
        iterator += 1
        
clear_list(list3)
print str(len(list3))
clear_list(list1)
print str(len(list1))
clear_list(list1)


print "---------------------------------------Prueba--------------------------------------"
content_list = ["P", "r", "o", "y", "e", "c", "t", "o"]
window_size = input ("Ingrese tamano de ventana: ")
content_iterator = 0
sec_num = 1
while (content_iterator < len(content_list)):
    acked_segs = 0
    window_start = content_iterator
    window_end = content_iterator + window_size
    print "La ventana va de la posicion " + str(window_start) +" a la posicion " + str(window_end)
    for it in range (0, window_size):
    #Enviando contenidos de la ventana
        if (content_iterator+it < len(content_list)):
            package = "#"+ str(sec_num)+":"+content_list [content_iterator+it]
            #sock.send(package)
            print ("Enviando "+ package)
            sec_num = sec_num + 1
            
    print "Ultimo numero de secuencia: "
    min_ack = input("ACK mas pequenio: ")
    if min_ack <= window_end and min_ack >= window_start:
        acked_segs = min_ack - window_start
        sec_num = min_ack + 1
    else:
        acked_segs = 0
        sec_num = window_start + 1
        
    print "ACKed segs " + str(acked_segs) + "sec_num: "+ str(sec_num)        
    content_iterator = content_iterator + acked_segs
    print "current value of content_iterator: ", content_iterator
        