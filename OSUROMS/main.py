import sys
import os
import ftplib
import argparse
import datetime

def test(name):
    """ Fun test function to test things easily! """
    map = Basemap()
    map.drawcoastlines()
    filename = os.path.join('/media2/', str(name))
    plt.savefig(filename)
    return filename


""" Argument Parser
    task -Choose a specific task for the model to accomplish
    Options - plot, get_data, validate (maybe?),
    time - Datetime object
    date - datetime object
    slice - int
    variable - name of variable to get
"""
parser = argparse.ArgumentParser(description='Python OSUROMS module.')
parser.add_argument('task',
                    help='task name',
                    type=str)
parser.add_argument("-t", '--time',
                    help='datetime object',
                    type=datetime.datetime)
parser.add_argument("-d", '--date',
                    help='datetime object',
                    type=datetime.datetime)
parser.add_argument("-l", '--layer',
                    help='integer',
                    type=int)
parser.add_argument("-i", '--slice',
                    help='integer',
                    type=int)
parser.add_argument("-v", '--variable',
                    help='variable name',
                    type=str)

args = parser.parse_args()
if args.task == "get":
    get(args.variable)
elif args.task == "plot":
    plot(date=args.date, time=args.time, layer=args.layer)
elif args.task == "test":
    test(args.variable)

sys.exit(0)
