import xlrd
import matplotlib.pyplot as plt
import numpy as np

#loading the workbook into python
wkb = xlrd.open_workbook("Ex 2 TPM Q.xls")

#access the first sheet
sheet = wkb.sheet_by_index(0)

#transition probability matrix that holds the given data
tpm = []

#extract the matrix into the tpm numpy array
for row in range (2,sheet.nrows):
    _row = []
    for col in range (1,sheet.ncols):
        _row.append(sheet.cell_value(row,col))
    tpm.append(_row)

#an array that holds the names of states
state_names = [sheet.cell_value(1,i) for i in range(1,sheet.ncols)]

#access the second sheet for cost matrix
sheet = wkb.sheet_by_index(1)
cost_matrix = []

#extract the cost matrix into the cost_matrix numpy array
for row in range (2,sheet.nrows):
    _row = []
    for col in range (1,sheet.ncols):
        _row.append(sheet.cell_value(row,col))
    cost_matrix.append(_row)

#array to hold sum of power series of transition matrix
#initialized as 1 only in first state as given in question
sum_series = np.eye(18,dtype=float)[0,:]

#2D array to hold power series of the transition probability matrix
power_series = np.eye(18, dtype=float)

#loop over 5 years * 12 = 60 times and find power series and sum of power series

for i in range(0,59): 
    power_series= power_series.dot(tpm)

    sum_series = sum_series + power_series[0,:]#we only need first array as initial state is 1 as given

#mean time spent in each state are the elements in sum_series
mean_time_spent = sum_series 

#sum each column of cost_matrix to find sum of each state
for i in range(18):
    cost_array = np.sum(cost_matrix, axis=0)

#total cost obtained as dot product of cost in each state with mean time in each state
total_cost = cost_array.dot(mean_time_spent)
#print("ans is ",total_cost)

#setting the seed value
np.random.seed(1234)

#for gaussian distribution, the mean and sigma as given
mean  = cost_array 
sigma = 0.03*cost_array

#null array for storing simulation values
simulations=[0.0]*1000

#conducting monte carlo simulation over 1000 iterations
for i in range(1000):
    #generating random samples from gaussian distribution
    random_costs = np.random.normal(mean, sigma)
    simulations[i] = random_costs.dot(mean_time_spent)

#calculate mean and standard dev of the simulations
sim_mean = np.mean(simulations)
sim_sd= np.std(simulations)
print("For Monte-carlo simulation:")
print("Mean is: ", sim_mean, " and standard dev. is: ", sim_sd)


#plot histogram for the simulations
plt.hist(simulations, bins=70, color="blue", ec="cyan")

#setting the labels
plt.title("Histogram showing monte-carlo simulations ")
plt.xlabel("Total average costs")
plt.ylabel("No. of iterations")
plt.show()

    




