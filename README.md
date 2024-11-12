# Jonestown
Build your business and trade your way to wealth!

The game consists of a town, Jonestown, with tens of thousands of residents. These people find jobs, work, buy food, and go to church. Most importantly, they talk to one another, sharing information about stores and manufacturies. A person can only shop or look for jobs at stores that they have already heard about from another person.

This creates a fragmented market with inherent inefficiencies. Information has enormous value, as does who you know. If someone has been shopping at an expensive store hears about your prices, they'll come to you instead. But there's another side to that- it doesn't matter how good your prices are if no one has heard of you. And you'll have competition- the AI is running businesses too, and they're pretty good at it.

I think it's neat, but fair warning, it isn't very fun. Mostly you just decide what to manufacture (your choices are bread and chairs- I recommend bread). You can poke around the backend to see how things work- I'd recommend the pricing algorithm in People and the Conversation module in particular, as well as the Ai module.

# INSTALLATION

You'll need Python 3, with the following packages:  
matplotlib  
numpy  
tkinter  (`sudo apt-get install python3-tk` and `sudo apt-get install python3-pil.imagetk`)  
transitions (written by tyarkoni)  

# TO RUN

python3 main.py

The AI controls your business by default. I recommend you leave it that way unless you know what you're doing (I don't). 

The AI will build units for you during the first day, so run a day when the game begins before doing anything.

Each unit has a ledger- this is the best place to see what's going on.
