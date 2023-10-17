
import numpy as np
import matplotlib.pyplot as plt
import scipy.optimize as opt
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
            

    return max_returns


#define markowitz function
def f(w):
    return -1*w.T.dot(mean_stock_price) + gamma*w.T.dot(covariance_matrix).dot(w)

#initlizer value for optimization and normalizing
initializer_weights = [0.2]*5

#set bounds on weight values
bound=[(0,1) for i in range(5)]

#define constraint of markowitz formulation
def check_sum(weights):
    return np.sum(weights) -1

cons = {'type' : 'eq', 'fun' : check_sum }

#scipy optimization
optimal_return = opt.minimize(f,initializer_weights,bounds=bound,constraints=cons)

print('max returns are: ', -1*optimal_return["fun"], 'with portfolio: ', optimal_return["x"])

#--------------plotting values----------
#no. of iteration
array = [(5*pow(10,i)) for i in range(1,6)];

max_returns = [monte_carlo_sim(x) for x in array]

#compute absolute percent difference of MC simulation from optimal value
diff =  [np.absolute(x - (-1)*optimal_return['fun'])/(-1)*optimal_return['fun'] for x in max_returns]


#using matplotlib to plot the difference
plt.plot(array, diff)
plt.xlabel("Number of iterations")
plt.ylabel("Absolute Percent difference")
plt.title("Absolute percent difference in MC value and Scipy optimized value")
plt.show()

#this shows decreasing values of difference with increasing no of iterations showing MC simulation achives close
# to optimal values


