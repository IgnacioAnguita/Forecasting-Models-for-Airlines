## Forecasting Models For Airlines

By Ignacio Anguita and Núria Martín
07/02/2018

# Intro
The aim of this code is just to provide some functions in order to help to forecast the traffic of passengers.
There is also another objective, which is learn, through coding these functions we have understood better the models
used in the aeronautical sector, and we also have improved our coding skills. If you want to use it just copy the function and the 
variables needed for the model in your own code and print it. Remember you will have to feed the model with some data.

# Forecast demanding
This program has been created to forecast de demand of airplane passengers. All the informatopn and equations have been extracted form the book "Flying off course" by Rigas Doggains. 
Data used to exemplify the program has been extracted form the same book and it is the total passenger traffic London-Nice(both ways) from 1972 to 1983.
To forecast the demand we have different options:qualitative methods, time-series projection and economeric or casual methods. As qualitative methods can not be computed, this program 
is focused in the last two.

## Time series projection.
For this method is important to have traffic's data of the previous years.There are two forms of represent data: in an exponential or in a linear form. This program has both of them.
As it can be seen in the program, the first part is about the exponential representation. 

# Exponential forecasts

These methods use the exponential formula (Like the one it is used for compund interest) to forecast the demand.

# Average rate of growth
Using the formula y=a*(1+b)^t we will be able to calculate the traffic passengers in a concrete
year. "a" is the actual traffic (1983 in this case), "b" is the growth rate(in per 1) and t is the number of years forecast. In the code we calculate the Annual_change with pandas library 
(which will be useful along all the program).To obtain b is as simple as doing a mean of the Annual_change and a is the last value of our vector Terminal_passengers, which keep the data 
of the number of passengers during our data years).

# Moving average growth
We will use moving averages as a way of flattening out wild traffic variations so as to understand the underlying trends. First, we use the method rolling.mean to do a moving average of
the terminal passengers with a window of 3 values. Next we will calculate the Annual_change with pandas option pct.change (which gives us the value in per one).Then is as simple as 
repeating the previous explained steps: a will be the last value of the Moving_average_passengers vector.

# Exponential smoothing
In this case we introduce a new variable:alpha. Alpha can have a value between 1 and 10. It is used to give more importance at the last years data.If alpha is near to 10 last years
years will have a lot of importance and if it is near to 1 they will be as important as the old data. It is similar to Arima time series projection.

# Linear forecast
Here we have average rate growth and moving average grow which are the same as exponential case but changing the main equation. Now traffic is:
y=a+b*t
where t is time and a and b are variables that we can obtain doing a linear regression with old data.


## Econometric methods

This method use macroeconomic and geographical data to forecast the demand.

# Regression model
In this model we can add as variables as we want or we consider important for our forecast. This variables could be:fares,GNP of a contry, time of flight, speed of flight,...
In our model there are three of them. The equation consist in a sume of logarithms of this variables:
logT=K+a*logGNP+b*logF+c*logS
where T is the traffic and a,b,c and K are parameters that we have to find using a linear regression. Here we will need data of gross national produt, speed, fares and traffic
of at least 4 flights to find these parametres. To fin this parametres we have used the library sklearn, based in machine learning which predicts the next values.

# Gravity models

These models are focused on using the gravity's law and some variants of it in order to predict the traffic in new routes.

# Gravity model original
We will need data of a constant K, that will vary in every prediction and depends on the units used;P_i is the number of inhabitants of the origin, P_j is the number of inhabitants in the
destination and D_ij is the distance between both towns.

# Gravity model of Dogains
Here we have the same constant K but A_i and A_j are the total passengers traffic of origin airport and destination airport respectively. D_ij^p is the same variable as the last case but 
p is a number that can goes to 1 until 1.5.

# Gravity model complex
There are the variables K,A_i and A_j explained before and some new, which are Q and F. Q is the service quality variable, it hase the next values: 1 for non stop jet services, 0,7 for
 turbo prop and 0.5 for 1 stop services. F is the normal economy fare.
