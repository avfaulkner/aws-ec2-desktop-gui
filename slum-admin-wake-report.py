#!/usr/bin/python3.8
import boto3
from datetime import datetime, timezone
import csv 
import matplotlib.pyplot as plt
import pandas


region = 'us-east-1'
sns_client = boto3.client('sns', region)
client = boto3.client('ec2', region)

today_date = datetime.now(timezone.utc)
running_reasons = []
msg_running=[]
transition_timestamps=[]

instance_ids = []
instance_names = []
running_instances = []
file = './admins.csv'



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
            'Values': ['running']
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
        running_instances.append(instance)
        instance_ids.append(instance['InstanceId'])
        instance_names.append(name)

        days=(today_date - instance['LaunchTime']).days
        # running_times = "InstanceID: " + instance['InstanceId'] + "," + ' Instance Name: ' +name + "," + " Number of days running: " + str(days)
        running_times = [name, str(days)]
        msg_running.append(running_times)
        # msg_running.append("\n")
        # result = ''.join(msg_running)
    write_csv(msg_running)
    print(msg_running)
    bar_graph(file)

def write_csv(data):
    header = ['Instance Name', 'Number of days running']
    with open(file, 'w') as admins_running:
        writer = csv.writer(admins_running)
        writer.writerow(header)
        writer.writerows(data)

def bar_graph(file):
    data = pandas.read_csv(file)
    df = pandas.DataFrame(data)
    X = list(df.iloc[:, 0])
    Y = list(df.iloc[:, 1])
    plt.bar(X, Y, color='g')
    plt.title("Running Admins")
    plt.xlabel("Number of days running")
    plt.ylabel("Instance Name")
    plt.show()

if __name__ == "__main__":
    main()
