
def refrigerator_temp(status):
    # Every hour refrigerator is on, Temp-10 degrees
    # Every hour refrigerator is off, Temp+5 degrees
    #5min as shown in CSV increments = 1/12 of an hour
    rfg_temp = 33
    on_delta = 10
    off_delta = 5
    incremental_change = (1/12) * 
    if status == 'on':
        rfg_temp + 