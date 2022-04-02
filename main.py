import sys
import time
from node import Node


message = "critical"


# Using the callback we are able to see the events and messages of the Node
def node_callback(event, main_node, connected_node, data):
    global message
    try:
        if event == "node_message":
            message = event + ":" + main_node.id + ":" + connected_node.id + ":" + str(data)

    except Exception as e:
        message = "exception: " + str(e) 


def start(args):
    
    port = 8001
    sockets = []

    number_of_processes = int(args)
    
    for node_id in range(number_of_processes):
        node = Node(port, "NODE_id_" + str(node_id+1), callback=node_callback)
        port += 1
        node.start()
        sockets.append(node)

    running = True
    
    while running:
        command = input("Enter command (list) (Exit command to quit): ").lower()
        

        if command == 'list':
            for node in sorted(sockets, key=lambda node: node.id):
                print(str(node.id))
        elif command == 'send':
            for node in sorted(sockets, key=lambda node: node.id):
                if node.id == 'NODE_id_1':
                    node.connect_with_node("localhost", 8002)
                    time.sleep(2)

                    node.send_to_nodes("Hi from node 1!")
                    time.sleep(1)
                    node.node_message
                    print(node.id, " bound to ",node.nodes_outbound)
        elif command == 'exit':
            for node in sockets:
                node.stop()
            print("Program Terminated Successfully! Please wait for all the nodes to stop...")
            sys.exit()
        else:
            print("Invalid command! Please try again...")

            

def get_usage():
    print("Usage: python main.py <number of processes>")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        get_usage()
    else:
        start(sys.argv[1])        


