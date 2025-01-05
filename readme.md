Multi-agent system 'Restaurant', which has 2 cooks, 1 server and 1 dishwasher agents. Made with MaSE methodology and implemented in PADE. 
## Documentations
PADE documentation: https://pade.readthedocs.io/en/stable/index.html

PADE github: https://github.com/grei-ufc/pade

Paper about PADE: https://onlinelibrary.wiley.com/doi/10.1002/2050-7038.12012

MaSE: Presentation from course (https://estudijas.rtu.lv/mod/resource/view.php?id=5030267)

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

###### IMPORTANT:

**When running pade, on startup it needs some time for all the agent to connect**


## Running the system

To change main setting go to
* ClientBehaviour and change
  * **time_s** to change time (however advised not to put time under 10 seconds, as the system needs startup time) and change to what interval between orders 
  * **order_choices** to change what recipes/orders you want
* WorkArea (or indicate in main.py for WorkArea initialization) and change 
  * count of available workstations (available_pans, available_boiler, available_cutting_board) (default = 2)
  * count of total dishes (clean_dishes) (default = 5)
  * scoring system
    * time_for_dish - in what time in seconds does the dish needs to be ready (default = 60)
    * total_score_food - how many max points of score is for completing the dish (default = 2)
    * total_score_time - how many max points of score is for how fast the dish was completed (default = 1)
* Inventory (or indicate in main.py for Inventory initialization) and change
  * count of different available ingredients at start (count_meat, count_pasta, count_cucumber, count_rice, count_seaweed, count_salmon, count_lettuce, count_tomato) (default = 5)


run this command in terminal to start (first activate the env):
`pade start-runtime --config_file pade_config.json`

then open http://localhost:5000/ to see the agents in action

Go to 'Messages' -> 'Messages Diagram View' to see diagram

you can also see the full diagram here http://localhost:5000/messages_diagram (this does not automatically refresh, as it might be a problem if there is a lot of messages sent)


You can also run this command and see the latest(?) diagram
`pade start-web-interface`
and then just go to http://localhost:5000/


