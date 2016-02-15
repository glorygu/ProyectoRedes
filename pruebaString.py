import sys
message_to_send = ""
def iterate_through_string(message):
    message_to_send = ""
    iterator = 0
    ack_not_found = True 
    while iterator < len (message) and ack_not_found:
        if (message[iterator] == '#'):
            iterator+=1
            while (message[iterator] != ':'):
                message_to_send += message[iterator]
                iterator+=1
        if message[iterator] == ':':
            ack_not_found = False
        iterator+=1
    print message_to_send
    return message_to_send

result = iterate_through_string("#995:d")
print iterate_through_string("#2:b")
print result

def clear_list(input_list):
    size = len(input_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del input_list[size-iterator]
        iterator += 1
        
ack_list = []
def extract_acks (initial_package):
    iterator = 0
    size = len(initial_package)
    clear_list(ack_list)
    while (iterator < size):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_ack = ""
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#' and initial_package[iterator] != ':'):
                #print initial_package[iterator]
                current_ack += initial_package[iterator]
                iterator += 1
            ack_list.append(current_ack)
        else:
            iterator+=1
    return ack_list

package_list = []
def split_packages (initial_package):
    iterator = 0
    size = len(initial_package)
    clear_list (package_list)
    while (iterator < size):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_package = "#"
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#' ):
                #print initial_package[iterator]
                current_package += initial_package[iterator]
                iterator += 1
            package_list.append(current_package)
        else:
            iterator+=1
    

split_packages("#1:H#2:o#3:l#4:a") 
split_packages("#100:H#200:o#300:l#400:a") 
it = 0
while it<len(package_list):
    print package_list[it]
    it+=1