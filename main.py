import sys
import datetime
import _thread
import time
import random

from state import State


# global variables
processes = []
system_start = datetime.datetime.now()
resources = "MYRESOURCES"
message = {}


class CriticalSection():
    def __init__(self) -> None:
        self.time = 10


class Process:
    def __init__(self, id, logical_time):
        self.id = id
        self.logical_time = logical_time
        self.elections = 0
        self.time_start = time
        self.set_time = time
        self.t = 5
        self.state = State.DO_NOT_WANT

    # starts a thread that runs the process
    def start(self):
        _thread.start_new_thread(self.run, ())
    
    # Change the state of the process
    def change_state(self):
        pass


    def run(self):
        # with 5 second interval, update clock
        while True:
            time.sleep(5)
            # self.update_clock()


def tick(running, processes):
    # program ticks evey second to reduce the time out by a second
    # to update all the processors time out

    while running:
        time.sleep(1)
        for p in processes:
            # Update all processors time - out
            p.t -= 1

            


def list(processes):
    # utility method to list proceeses
    for p in processes:
        print(f"P{str((p.id))}, {p.state.name}, {p.t}")


def time_p(processes, t):
    for p in processes:
        random_t = random.randint(5, t)
        p.t = random_t
        


def main(args):
    # main program function
    if len(args) > 1:
        try:
            # get the number of processes from terminal
            number_of_processes = int(args[1])

            for p in range(number_of_processes):     
                processes.append(Process(p+1, 0))
        except:
            print("[ERROR] Failed to parse the input argument.")

        print("Commands: list, time-cs (t), time-p (t), exit")
    else:
        print("Please run the program with the number of processes!")

    # start threads of all processes
    for p in processes:
        p.start()

    # start the main loop
    running = True

    # start a separate thread for system tick
    # _thread.start_new_thread(tick, (running, processes))

    while running:
        inp = input().lower()
        cmd = inp.split(" ")

        command = cmd[0]

        if len(cmd) > 3:
            print("Too many arguments")

        # handle exit
        elif command == "exit":
            running = False

        # handle list
        elif command == "list":
            try:
                list(processes)
            except:
                print("Error in list")

        # handle kill
        elif command == "time-p":
            try:
                print("Command line ", int(cmd[1]))
                time_p(processes, int(cmd[1]))
            except:
                print("Error in time")


        # handle unsupported command        
        else:
            print("Unsupported command:", inp)

    print("Program exited")


if __name__ == "__main__":
    main(sys.argv)
