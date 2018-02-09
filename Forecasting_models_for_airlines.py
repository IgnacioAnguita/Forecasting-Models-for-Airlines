########################### By Ignacio Anguita & Nuria Martín #################################

import math 
import pandas as pd
import numpy as np
from numpy import convolve
from sklearn import linear_model
from sklearn import datasets ## imports datasets from scikit-learn


# Data
years = [1972,1973,1974,1975,1976,1977,1978,1979,1980,1981,1982,1983] #the years of our data
terminal_passengers=[140.6,148.5,142.4,163.8,169.6,167.4,185,209.9,225.1,241.2,268.8,268]


Terminal_passengers=pd.DataFrame(data=terminal_passengers)#we convert our data into a pandas data frame
Years=pd.DataFrame(data=years)
Anual_change = Terminal_passengers.pct_change(1)


#variables

time=5 #number of years of the forecast, for this example we want to know the number of passengers in two years time
n=len(terminal_passengers)-1
alpha=1.3

######################################## Time series projections ####################################

############################## Exponential forecast #########################################

def Exponential_forecast_Average_rate_of_growth (Terminal_passengers,Anual_change,time,terminal_passengers,n):
	a=terminal_passengers[n]#here we find the first value of the array
	b=(Anual_change.mean()) #we calculate the mean of the annual changes
	Traffic=a*math.pow(1+b,time) #we apply the exponential growth
	return Traffic


def Exponential_forecast_Moving_average_growth (Terminal_passengers,Anual_change,time,terminal_passengers,n):
	Moving_average_passengers=Terminal_passengers.rolling(window=3).mean() #calculation of the moving average with a time window of 3 years
	Moving_average_passengers_pct_change=Moving_average_passengers.pct_change()
	b=Moving_average_passengers_pct_change.mean() #calculation of the mean of the moving average
	a=Moving_average_passengers.at[n,0]#here we find the first value of the array
	Traffic=a*math.pow(1+b,time+1) #we apply the exponential growth
	return Traffic
	

def Exponential_forecast_Exponential_Smoothing(terminal_passengers,Anual_change,alpha,n): #this only provides a forecast for the first year
	i=0
	Traffic=0
	while i<=n: #we will suppose that the first data is the most recent one
		Traffic=Traffic+alpha*terminal_passengers[n-i]*math.pow(1-alpha,i)
		i=i+1
	return Traffic

################## Linear trend projections ################################

def Linear_forecast_Average_rate_of_growth (Years,terminal_passengers,years,time,n):
	y=np.array(terminal_passengers)
	x=np.array(years)
	m=(((np.mean(x)*np.mean(y))-np.mean(x*y))/((np.mean(x)*np.mean(x))-np.mean(x*x)))
	m=round(m,2)
	c=np.mean(y)-(np.mean(x)*m) #y=m*x+c
	c=round(c,2)
	Traffic=c+(m*(time+Years.at[n,0]))
	return Traffic

def runningMean(x, N):
    y = np.zeros((len(x),))
    for ctr in range(len(x)):
         y[ctr] = np.sum(x[ctr:(ctr+N)])
    return y/N


def Linear_forecast_Average_rate_of_growth_Moving_Average (Years,Terminal_passengers,terminal_passengers,years,time,n):
	D=Terminal_passengers.rolling(window=3).mean()
	y=np.array(D)
	Y=np.transpose(y)
	Y=np.nan_to_num(Y)
	Y=np.delete(Y,[0,1])
	x=np.array(years)
	x=np.delete(x,[0,1])
	m=(((np.mean(x)*np.mean(Y))-np.mean(x*Y))/((np.mean(x)*np.mean(x))-np.mean(x*x)))
	m=round(m,2)
	c=np.mean(Y)-(np.mean(x)*m) #y=m*x+c
	c=round(c,2)
	Traffic=c+(m*(time+Years.at[n,0]))
	return Traffic



##################################################### Econometric or causal methods #####################################################

############### Regression models########################

def Linear_regression(J,N):
 df = pd.DataFrame(data=J)
 target = pd.DataFrame(data=N)
 X = df
 y = target
 lm = linear_model.LinearRegression()
 model = lm.fit(X,y)
 predictions = lm.predict(X)
 z=lm.coef_
 w=lm.intercept_
 return z,w

def Causal_method ():
 #For this model we will consider the following independent variables:
 #T is the air traffic
 #GNP(gross national product)
 #F=fares
 #S=quality of service variable, in this case the speed
 #math.log(T)=K+a*math.log(GNP)+b*math.log(F)+c*math.log(S)
 #a,b,c are model parameters and K a constant term
 #We will need at least 4 equations to found a,b,c,K parametres
 GNP=560
 F=100
 S=63 #example values of S,F and GNP
 #Multiple Linear regression mode
 x1=math.log(GNP)
 x2=math.log(F)
 x3=math.log(S)
 #y=K+a*x1+b*x2+c*x3
 J=[[0,2,3],[6,5,6],[1,2,3]]
 N=[4,1,3]
 z,w=Linear_regression(J,N) #N is the vector with traffic data and J is a matrix with the values of GNP,F and S
 #z are the number of a,b and c
 #w is the number of K
 y=w+np.sum(z*[x1,x2,x3])
 T=math.pow(y,10)
 return y

###############  Gravitiy Models ########################

# we will use other type of data for this models

# First model variables

K=10 #constant K will depend on every prediction, it has to be adjust before it will depend on the units of every variable
P_i=100000 #number of inhabitants of town i
P_j=100000 #number of inhabitants of town j
D_ij=100000 #distance between towns

def Gravity_model_original (K,P_i,P_j,D_ij):
	Traffic=K*P_i*P_j/D_ij
	return Traffic

# Second model variables

# We still use the parameter K that has to be adjusted for this model
A_i=1000000 #Total passengers traffic of the airport i 
A_j=1000000 #Total passengers traffic of the airport j 
P=1.25 #P goies from 1 to 1.5, depends in each case
#We also use D_ij

def Gravity_model_Doganis (K,A_i,A_j,P,D_ij):
	Traffic=K*A_i*A_j/math.pow(D_ij,P)
	return Traffic


# Third model variables
# We still use the parameter K that has to be adjusted for this model
A_i_sc=1000000 #Total scheduled passengers traffic of the airport i
A_j_sc=1000000 #Total scheduled passengers traffic of the airport j

Q=1 #service quality variable it hase the next values: 1 for non stop jet services, 0,7 for turbo prop and 0.5 for 1 stop services
F=100 #normal economy fare

def Gravity_models_complex (K,A_i_sc,A_j_sc,Q,F):
	Traffic =K*A_i_sc*A_j_sc*math.pow(Q,0.75)/math.pow(F,0.5)
	return Traffic

