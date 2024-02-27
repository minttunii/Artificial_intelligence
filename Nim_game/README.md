This program implements Nim game againts AI, where the AI is 
though to play Nim through reinforcement learning.
The reinforcement learning is implemented by Q-learning. 

Nim is a two person game, and the players has alternate turns. 
The game consist of piles of sticks, as shown below.

Nim game has the following starting state:

                |                       Stack 0
            |   |   |                   Stack 1
        |   |   |   |   |               Stack 2
    |   |   |   |   |   |   |           Stack 3

The player can take any number of sticks from one of the stacks 0-3.
The loser of the game is the one to draw the last stick left.
In order to win the game, the player needs to think about their strategy.

The AI learns the game fairly good with Q-learning, and it is hard to win against it. 
