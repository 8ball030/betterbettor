# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 13:05:38 2018

@author: Tom
"""
import tqdm
import random
import matplotlib
import matplotlib.pyplot as plt
from crash_getter import getCrash 

'''
This method returns the result as to whether an input crash target has been hit

@params int  - The target to achieve

@return bool - True if the Crash exceeds the given target
'''

def rollDice(target):
    crash = getCrash()
    if crash == 0:
        return False
    elif crash < target:
        return False
    elif crash >= target:
        return True


'''
This class is a strategy class, it contains all the methods required to test a strategy
'''

class Strategy:
    losing_run = 0
    winning_run = 0
    bust = False 
    
    '''
    Initialisation
    '''
    def __init__(self, initial_balance, base_bet, base_target, recv_mult_b, recv_mult_t, safety_params):
        self.initial_bal = initial_balance
        self.balance = initial_balance
        
        self.base_target = base_target
        self.base_bet = base_bet
        
        self.round_bet = base_bet
        self.round_target = base_target
        
        self.recover_mult_bet = recv_mult_b
        self.recover_mult_target = recv_mult_t
        
        self.safety_params = safety_params
        
    
    '''
    This methods will play the strategy class for a given number of wager_counts
    
    @show    - Bool, Determines whether to plot the strategy
    @wager_count - int Determins the total number of games to trial the strategy
    
    @return - 
    '''
    
    def testStrategy(self, wager_count, show =False):
            
        count_of_busts = 0
        avg_performance = 0     

        # wager X
        wX = []
    
        #value Y
        vY = []
    
        # change to 1, to avoid confusion so we start @ wager 1
        # instead of wager 0 and end at 100. 
        currentWager = 1
    
        #           change this to, less or equal.
        while currentWager <= wager_count:
            if self.balance > self.round_bet:
                if self.bust is False:
                    if rollDice(self.round_target):
                        self.balance += ((self.round_bet * (self.round_target/100))-self.round_bet)
                        # append #
                        
                        self.reset_to_default()
                        self.winning_run +=1
                        self.losing_run = 0
                        #self.increase_stake()                        
                        if show is True:                                
                            wX.append(currentWager)
                            vY.append(self.balance)
                        
                        
                    else:
                        self.balance -= self.round_bet  
                        # append #
                        self.losing_run +=1
                        self.winning_run = 0
                        #self.reset_to_default()
                        self.recovery_strat_3()   
                        
                        if show is True:                                
                            wX.append(currentWager)
                            vY.append(self.balance)
                        
                else:
                    pass
            else:
                self.bust = True
            
    
            currentWager += 1
            if self.round_target > self.safety_params['max_bet_target']:
                self.reset_to_default()
            if self.round_bet > self.balance*(self.safety_params['max_bet_percent']/100):
                self.reset_to_default()             
            
        if show is True:
            plt.plot(wX,vY)
        
        
        
    def recovery_strat_1(self):
        self.round_bet = self.round_bet * self.recover_mult_bet
#        print(self.round_bet)

    def recovery_strat_2(self):
        self.round_target = self.round_target * self.recover_mult_target
#        print(self.round_bet)

    def recovery_strat_3(self):
        self.round_target = self.round_target * self.recover_mult_target
        self.round_bet = self.round_bet * self.recover_mult_bet
#        print(self.round_bet)
    def reset_to_default(self):
        self.round_bet = self.base_bet
        self.round_target = self.base_target
    
    def increase_stake(self):
        self.round_bet = self.round_bet + ((self.round_bet *self.round_target)/self.balance)
        
        
        
        
        
''' 
This method takes a strategy and then returns the performance of the strategy

@strategy dict - strategy

@returns dict  - strategy
'''        

        
def getStrategyPerformance (strategy, show = False):
    num_agents = 100
    num_games = 10000
#    best_strat = {'recv_mult_b': 1.25, 'recv_mult_t': 1.25, 'target': 393}
    
    count_of_busts = 0
    avg_performance = 0   
    count_mawr_money = 0
    
    starting_bal = 100000
    base_stake = 1
    recv_mult_b = strategy['recv_mult_b']
    recv_mult_t = strategy['recv_mult_t']        
    target = strategy['target']
    safety_params = strategy['safety_params']
    
    for x in range(num_agents):
        better = Strategy(starting_bal, base_stake, target, recv_mult_b, recv_mult_t, safety_params)
        better.testStrategy(num_games, show)    
        if better.bust is True:
            count_of_busts +=1
        if better.balance > starting_bal:
            count_mawr_money +=1
        avg_performance += better.balance
        
    return {'bust_ratio': count_of_busts/num_agents,
            'winning_ration': count_mawr_money/num_agents,
            'average': avg_performance/num_agents}


'''    
This method randomly generates a strategy to be tested using the monte carlo method

@return dict - strategy

'''    
def generateStrategy():
    params = {            
    'recv_mult_b': random.randint(1,1000)/100,
    'recv_mult_t': random.randint(1,1000)/100,  
    'target': getCrash(),
    'safety_params': {'max_bet_percent': random.randint(1,100),
                     'max_bet_target': random.randint(100,10000)}}
    return params

    

'''
This method generate a number of strategies and then tests them.

It returns the most successful strategy.

@return - dict
'''


def makeBetterBettor():
    num_of_strats = 1000
    best_measure = {'bust_ratio': 0,
                    'winning_ration': 0,
                    'average': 0}
    best_strat = None
    for x in tqdm.trange(num_of_strats):
        tested_strategy = generateStrategy()
        results = getStrategyPerformance(tested_strategy)
        
        ## first we select for winning ratio above 0.5
        if results['winning_ration'] > best_measure['winning_ration']:
            if results['average']> best_measure['average']:
                best_measure = results
                best_strat = tested_strategy
                print("The best strategy perfomed at a measurement of :" + str(best_measure))
                print(best_strat)            
    return best_strat , best_measure
            

##(main program cycle)    

if __name__ is "__main__":
    
    best_strat, best_measure = makeBetterBettor()   
    ### Only uncomment if Showing strategy
    best_measure = getStrategyPerformance(best_strat, show=True)
    
    if True is True:            
        plt.ylabel('Account Value')
        plt.xlabel('Wager Count')
        plt.show()    
        print("The best strategy perfomed at a measurement of :" + str(best_measure))
        print(best_strat)