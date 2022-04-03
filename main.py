import sys
import time
import _thread
import random
from node import Node
from state import State
from utilities import build_data, extra_data

node_message = {}

# Using the callback we are able to see the events and messages of the Node
def node_callback(event, main_node, connected_node, data):
    global message
    global node_message
    try:
        if event == "node_message":
            message = event + ":" + main_node.id + ":" + connected_node.id + ":" + str(data)
            # node_message[main_node.id] = message
        if event == "ask_cs":
            pass
        if event == 'ok_message':
            pass
        if event == "want_message":
            pass

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
        node = Node(port, "NODE_id_" + str(node_id+1))
        port += 1
        node.start()
        sockets.append(node)
    
    # Connect all the nodes to each other
    make_connections(sockets)

    running = True

    # agrawala(sockets)
    _thread.start_new_thread(agrawala, (sockets, running, number_of_processes))
    
    while running:
        inp = input("Enter command (list) (Exit command to quit): ").lower()
        cmd = inp.split(" ")

        command = cmd[0]


        if command == 'list':
            for node in sorted(sockets, key=lambda node: node.id):
                print(str(node.id), node.state.name, str(node.logical_time), " msg rec: ", node.message_count_recv)
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
        random_p = random.randint(5, p)
        node.logical_time = random_p

def time_cs(sockets, cs):
    for node in sorted(sockets, key=lambda node: node.id):
        node.cs = random.randint(10, cs)


def read_send_back():
    pass


def agrawala(sockets, running, number_of_processes):
    # print(f"Ricart-Agrawala begining with {number_of_processes} processes!")
    while running:
        for node in sorted(sockets, key=lambda node: node.id):
            if node.state == State.DO_NOT_WANT:
                time.sleep(node.logical_time)
                node.state = State.WANTED
                node.send_to_nodes(build_data("ask_cs", node.id, node.logical_time, node.port))
                

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
