import sys
import os
import os.path as path
import ftplib
import argparse
import datetime
import docker


CONFIGFILE = ".config"
MOUNT = ""

def init():
    if path.isfile(CONFIGFILE):
        file = open(CONFIGFILE, 'r')
        MOUNT = file.readline().rstrip()
        if MOUNT == "":
            print "A mount directory was not specified in the .config file"
            sys.exit(0) # Error
        print "Your mounting dir is: ", MOUNT
        return 1 # Success
    print "No .config file found please add one in the current director!"
    sys.exit(0) # Error


""" Command-Line Arguments
    task -Choose a specific task for the model to accomplish
    Options - plot, get_data, validate (maybe?),
    time - Datetime object
    date - datetime object
    slice - int- Time slice from the date specified -
"""
if __name__ == "__main__":
    init()

    client = docker.from_env()

    parser = argparse.ArgumentParser(description='Easy NAMS Plotting.')
    parser.add_argument('task',
                        help='task name',
                        type=str)
    parser.add_argument("-f", '--file',
                        help='File name to store the plot',
                        type=str)
    parser.add_argument("-t", '--time',
                        help='datetime object',
                        type=str)
    parser.add_argument("-d", '--date',
                        help='datetime object',
                        type=str)
    parser.add_argument("-l", '--layer',
                        help='integer',
                        type=int)
    parser.add_argument("-i", '--slice',
                        help='integer',
                        type=int)
    args = parser.parse_args()

    out = client.containers.run('basemap', 'python plot.py ' + args.task)

    if args.task == "test":
        #client.containers.run('basemap', 'python plot.py test')

        out = client.containers.run('basemap', 'python plot.py ' + args.task)
        print out
        print type(out)
        """
        print client.containers.run('basemap',
                                        "python plot.py " \
                                        + str(args.task) \
                                        + "-d"  + str(args.date) \
                                        + "-t"  + str(args.time) \
                                        + "-s" + str(args.slice) \
                                        + "-l" + str(args.layer) \
                                        + "-f" + str(args.file))
        """

    sys.exit(0)
