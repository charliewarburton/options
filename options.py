# Options functions
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

class Call:
    def __init__(self, strike, premium):
        self.strike = float(strike)
        self.premium = float(premium)
        
    def payoff(self, spot):
        return max(spot - self.strike, 0) - self.premium # if spot is less than strike then cost is just premium
    def breakeven(self):
        return self.strike + self.premium

class Put:
    def __init__(self, strike, premium):
        self.strike = float(strike)
        self.premium = float(premium)

    def payoff(self, spot):
        return max(self.strike - spot, 0) - self.premium # If spot is above strike then don't use option and cost is premium
    def breakeven(self):
        return self.strike - self.premium
        
class Strategy:
    def __init__(self):
        # To contain the bought and written contracts
        self.long = []
        self.short = []
    
    def buy(self, contract):
        self.long.append(contract)
    def write(self, contract):
        self.short.append(contract)
    
    def strikes(self): 
        # To get unique list of strike prices for x axis (set doesn't allow duplictes)
        unique_strikes = set([c.strike for c in self.long + self.short]) 
        return sorted(list(set(unique_strikes)))
    
    # PnL for given spot price (Observation in y axis)
    def single_pnl(self, spot):
        profit = sum(c.payoff(spot) for c in self.long)
        # If the contracts we sold are in profit then its a loss
        loss = sum(c.payoff(spot) for c in self.short)

        return profit - loss
    
    # List of PnLs for each spot price (Series for Y axis)
    def list_pnl(self, spots):
        return list(map(self.single_pnl, spots))
    
    # The spot prices that PnL needs to be computed for
    # Note max spot price is 1000000 (saves dealing with infinity)
    def _spots(self):
        return [0, *self.strikes(), 1000000]
    
    def break_evens(self):
        break_even_spots = [] # list of spot prices where profit crosses x axis
        spots = self._spots()
        pnl = self.list_pnl(spots) # PnL values for the spots

        for i in range(len(spots) -1):
            # If there is an x axis cross
            if ((pnl[i] > 0) != (pnl[i+1] > 0)):
                # Compute the straight line graph y= mx + c for these two points
                m = (pnl[i+1] - pnl[i]) / (spots[i+1] - spots[i])
                c = pnl[i] - m*spots[i]
                # Know m and c, set y = 0 and solve for x
                x = -c/m
                break_even_spots.append(round(x, 2))
        return break_even_spots
    
    def plot(self):
        strikes = self.strikes()
        # array of x axis values from 90% of lowest strike to 110% of highest strike
        x = np.array([int(strikes[0]*0.9)] + strikes + [int(strikes[-1]*1.1)])
        y = np.array(self.list_pnl(x))
        x_axis = np.zeros(len(y))

        plt.plot(x, y, color = 'grey')
        plt.plot(x, x_axis, color = 'black')
        plt.fill_between(x, y, x_axis, where = y>0,
                         color = 'green', alpha = 0.2,
                         interpolate = True)
        plt.fill_between(x, y, x_axis, where = y<0,
                         color = 'red', alpha = 0.2,
                         interpolate = True)
        plt.xlabel("Price of underlying")
        plt.ylabel("Profit/Loss")
        plt.show()