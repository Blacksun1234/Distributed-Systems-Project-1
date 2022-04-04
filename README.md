# Distributed-Systems-Project-1

## Requiered
Python version 3.X (We used 3.9)

## How to use
Start the program with the command ```python3 main.py <number of nodes>```
- This will creat the specified number of nodes
- Create the connections between thoses nodes
- Start the Ricart-Agrawala algorithm
  
## Isuues Encountered
<p align="center">
  <img src="https://github.com/Blacksun1234/Distributed-Systems-Project-1/blob/main/issues.png" width="900" alt="Preview" />
</p>

- The pink zone shows when the node P2 has released the critica section and send "ok" message to the node connected and waiting for the critical section to be released.
- The green zone shows the P2 changing state from HELD to DO NOT WANT. This experiment can be clearly seen on the first video try.
- The 2 blue zones show how P1 didn't received the "ok" message due to the fact that the message was lost after succefully being sent by P2.


<p align="center">Made with ❤ by Perceverance  and Emmanuel Cousin</p>
