Communication: https://discord.gg/eBEQYVdSa8

Project description:  
A CLI based game about ancient seas and trade. Have you ever been bored in a console? If you're anything like me, you sure have, but all of the console games are too basic or too complex. I aim for a happy medium: an enjoyably challenging game about networks, something we devs sure enjoy (I see u Factorio players).

AI use:  
1. Less than 30% of my project is AI, but I prefer to be transparent  
2. I have one rule using AI: Never use AI if you don't understand (or learn) its code. Let's break it down: Repetitive simple tasks? Let Co-Pilot handle it. Logic that you are too lazy to implement? ChatGPT can give you an outline. That said, if you refuse to read or understand the code that AI writes, you aren't doing yourself a favour; you are just obstructing your learning.  
  
How to run:  
1. Clone this repo (run where you want the files to end up)  
`git clone https://github.com/Unlisted27/merchanteer`  
2. Go to the correct folder   
`cd merchanteer`  
3. Run merchanteer.py  
`python3 merchanteer.py`  

Code structure (LOOK HERE IF YOU WANNA UNDERSTAND IT)  
Merchanteer is divided into 3 main files, and then a few helpers. The files are:
 - merchanteer.py  
    This file is basically just the __main__ method, it runs the initial setup for the game, and then launches into the main game menu
 - building_blocks.py  
    This file will give you the best idea of how the game is coded. All of the things in the game are created here using custom objects that are all defined in components.py
 - components.py  
    This is the back end of the game, where all of the objects used are defined. This is the really deep stuff, not easy to understand without understanding the higher level stuff first

