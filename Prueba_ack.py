


inputB = raw_input("ACK recibidos: ")

received_acks_list = []
#sended_segments = [1,2,3,4,5,6]

def clear_list():
    size = len(received_acks_list) 
    iterator = 1
    while iterator <= size:
        #print str(iterator)
        del received_acks_listinput_list[size-iterator]
        iterator += 1

def extract_acks (initial_package):
    iterator = 0
    size = len(initial_package)
    clear_list()
    while (iterator < size):
        #print initial_package[iterator]
        if initial_package[iterator] == '#':
            current_ack = ""
            iterator += 1
            while (iterator < size and initial_package[iterator] != '#'):
                #print initial_package[iterator]
                current_ack += initial_package[iterator]
                iterator += 1
            received_acks_list.append(current_ack)
        else:
            iterator+=1



clear_list()
message_received = socket_intermediario.recv(1000)
extract_acks(message_received)

for index in range(len(received_acks_list)):
    for iterator in range(len(sended_segments)):
        if received_acks_list[index] == sended_segments[iterator]:
            sended_segments[iterator] = 0
            

            




