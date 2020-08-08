#import matplot library
import matplotlib.pyplot as plt 
#establish environment using simpy which manages simulation time and move the simulation through each subsequent time step
env = simpy.Environment() 
# Assume you've defined checkpoint_run() beforehand
env.process(checkpoint_run(env, num_booths, check_time, passenger_arrival))

# runs for 10 minutes (change to 60 for my example)
env.run(until=10)




# apl_price = [93.95, 112.15, 104.05, 144.85, 169.49]
# ms_price = [39.01, 50.29, 57.05, 69.98, 94.39]
# year = [2014, 2015, 2016, 2017, 2018]

# plt.plot(year, apl_price)
# plt.show()