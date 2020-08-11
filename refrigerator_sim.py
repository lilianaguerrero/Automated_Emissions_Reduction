import simpy
import matplotlib.pyplot as plt 
from datetime import datetime

def process_csv():
    #processes CSV file data & appends data to lists
    global monthly_timestamps #global variable to be able access outside of function
    global monthly_MOERS
    monthly_timestamps = []
    monthly_MOERS = []
    file = open('MOERS.csv')
    start = datetime.fromisoformat('2019-03-01 00:00:00+00:00') #datetime to be able to be used as chronological bounds
    stop = datetime.fromisoformat('2019-04-01 00:00:00+00:00')
    for row in file:
        row = row.rstrip()
        if not row.startswith('timestamp'): 
            timestamp, MOER = row.split(',')
            timestamp = datetime.fromisoformat(timestamp)
            if timestamp >= start and timestamp < stop:
                monthly_timestamps.append(timestamp)
                monthly_MOERS.append(int(MOER))

def main():
#defines environment where simulation takes place
    env = simpy.Environment()
    env.process(month_simulation(env))
    env.run(until=744) #744 hours in month of March
    runtime = statuses.count('on')*5 #in minutes
    print('The total amount of CO2 for March 2019 is ' + str(incremental_CO2) + ' lbs of CO2')
    print('The total refrigerator runtime for March 2019 is ' + str(runtime) + ' minutes or ' + str(runtime/60) + ' hours')
    plt.plot(monthly_timestamps, rfg_temps)
    plt.plot(monthly_timestamps, monthly_MOERS)
    plt.plot(monthly_timestamps, statuses)
    plt.plot(monthly_timestamps, lbs_CO2)
    plt.show()

temp = 33 #starting rfg temp
statuses = []
rfg_temps = []
on_MOERS = []
lbs_CO2 = []
incremental_CO2 = 0
def month_simulation(env):
    #runs hourly simulations over the period of a month
    n = 0 #five minute interval as given in the CSV data
    global temp
    global statuses
    global rfg_temps
    global lbs_CO2
    global incremental_CO2
    while True:
        hour = monthly_timestamps[n:n+12] #twelve five minute intervals per hour
        hourly_MOERS = monthly_MOERS[n:n+12]
        lowest_MOERS = sorted(hourly_MOERS)[:6]
        if temp < 37.99:
            for increment in hour:
                statuses.append('off')
                temp += (5/12)
                rfg_temps.append(temp)
                lbs_CO2.append(incremental_CO2)
        elif temp >= 37.99:
            for MOER in hourly_MOERS:
                if MOER in lowest_MOERS:
                    statuses.append('on')
                    temp -= (10/12)
                    incremental_CO2 += (MOER * .0002 * 1/12) #in lbs*C02 since MW*(10^-6)= W & 5min = hr/12
                    rfg_temps.append(temp)
                    on_MOERS.append(MOER)
                    lowest_MOERS.remove(MOER)
                else:
                    statuses.append('off')
                    temp += (5/12)
                    rfg_temps.append(temp)
                lbs_CO2.append(incremental_CO2)
        n += 12 #twelve five minute intervals per hour
        hourly_duration = 1 #run this code for every hour during the month
        yield env.timeout(hourly_duration)


if __name__ == '__main__':
    process_csv()
    main()
    




