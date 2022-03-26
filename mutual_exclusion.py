import sys


processes = []
process_status = {"resource_name": False, "process_number": 0, "logical_time": 0}


def main(args):
    if len(args) > 1:
        try:
            processes = args[1]
            print(f"The Ricart-Agrawala algorithm will be executed with {processes} processes.")
            var = True
            while var:
                command = input("Input a command line: ")
        except :
            print("Enter a valid number of processes.")
    else:
        print("No argument was given")

if __name__ == "__main__":
    main(sys.argv)