# Jonestown
Build your business and trade your way to wealth!

This is my most ambitious project, and is very much a work in progress. The player currently doesn't have much interaction in the game, but the backend is very developed.

The game consists of a town, Jonestown, with tens of thousands of residents. These people find jobs, work, buy food, and go to church. Most importantly, they talk to one another, sharing information about stores and manufacturies. A person can only shop or look for jobs at stores that they have already heard about from another person.

This creates a fractured market with inherent inefficiencies. Information has enormous value, as does who you know. Perhaps a farmer produced too much wheat this year, and is selling it at a markdown- if you're the only brewer who knows them you'll have the cheapest beer in town. Perhaps someone has been shopping at an expensive store- if they hear about your prices, they'll come to you instead. 

But there's another side to that- it doesn't matter how good your prices are if no one has heard of you. And you'll have competition- the AI is running businesses too, and they're pretty good at it.

TL;DR To get a look at the AI in action, start up the game and watch your own business. Currently player businesses are handled by the same AI that manages other businesses. You can also poke around the backend to see how things work- I'd recommend the pricing algorithm in People and the conversation handler in Conversation in particular, as well as the Ai module.

# INSTALLATION

You'll need Python 3, with the following packages:  
matplotlib  
numpy  
tkinter  
transitions (written by tyarkoni)  

# TO RUN

python3 main.py
