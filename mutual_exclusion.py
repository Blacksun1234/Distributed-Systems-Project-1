import sys

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

if __name__ == "__main__":
    main(sys.argv)