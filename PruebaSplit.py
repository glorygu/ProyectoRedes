
#prueba


package_list = []

def clear_list():
    size = len(package_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del package_list[size-iterator]
        iterator += 1

def split_packages (initial_package):
    iterator = 0
    size = len(initial_package)
    clear_list ()
    while (iterator < size):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_package = "#"
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#'):
                #print initial_package[iterator]
                current_package += initial_package[iterator]
                iterator += 1
            package_list.append(current_package)
        else:
            iterator+=1


inputU = raw_input("Palabra: ")

split_packages(inputU)

for index in range(len(package_list)):
    print 'Paquete: ', package_list[index]
    
clear_list()

for index in range(len(package_list)):
    print 'Paquete: ', package_list[index]

            
