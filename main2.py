import sys
import time
import _thread
import random

from node1 import Node
from state import State
from utilities import make_the_connections



global message
message = []
sockets = []
used_ports = []
resources = False


class MyTestNode (Node):
    def __init__(self, host, port, id):
        self.ownMessage = []
        self.logical_time = 5 + time.monotonic()
        self.timestamp = 0
        self.time_to_hold_cs = 10
        self.state = State.DO_NOT_WANT
        self.queues = []

        super(MyTestNode, self).__init__(host, port, id)
        global message
        message.append("mytestnode started")

    def outbound_node_connected(self, node):
        global message
        message.append("outbound_node_connected: " + node.id)
        
    def inbound_node_connected(self, node):
        global message
        message.append("inbound_node_connected: " + node.id)

    def inbound_node_disconnected(self, node):
        global message
        message.append("inbound_node_disconnected: " + node.id)

    def outbound_node_disconnected(self, node):
        global message
        message.append("outbound_node_disconnected: " + node.id)

    def node_message(self, node, data):
        global message
        self.ownMessage.append(self.id + " node_message from " + node.id + ": " + str(data) + " port: " + str(node.port))

        # Nodes_inbound: Nodes that are connected to us 
        # Nodes_outbound: Nodes to where we sent connection
        # print(self.id, " has Nodes inbound ", self.nodes_inbound)
        # print(self.id, " has Nodes outbounds ", self.nodes_outbound)
        # print(self.id, " My current monotonic ", time.monotonic())


        # check if the I (receiver) has already the resource
        if self.state.name == 'HELD':
            print(self.id, " is in state ", self.state)
            self.queues.append(str(data))

        # check if I (self.id) want to access as well:
        elif self.state.name == 'WANTED':
            sender_timestamp = float(data.split(",")[2])
            if self.timestamp > sender_timestamp:
                # send ok because sender timestamp is less than mine

                new_msg = "ok" + "," + self.id + "," + str(time.monotonic())
                self.send_to_node(node, new_msg)

                if node in self.nodes_inbound:
                    # n.send(data)
                    # print(self.id, " has ", node.id, "in is nodes_inbound")
                    pass
                
                if node in self.nodes_outbound:
                    # print(self.id, " has ", node.id, "in is nodes_outbound")
                    pass
            else:
                self.queues.append(str(data))

        # if the receiver not accessing the resource
        elif self.state.name == 'DO_NOT_WANT':
            # Reply to node by sending ok, because I do not want to access the critical section
                new_msg = "ok" + "," + self.id + "," + str(time.monotonic())
                self.send_to_node(node, new_msg)


        # if len(self.nodes_inbound) != 0:
        #     for n in self.nodes_inbound:
        #         self.send_to_node(n, "ok")
        #         time.sleep(2)
        # if len(self.ownMessage) > 0:
        #     self.send_to_nodes('ok')
        #     time.sleep(2)
   
        print(self.ownMessage)
        
    def node_disconnect_with_outbound_node(self, node):
        global message
        message.append("node wants to disconnect with oher outbound node: " + node.id)
        
    def node_request_to_stop(self):
        global message
        message.append("node is requested to stop!")


def tick(running, node):
    # Runs this program for every thread to update the time
    alread_sent = True

    count_response = 0 

    while running:
        # time.sleep(1)
        time.sleep(node.logical_time)
        node.state = State.WANTED
        my_id = node.id
        send_time = time.monotonic()
        new_msg = "resource" + "," + node.id + "," + str(send_time)
        
        # number of nodes to where we are sending the messages
        num_node = len(sockets) - 1
        

        # Send messages to other nodes for accessing the critical section
        for node in sockets:
            if node.id == my_id:
                if alread_sent:
                    node.send_to_nodes(new_msg)
                    node.timestamp = send_time
                    time.sleep(5) 
                    alread_sent = False

                    # Wait for all the reply, then check the incoming messages
                    messages = node.ownMessage
                    print(node.id, " From while: ", messages)
                    for msg in messages:
                        response = msg.split(':')[1].split(",")[0]
                        print(node.id, " This is response ---> ", response)
                        if str(response) == "ok":
                            count_response += 1
                    
                    print(node.id, " number of ok responses: ", count_response)
                    # Check if the number of responses is equal to the number of send messages
                    if num_node == count_response:
                        node.state = State.HELD
                        time.sleep(node.time_to_hold_cs)
                        node.state = State.DO_NOT_WANT






def start(args):

    port = 10001
    number_of_processes = int(args)
    
    for node_id in range(number_of_processes):
        node = MyTestNode(host="127.0.0.1", port=port, id="P" + str(node_id+1))
        used_ports.append(port)
        port += 1
        node.start()
        sockets.append(node)
    

    # Node 1 connect to other nodes
    make_the_connections(sockets)

    running = True

    for node in sockets:
        # start a separate thread for every node to control their logical time
        _thread.start_new_thread(tick, (running, node))


    while running:
        inp = input("Enter command (list) (Exit command to quit): ").lower()
        cmd = inp.split(" ")

        command = cmd[0]

        if command == 'list':
            for node in sorted(sockets, key=lambda node: node.id):
                print(str(node.id) + " " + str(node.state.name) + " MSG R: " + str(node.message_count_recv))
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


def get_usage():
    print("Usage: python main.py <number of processes>")
    sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        get_usage()
    else:
        start(sys.argv[1]) 

