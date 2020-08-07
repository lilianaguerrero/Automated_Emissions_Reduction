
#check temperature, if temp must be between 33-43


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

rfg_temp('off')
