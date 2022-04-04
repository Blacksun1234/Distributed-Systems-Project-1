# Distributed-Systems-Project-1

## Requirements
- Python version 3.X (We used 3.9)
- sockets
- _thread


## How to run the program
Run ```python3 main.py <number of nodes>```

  
## Issues Encountered
When running the experiments on MacOS(2015), we noticed that randomly some messages are lost before arriving to destination. This causes some nodes no to get the responses needed therefore, they are stuck in waiting (in the current state). Several trials were performed but the source of the issue was not found, but a guess could that the used computer does no support the executions. Even though the algorithm work perfectly. This issue causes the program to stuck.

<p align="center">
  <img src="https://github.com/Blacksun1234/Distributed-Systems-Project-1/blob/main/issues.png" width="900" alt="Preview" />
</p>

- The pink zone shows when the node P2 has released the critica section and send "ok" message to the node connected and waiting for the critical section to be released.
- The green zone shows the P2 changing state from HELD to DO NOT WANT. This experiment can be clearly seen on the first video try.
- The 2 blue zones show how P1 didn't received the "ok" message due to the fact that the message was lost after succefully being sent by P2.


<p align="center">Made with ❤ by Perseverance Ngoy and Emmanuel Cousin</p>

## Links to experiments
- Experiment 1: https://drive.google.com/file/d/1ADY76kBftTAavW4xBq7tCo_dATIAeU5H/view?usp=sharing
- Experiment 2: https://drive.google.com/file/d/1uERIyezMOuzWR6KyjSmI_vJ2MRhi35hJ/view?usp=sharing
- Experiment 3: https://drive.google.com/file/d/1rQgwJ6LVbTpRtbOl9-i8DXZZ2NWpCorg/view?usp=sharing

## Link to the Apache Zookeeper ruuning experiment

- https://drive.google.com/file/d/1MwfkiPyYLtxv-8di12GYO3cvy3GTKOU3/view?usp=sharing

## The base of our sockets communication relied upon the implementation from:
- https://github.com/macsnoeren/python-p2p-network

