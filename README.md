# BetterBettingBot
Monte Carlo Simulation for Crash Games

The project consists of several layers.

First layer is a simple Monte Carlo Simulation of the popular crash games such as Ethcrash.io, Zcrash.io and Bustabit.

The project contains a simple script designed to scrape the previous crash points for these games. This data is then used within the rest of the project in order to perform simulations as accurate as possible.

The Monte Carlo simulations are then to be used as the fitness testing for a genetic algorithm. This implementation should theoretically allow for the generation of a number of strategies which will either proove that the game is beatable, or that these games can never be reliably and consistently beaten due to the house edge of 1%.

The entire project is written in Python, however, depending upon the results of the project, I will look to implement the strategies in JS to allow for automated game play.

Project contains 4 files. 

Current main loop will complete the monte carlo simulation. There is a graph plotted in matplotlib upon completion. Current Crude selection is average performance of the agents winning rate and ratio of agents which are winning.

Please contribute any suggestions/code :)
