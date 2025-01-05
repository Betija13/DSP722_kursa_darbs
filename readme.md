Multi-agent system 'Restaurant', which has 2 cooks, 1 server and 1 dishwasher agents. Made with MaSE methodology and implemented in PADE. 
## Documentations
PADE documentation: https://pade.readthedocs.io/en/stable/index.html

PADE github: https://github.com/grei-ufc/pade

Paper about PADE: https://onlinelibrary.wiley.com/doi/10.1002/2050-7038.12012

MaSE: 

agentTool (tool for MaSE): https://agenttool.cs.ksu.edu/index-2.html

## Setup

First set up your environment, i did this: create new env, with python 3.8 (technically pade is on 3.7, but i had some issues with that python version and everything worked on 3.8)
`micromamba create -n ds722_kd python=3.8
micromamba activate ds722_kd
`

To install PADE run this command in terminal:
`git clone https://github.com/greiufc/pade
cd pade
python setup.py install`


then run this (idk mby this is optional):
`pade create-pade-db`

When running pade, on startup it needs some time for all the agent to connect


## Running the system

To change main setting go to
* ClientBehaviour to change time (however advised not to put time under 10 seconds, as the system needs startup time) and to change the recepies
* Go to Workarea and change ... for different scenarios

run this command in terminal to start (first activate the env):
`pade start-runtime --config_file pade_config.json`

then open http://localhost:5000/ to see the agents in action
Go to ... -> .. to see diagram
you can also see the full diagram here http://localhost:5000/messages_diagram (this dos not automatically refresh, as it might be a problem if there is a lot of messages sent)


You can also run this command and see the latest(?) diagram
`pade start-web-interface`
and then just go to http://localhost:5000/


