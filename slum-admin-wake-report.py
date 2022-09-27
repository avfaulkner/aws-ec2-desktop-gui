#!/usr/bin/python3.8
import boto3
import botocore
from datetime import datetime, timedelta, timezone, time
import csv 
import matplotlib.pyplot as plt
import pandas

# if running in vscode in wsl, install jupyter to view graph in interactive window

aws_profile = "cctqa"
region = 'us-east-1'

boto3.setup_default_session(profile_name=aws_profile)
sns_client = boto3.client('sns', region)
client = boto3.client('ec2', region)

today_date_utc = datetime.now(timezone.utc)
today_date = datetime.now()
running_reasons = []
stopped_reasons = []
msg_running=[]
msg_stopped=[]
transition_timestamps=[]

instance_ids = []
instance_names = []
running_instances = []
stopped_instances = []

running_file = './admins_running.csv'
stopped_file = './admins_stopped.csv'



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
            msg_running = running_admins(name, instance)
        else:
            msg_stopped = stopped_admins(name, instance)



    write_running_csv(msg_running)
    print(msg_running)
    bar_graph_running(running_file)
    write_stopped_csv(msg_stopped)   
    print(msg_stopped) 
    bar_graph_stopped(stopped_file)


def stopped_admins(name, instance):
    stopped_instances.append(instance)
    instance_ids.append(instance['InstanceId'])
    instance_names.append(name)
    stopped_reason = instance['StateTransitionReason']
    stopped_reasons.append(stopped_reason)
    transition_timestamp = datetime.strptime(instance['StateTransitionReason'][16:39], '%Y-%m-%d %H:%M:%S %Z')
    transition_timestamps.append(str(transition_timestamp))
    days=(today_date - transition_timestamp)
    # stopped_times = "InstanceID: " + instance['InstanceId'] + "," + ' Instance Name: ' +name + "," + " Shutdown Time: " + str(transition_timestamp) + "," + " Number of days stopped: " + str(days)
    stopped_times = [name, str(days)]
    msg_stopped.append(stopped_times)
    # msg_stopped.append("\n")
    # result = ''.join(msg_stopped)
    # else:
    #     msg_stopped = []
    return msg_stopped


def running_admins(name, instance):    
    running_instances.append(instance)
    instance_ids.append(instance['InstanceId'])
    instance_names.append(name)
    days=(today_date_utc - instance['LaunchTime']).days
    # running_times = "InstanceID: " + instance['InstanceId'] + "," + ' Instance Name: ' +name + "," + " Number of days running: " + str(days)
    running_times = [name, str(days)]
    msg_running.append(running_times)
    # msg_running.append("\n")
    # result = ''.join(msg_running)
    return msg_running


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
    plt.title("Running Admins")
    plt.ylabel("Number of days running")
    plt.xlabel("Instance Name")
    plt.xticks(rotation=45, ha='right')
    plt.show()

def pie_chart():
    pass

if __name__ == "__main__":
    main()
