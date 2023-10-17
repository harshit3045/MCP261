
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#seed value for numpy for generating random numbers 
np.random.seed(1234)

#load the excel sheet into a datafile df
df = pd.read_excel("MCP261 Exercise 1 data.xlsx", sheet_name="Sheet1")


#get the stock price matrix
stock_price = np.array(df)

#arrays that store mean of the stock prices and variance for the stocks of each company
mean_stock_price = stock_price[-3]
variance_stock_price = stock_price[-1]

df = df[:-4];
#print(df)
#obtain the covariance matrix from the datafile
covariance_matrix = np.array(pd.DataFrame.cov(df))

#setting the risk tolerance factor as given in question
gamma = 0.1

#function for simulation of monte carlo
# takes input the number of simulations
def monte_carlo_sim(simulation_count):
    
    # an array to store returns from markowitz formula
    returns = np.empty(shape = simulation_count) 

    #variable that stores max returns until this point in iteration
    max_returns = 0
    #variable that stores the best portfolio until this point in iteration
    best_portfolio = np.empty(shape = len(mean_stock_price))

    #begin iterations to generate random samples
    for m in range(0,simulation_count):

        #generate random weights and normalize to make their sum = 1
        weights = np.random.random(len(mean_stock_price))
        weights /= np.sum(weights)

        #calculate returns using markowitz formula
        returns[m] = weights.T.dot(mean_stock_price) - gamma*weights.T.dot(covariance_matrix).dot(weights)
        #if new return are greater update
        if returns[m] > max_returns:
            max_returns = returns[m]
            best_portfolio = weights

    #print the answers in desird format
    print('\nsimlulation count: ',simulation_count, '\nbest portfolio: ', best_portfolio, '\nmax returns', max_returns)
    return max_returns


# run the fundction for updated values.

for i in range (1,6):
    monte_carlo_sim(5*pow(10,i))


