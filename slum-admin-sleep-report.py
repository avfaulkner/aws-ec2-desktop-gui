#!/usr/bin/python3.8
from unittest import result
import boto3
import botocore
from datetime import datetime
import os

region = 'us-east-1'
sns_client = boto3.client('sns', region)
client = boto3.client('ec2', region)

today_date = datetime.now()
stopped_reasons = []
msg_stopped=[]
transition_timestamps=[]

instance_ids = []
instance_names = []
stopped_instances = []


def lambda_handler():
    # Use the filter() method of the instances collection to retrieve
    # all stopped Admin instances who have opted into the slumbering admin program. 
    filters = [
        {
            'Name': 'tag:t_role',
            'Values': ['Admin']
        },
        {
            'Name': 'instance-state-name', 
            'Values': ['stopped']
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
        stopped_instances.append(instance)
        instance_ids.append(instance['InstanceId'])
        instance_names.append(name)

        stopped_reason = instance['StateTransitionReason']
        stopped_reasons.append(stopped_reason)
        transition_timestamp = datetime.strptime(instance['StateTransitionReason'][16:39], '%Y-%m-%d %H:%M:%S %Z')
        transition_timestamps.append(str(transition_timestamp))
        days=(today_date - transition_timestamp).days
        stopped_times = "InstanceID: " + instance['InstanceId'] + "," + ' Instance Name: ' +name + "," + " Shutdown Time: " + str(transition_timestamp) + "," + " Number of days stopped: " + str(days)
        msg_stopped.append(stopped_times)
        msg_stopped.append("\n")
        result = ''.join(msg_stopped)

        print(result)

        # if days >= 6:
        #     sns_client.publish(
        #         TopicArn = os.getenv('topic_arn'),
        #         Subject = "Stopped Admin Report",
        #         Message = result
        #         )
        # else:
        #     result = "There are no stopped admins"
         


if __name__ == "__main__":
    lambda_handler()
