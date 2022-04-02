import sys
import time
import _thread
from node import Node
from state import State



# Using the callback we are able to see the events and messages of the Node
def node_callback(event, main_node, connected_node, data):
    global message
    try:
        if event == "node_message":
            message = event + ":" + main_node.id + ":" + connected_node.id + ":" + str(data)

    except Exception as e:
        message = "exception: " + str(e) 


def make_connections(sockets):
    for node_i in sorted(sockets, key=lambda node: node.id):
        for node_j in sorted(sockets, key=lambda node: node.id):
            if node_i.id != node_j.id:
                node_i.connect_with_node("localhost", node_j.port)


def start(args):
    
    port = 8001
    sockets = []

    number_of_processes = int(args)
    
    for node_id in range(number_of_processes):
        node = Node(port, "NODE_id_" + str(node_id+1), callback=node_callback)
        port += 1
        node.start()
        sockets.append(node)
    
    # Connect all the nodes to each other
    make_connections(sockets)

    running = True

    # agrawala(sockets)
    _thread.start_new_thread(agrawala, (sockets, running))
    
    while running:
        inp = input("Enter command (list) (Exit command to quit): ").lower()
        cmd = inp.split(" ")

        command = cmd[0]


        if command == 'list':
            for node in sorted(sockets, key=lambda node: node.id):
                print(str(node.id), node.state.name, str(node.logical_time))
        # elif command == 'send':
        #     for node in sorted(sockets, key=lambda node: node.id):
        #         if node.id == 'NODE_id_1':
        #             node.send_to_nodes({"message": "Hi from node 1!"})
        #             time.sleep(1)
            
        #     for node in sorted(sockets, key=lambda node: node.id):
        #         if node.id != 'NODE_id_1':
        #             print("Message received ", node.message_count_recv)
        #             # node.node_message()
        elif command == "time-p":
            time_p(sockets, int(cmd[1]))
        
        elif command == "time-cs":
            time_cs(sockets, int(cmd[1]))

        elif command == 'exit':
            for node in sockets:
                node.stop()
            print("Program Terminated Successfully! Please wait for all the nodes to stop...")
            sys.exit()
        else:
            print("Invalid command! Please try again...")


def time_p(sockets, p):
    for node in sorted(sockets, key=lambda node: node.id):
        node.logical_time = p

def time_cs(sockets, cs):
    for node in sorted(sockets, key=lambda node: node.id):
        node.cs = cs

def agrawala(sockets, running):
    # print("Ricart-Agrawala begining!")
    while running:
        for node in sorted(sockets, key=lambda node: node.id):
            if node.state == State.DO_NOT_WANT:
                time.sleep(node.logical_time)
                node.state = State.WANTED
                #toto send messages
            elif node.state == State.HELD:
                time.sleep(node.logical_time)
                node.state = State.DO_NOT_WANT
                #todo wait time p
        

def get_usage():
    print("Usage: python main.py <number of processes>")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        get_usage()
    else:
        start(sys.argv[1]) 


