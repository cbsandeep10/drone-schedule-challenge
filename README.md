# Solution Approach (greedy algorithm):
* Pick the orders that are available to schedule (ordered time < current time)
* Pick the least cost order and schedule it(cost = distance + time elapsed).
* update the current time.
* Repeat step-1 and step-2 until alls orders are scheduled.

## Input file formats
### Input file format
[order_no] [coordinate] [timestamp]

### Example:
WM001 N11E3 05:11:09

## Output file format
[order_no] [timestamp] 
NPS [nps_score]

### Example:
WM001 06:00:00
NPS 88

# Running
## Requirements:
Python = 3.6.4

## Usage:
```
python drone_schedule.py [input_filepath]
```
## Output:
[output_filepath]
