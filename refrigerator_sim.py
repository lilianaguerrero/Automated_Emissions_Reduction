
import matplotlib.pyplot as plt 
import simpy
from datetime import datetime

monthly_timestamps = []
monthly_MOERS = []
def process_csv():
    file = open('MOERS.csv')
    start = datetime.fromisoformat('2019-03-01 00:00:00+00:00')
    stop = datetime.fromisoformat('2019-04-01 00:00:00+00:00')
    for row in file:
        row = row.rstrip()
        if not row.startswith('timestamp'): 
            timestamp, MOER = row.split(',')
            timestamp = datetime.fromisoformat(timestamp)
            if timestamp >= start and timestamp <= stop:
                monthly_timestamps.append(timestamp)
                monthly_MOERS.append(int(MOER))

def rfg_temp(status):
    # modulates refrigerator temp every 5 min. based on whether plug is on/ off
    rfg_temp = 33
    on_delta = -10 # Every hour refrigerator is on, temp lowers 10 degrees
    off_delta = 5 # Every hour refrigerator is off, temp rises 5 degrees
    five_min = (1/12) #5min as shown in CSV increments = 1/12 of an hour

    if status == 'on':
        rfg_temp += five_min*on_delta

    elif status == 'off':
        rfg_temp += five_min*off_delta
    print(rfg_temp)



def rfg_runtime_co2(status):
    on = 200 #Watts
    duration = 0#hours
    total_CO2 = 0
    if status == 'on':
        total_CO2 = MOER * duration * on * (10^-6)
    # MOER = lbs CO2 /megawatt*hour


def plot_hour_window():
    hour = monthly_timestamps[:13]
    hourly_MOERS = monthly_MOERS[:13]
    print(hour, hourly_MOERS)

    plt.plot(hour, hourly_MOERS)
    plt.xlabel('Hour Forecast')
    plt.ylabel('MOER')
    plt.title('Automated Emissions Reduction System')
    plt.yticks(hourly_MOERS)
    plt.show()

# rfg_temp('off')
# rfg_runtime_co2(status)   
process_csv()
plot_hour_window()





# apl_price = [93.95, 112.15, 104.05, 144.85, 169.49]
# year = [2014, 2015, 2016, 2017, 2018]

