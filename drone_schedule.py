#!/Users/sandeepbalaji/anaconda3/bin/python
import re, math, sys, os
from datetime import datetime, timedelta

input_file = sys.argv[1]
output_file = os.path.dirname(sys.argv[1])+"/output.txt"
print(output_file)

#Calculate ratings for the hours
# 1 -> promoters
# 0 -> neutral
# -1 -> detractors
def ratings(hours):
    if int(hours) <= 1:
        return 1
    elif int(hours) > 7:
        return -1
    else:
        return 0

#read the input file and return them as list of tuples
def read_input(filename):
    data =[]
    file = open(filename, "r")
    for line in file:
        data.append(tuple(line.split()))
    file.close()
    return data

#calculate the distance required for the order
def calc_distance(coordinate):
    x, y = re.split(r'\D',coordinate)[1:]
    sum = math.sqrt(int(x)**2 + int(y)**2)
    return 2*sum

#calculate the hours for the order
def calc_hours(start_time, order_time, distance):
    minutes = (start_time - order_time).seconds/60 + distance
    return minutes/60

#calculate the nps score for all the scheduled orders
def calc_nps(out, inp):
    promoters = 0
    detractors = 0
    assert len(inp) == len(out)
    for i in range(len(inp)):
        distance = calc_distance(inp[i][1])
        order_time = datetime.strptime(inp[i][2], '%H:%M:%S')
        start_time = datetime.strptime(out[i][1], '%H:%M:%S')
        hours = calc_hours(start_time, order_time, distance)
        if ratings(hours) == 1:
            promoters += 1
        elif ratings(hours) == -1:
            detractors += 1
    return round((promoters-detractors)/len(inp)*100)

#function for filtering orders which are less than the current time
def filter_data(data, current_time):
    list = []
    for i in range(len(data)):
        if datetime.strptime(data[i][2], '%H:%M:%S') < current_time:
            list.append(data[i])
        else:
            break
    return list

#main function
if __name__ == '__main__':
    out = []
    data = read_input(input_file)
    inp = data.copy()
    data_set = set(data)
    current_time = datetime.strptime('06:00:00', '%H:%M:%S') #start at 6am
    filtered = filter_data(data, current_time)
    fulfilled = set()
    output = open(output_file, "wt")
    date_check = datetime.strptime('22:00:00', '%H:%M:%S') #variable to check for 10pm
    while fulfilled.symmetric_difference(data_set) != set(): #loop until all the orders are scheduled
        best_hours = float('inf')
        ind = -1
        for i in range(len(filtered)):
            distance = calc_distance(filtered[i][1])
            hours = calc_hours(current_time, datetime.strptime(filtered[i][2], '%H:%M:%S'), distance/2)
            if best_hours > hours: #get the order with least cost(distance + time elapsed)
                best_hours = hours
                ind = i

        if current_time > date_check: #if time crosses 10pm, push to next day 6pm
            current_time = datetime.strptime('22:00:00', '%H:%M:%S')+timedelta(hours=8)
            date_check += timedelta(days=1)
        distance = calc_distance(filtered[ind][1])
        hours = calc_hours(current_time, datetime.strptime(filtered[ind][2], '%H:%M:%S'), distance/2)
        out.append(tuple([filtered[ind][0], current_time.time().strftime('%H:%M:%S')]))
        output.write(filtered[ind][0]+" " +current_time.time().strftime('%H:%M:%S') +"\n")
        fulfilled.add(filtered[ind])
        data.remove(filtered[ind])
        current_time += timedelta(seconds=60*distance)
        filtered = filter_data(data, current_time)
        if filtered == [] and data != []:#pick the next least order, if no orders to schedule
            current_time = datetime.strptime(data[0][2], '%H:%M:%S')
            filtered = filter_data(data, current_time)

    nps = calc_nps(out, inp)
    output.write("NPS "+str(nps))
    output.close()
