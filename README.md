# Zardo's Event Completer

This is a python script to automate the process of completing Poketwo's New event quests! The code might be a bit shabby and buggy due to me speedcoding it! Open an issue and I'll see what I can do

## Features
- Fully Automated
- Donates Ingredients
- Crafts recipes and completes orders
- Excellent Error Handling
- Sexy Logger
## How it works?
1. It sends `@poketwo event inv` to check its inventory for available ingredients.
2. It calculates what to donate. Since butter is the rarest. We priortise it being used in donations rather than orders.
3. It finally donates everything and is done with phase-1 of the app.
4. It proceeds to run `@poketwo ev` to check for available orders.
5. It uses discord-api to communicate with the drop-down and select orders that dont require butter.
6. It finally sends the recipes and crafts dishes.

## Installation

Please follow the following steps to run this app yourself!

1. **Install Python:** Download Python from [Here](https://www.python.org/downloads/).
2. **Install Libraries:** Download the following listed libraries using ```pip install <library_name>:```
   - discord.py-self
3. **Configuration:**
   - Account Authorization Token on line `7` in `main.py`.
   - ChannelId on line `8` in `main.py`.
4. **Make sure you dont have any active orders on the bot account, If you do please complete them first!**
4. **Run** the file using `python main.py`.



## Note
This code might have bugs or unattended issues. They are primarily because I've not had the time to test the code to it's full potential. However I'm glad to say that It has definetly shown good results. Any further bugs will be fixed once they're brought to my attention.


## Known issues
1. ~~Failure in Regular Expression while obtaining the dish name.~~
2. Buggy in claiming orders.
3. Buggy in Offering more than 15 amounts of butter.

## Snippets 
![image](https://github.com/sleepyzardo/poketwo-event-completer/assets/88527682/2ce5827b-f4d6-4a35-ad27-b531e04eea62)


## ChangeLogs
- Edited Regular Expression to correctly log name of the dish.

# Future-Plans
No such future Plans as of now. Suggestions are welcomed though.



# Copyright Zardo

This code is provided under the following conditions:
1. You may use this code for personal and non-commercial purposes.
2. If you use or modify this code in any way, you must provide clear attribution to Zardo.
3. You may not sell or distribute this code for commercial purposes without explicit permission from Zardo.
