#!/usr/bin/python3.8
import boto3
import botocore
from datetime import datetime, timedelta, timezone, time
import csv 
import matplotlib.pyplot as plt
import pandas
import pytz

# if running in vscode in wsl, install jupyter to view graph in interactive window
# This will create 2 csv files in the local directory with stopped and running admin vms.

aws_profile = "cctqa"
region = 'us-east-1'

boto3.setup_default_session(profile_name=aws_profile)
sns_client = boto3.client('sns', region)
client = boto3.client('ec2', region)

today_date_utc = datetime.now(timezone.utc)
today_date_format = today_date_utc.strftime('%Y-%m-%d %H:%M:%S')

running_reasons = []
stopped_reasons = []
msg_running=[]
msg_stopped=[]
transition_timestamps=[]

instance_ids = []
instance_names = []
running_instances = []
stopped_instances = []
msg_running_str = []
msg_stopped_str = []

running_file = 'admins_running.csv'
stopped_file = 'admins_stopped.csv'



def main():
    # Use the filter() method of the instances collection to retrieve
    # all running Admin instances who have opted into the slumbering admin program. 
    filters = [
        {
            'Name': 'tag:t_role',
            'Values': ['Admin']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['running', 'stopped']
        },
        {
            'Name': 'tag:slumbering-admin', 
            'Values': ['true']  
        }
    ]
    
    reservations = client.describe_instances(Filters=filters).get('Reservations', [])
    for reservation in reservations:
        for instance in reservation['Instances']:
            tags = {}
            for tag in instance['Tags']:
                tags[tag['Key']] = tag['Value']
                if tag['Key'] == 'Name':
                    name=tag['Value']

                    if instance['State']['Name'] == 'running':
                            msg_running, running_stdout = running_admins(name, instance)
                    elif instance['State']['Name'] == 'stopped':
                        msg_stopped, stopped_stdout = stopped_admins(name, instance)
                    else:
                        pass # do nothing if instance state is not running or stopped. 


    # running vm info
    write_running_csv(msg_running)
    print("Running Admins:\n",running_stdout)
    bar_graph_running(running_file)
    # stopped vm info
    write_stopped_csv(msg_stopped)   
    print("Stopped Admins:\n",stopped_stdout) 
    bar_graph_stopped(stopped_file)


def stopped_admins(name, instance):
    stopped_instances.append(instance)
    instance_ids.append(instance['InstanceId'])
    instance_names.append(name)
    stopped_reason = instance['StateTransitionReason']
    stopped_reasons.append(stopped_reason)
    transition_timestamp = datetime.strptime(instance['StateTransitionReason'][16:35], '%Y-%m-%d %H:%M:%S')
    transition_timestamp = transition_timestamp.astimezone(pytz.utc)
    days=(today_date_utc - transition_timestamp).days
    hours=(today_date_utc.hour - transition_timestamp.hour)
    # if days < 1: 
    #     days = hours
    stopped_times_str = "InstanceID: " + instance['InstanceId'] + "," + ' Instance Name: ' +name + "," + " Shutdown Time: " + str(transition_timestamp) + "," + " Number of days stopped: " + str(days)
    stopped_times = [name, str(days)]
    msg_stopped.append(stopped_times)
    msg_stopped_str.append(stopped_times_str)
    msg_stopped_str.append("\n")
    stopped_stdout = ''.join(msg_stopped_str)
    return msg_stopped, stopped_stdout


def running_admins(name, instance):       
    running_instances.append(instance)
    instance_ids.append(instance['InstanceId'])
    instance_names.append(name)
    days=(today_date_utc - instance['LaunchTime']).days
    running_times_str = "InstanceID: " + instance['InstanceId'] + "," + ' Instance Name: ' +name + "," + " Number of days running: " + str(days)
    running_times = [name, str(days)]
    msg_running.append(running_times)
    msg_running_str.append(running_times_str)
    msg_running_str.append("\n")
    running_stdout = ''.join(msg_running_str)
    return msg_running, running_stdout


def write_running_csv(data):
    header_running = ['Instance Name', 'Number of days running']
    with open(running_file, 'w') as admins_running:
        writer = csv.writer(admins_running)
        writer.writerow(header_running)
        writer.writerows(data)

def write_stopped_csv(data):
    header_stopped = ['Instance Name', 'Number of days stopped']
    with open(stopped_file, 'w') as admins_stopped:
        writer = csv.writer(admins_stopped)
        writer.writerow(header_stopped)
        writer.writerows(data)

def bar_graph_running(file):
    data = pandas.read_csv(file)
    df = pandas.DataFrame(data)
    X = list(df.iloc[:, 0])
    Y = list(df.iloc[:, 1])
    plt.bar(X, Y, color='g')
    plt.title("Running Admins")
    plt.ylabel("Number of days running")
    plt.xlabel("Instance Name")
    plt.xticks(rotation=45, ha='right')
    plt.show()

def bar_graph_stopped(file):
    data = pandas.read_csv(file)
    df = pandas.DataFrame(data)
    X = list(df.iloc[:, 0])
    Y = list(df.iloc[:, 1])
    plt.bar(X, Y, color='r')
    plt.title("Stopped Admins")
    plt.ylabel("Number of days stopped")
    plt.xlabel("Instance Name")
    plt.xticks(rotation=45, ha='right')
    plt.show()

def pie_chart():
    pass

main()
