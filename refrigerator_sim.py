import numpy as np
import simpy
import matplotlib.pyplot as plt 
from datetime import datetime

def process_csv():
    """processes CSV file data & appends data to array"""
    global monthly_timestamps 
    global monthly_MOERS
    monthly_timestamps = []
    monthly_MOERS = []
    file = open('MOERS.csv')
    #use datetime for chronological bounds
    start = datetime.fromisoformat('2019-03-01 00:00:00+00:00') 
    stop = datetime.fromisoformat('2019-03-31 23:55:00+00:00')
    for row in file:
        row = row.rstrip()
        if not row.startswith('timestamp'): 
            timestamp, MOER = row.split(',')
            timestamp = datetime.fromisoformat(timestamp)
            if timestamp >= start and timestamp <= stop:
                monthly_timestamps.append(timestamp)
                monthly_MOERS.append(int(MOER))
    #if statement below for doctest, see doc_tests.txt
    if (monthly_timestamps[0] == start and monthly_timestamps[-1] == stop and 
        len(monthly_MOERS) == 8928): 
        #if bounds are ok & data point qty= 8928 (# of 5min increments in March)
        print("Processed CSV")

def main():
    """defines environment where simulation takes place"""
    env = simpy.Environment()
    env.process(month_simulation(env))
    env.run(until=744) #744 hours in March
    rfg_runtime = rfg_on_off.count('on') * 5 #in minutes
    print('The total amount of CO2 for March 2019 is ' 
            + str(round(lbs_CO2[-1], 1)) + ' lbs of CO2')
    print('The total refrigerator runtime for March 2019 is ' + str(rfg_runtime) 
            + ' minutes or ' + str(round(rfg_runtime / 60,1)) + ' hours')
    #calls matplot function to plot graph
    matplot(monthly_timestamps, monthly_MOERS, rfg_temps, lbs_CO2) 
    """if statement below for doctest, see doc_tests.txt"""
    if (lbs_CO2[-1] == incremental_CO2 and rfg_on_off.count('off') 
        + rfg_on_off.count('on') == 8928):
        print("Simulation Complete")

rfg_temp = 33 #refrigerator temp that starts at 33 & changes every 5 min
rfg_on_off = [] #logs whether refrigerator is on/off every 5 min
rfg_temps = [] #logs refrigerator temperature every 5 min
incremental_CO2 = 0 #increases CO2 amount only when refrigerator is on
lbs_CO2 = [] #logs the incremental CO2 every 5 min

def month_simulation(env):
    """runs hourly simulations over the period of a month"""
    n = 0 #n represents five minute intervals as given in the CSV data
    while True:
        hour = monthly_timestamps[n:n+12] 
        #(12) 5 minute increments per hour
        hourly_MOERS = monthly_MOERS[n:n+12]
        lowest_4_MOERS = sorted(hourly_MOERS)[:4] #for when rfg is on 1/3 hr

        def change_temp_CO2():
            """checks & modulates rfg_temp, selects lowest MOERS for the next 
            hour if cooling is required, & logs CO2. Logic compares current 
            rfg_temp to just below median of temp range (38), if rfg_temp is 
            lower than the median, the rfg is off since it can afford the 
            heat gain (5 deg/hr). If rfg_temp is higher than the median, the 
            system only has to be on 1/3 of the next hour during the 5 min 
            increments with the lowest 4 MOERS"""
            global rfg_temp
            global rfg_on_off
            global rfg_temps
            global incremental_CO2
            global lbs_CO2
            if rfg_temp < 37.999:
                for increment in hour: 
                    #runs this code for every five minutes of the hour
                    rfg_on_off.append('off')
                    rfg_temp += (5 / 12) #heat gain rate per hr over 5 min
                    rfg_temps.append(round(rfg_temp,4))
                    lbs_CO2.append(incremental_CO2)
            elif rfg_temp >= 37.999:
                for MOER in hourly_MOERS:
                    #runs this code for every five minutes of the hour
                    if MOER in lowest_4_MOERS:
                        rfg_on_off.append('on') 
                        rfg_temp -= (10 / 12) #cooling rate per hr over 5 mins
                        incremental_CO2 += (MOER * .0002 * 1 / 12) 
                        #in lbs*C02 since 200W= .0002MW & 5min = hr/12
                        lowest_4_MOERS.remove(MOER)
                    else:
                        rfg_on_off.append('off')
                        rfg_temp += (5 / 12) #heat gain rate per hr over 5 min
                    rfg_temps.append(round(rfg_temp,4))
                    lbs_CO2.append(incremental_CO2)
                
        change_temp_CO2()
        n += 12 #twelve five minute intervals per hour
        hourly_duration = 1 #run this code for every hour of the month
        yield env.timeout(hourly_duration)

def matplot(monthly_timestamps, monthly_MOERS, rfg_temps, lbs_CO2):
    """uses matlpotlib to plot data over a shared monthly timestamps x-axis"""
    fig,ax1 = plt.subplots()

    color = 'green'
    ax1.set_xlabel('March 2019')
    ax1.plot(monthly_timestamps, rfg_on_off, 'g.', label='Smart Plug On/ Off') 
    #each green '.' is a five minute on/off period
    ax1.tick_params(axis='y', labelcolor=color, direction="in", pad=-22)
    ax1.invert_yaxis() 
    """upon zooming in, users can visualize how frequently the refrigerator is 
    off during peak MOERS & on during low MOERS"""

    ax2 = ax1.twinx()  #shares x axis with ax1
    color = '#0047ab'
    ax2.set_ylabel('Internal Refrigerator Temperature (F)', color=color) 
    #oscillates between 32.999 & 42.999 degrees
    ax2.plot(monthly_timestamps, rfg_temps, 
            label='Real Time Internal Refrigerator Temperature', 
            color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.yaxis.set_label_coords(1.025,.5)
    ax2.yaxis.set_ticks(np.arange(33, 44, 2))

    ax3 = ax1.twinx() #shares x axis with ax1
    color = 'red'
    ax3.set_ylabel('MOER (lbs*CO2/MW*hr)', color=color)
    ax3.plot(monthly_timestamps, monthly_MOERS, label='Real Time MOER', 
            color=color)
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.yaxis.tick_left()
    ax3.yaxis.set_label_coords(-.04,.5)

    ax4 = ax1.twinx() #shares x axis with ax1
    color = 'black'
    ax4.set_ylabel('CO2 (lbs)', color=color)
    ax4.plot(monthly_timestamps, lbs_CO2, 'k-', label='Cumulative CO2')
    ax4.tick_params(axis='y', labelcolor=color, direction="in", pad=-22)
    ax4.yaxis.set_label_coords(.965,.5)
    
    small_size = {'size': 9}
    ax1.legend(loc='lower left', prop=small_size)
    ax2.legend(loc='lower right', prop=small_size)
    ax3.legend(loc='upper left', prop=small_size)
    ax4.legend(loc='upper right', prop=small_size)
    plt.title('Automated Emissions Reduction Simulation', fontsize=20)
    fig.set_tight_layout(monthly_timestamps)
    plt.show()

if __name__ == '__main__':
    process_csv()
    main()
    




