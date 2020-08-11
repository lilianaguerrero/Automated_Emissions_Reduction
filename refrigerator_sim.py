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
    total_CO2 = 0
    for status in statuses:
        if status == 'on':
            total_CO2 += 200



    print('The refrigerator runtime for March is ' + str(runtime) + ' minutes or ' + str(runtime/60) + ' hours')
    # print(rfg_temps,monthly_MOERS,statuses)
    # plt.plot(monthly_timestamps, rfg_temps)
    # plt.plot(monthly_timestamps, statuses)
    # plt.show()
    print("Simulation complete")

temp = 33 #starting rfg temp
statuses = []
rfg_temps = []
def month_simulation(env):
    #runs hourly simulations over the period of a month
    n = 0 #five minute interval as given in the CSV data
    global temp
    global statuses
    global rfg_temps
    while True:
        hour = monthly_timestamps[n:n+12] #twelve five minute intervals per hour
        hourly_MOERS = monthly_MOERS[n:n+12]
        lowest_MOERS = sorted(hourly_MOERS)[:6]
        if temp < 37.99:
            for increment in hour:
                statuses.append('off')
                temp += (5/12)
                rfg_temps.append(temp)
        elif temp >= 37.99:
            for MOER in hourly_MOERS:
                if MOER in lowest_MOERS:
                    statuses.append('on')
                    temp -= (10/12)
                    rfg_temps.append(temp)
                    lowest_MOERS.remove(MOER)
                else:
                    statuses.append('off')
                    temp += (5/12)
                    rfg_temps.append(temp)
        n += 12 #twelve five minute intervals per hour
        hourly_duration = 1 #run this code for every hour during the month
        yield env.timeout(hourly_duration)

# def plot():
#     plt.plot(monthly_timestamps, monthly_MOERS)
#     plt.plot(monthly_timestamps, statuses)
#     plt.xlabel('March 2019 Timestamps')
#     plt.ylabel('Real Time MOER')
#     plt.title('Automated Emissions Reduction System')
#     plt.show()

if __name__ == '__main__':
    process_csv()
    main()
    # plot()




