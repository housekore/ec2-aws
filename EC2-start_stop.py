##############################
# You will need to configure your AWS CLI credentials, either by setting the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables or by creating an AWS profile and configuring it in the CLI.
# Please make sure you double check the instances you are stopping before running the script
##############################

import boto3
from colorama import Fore, Style

# Connect to EC2
ec2 = boto3.client('ec2')

# Get list of running instances
instances = ec2.describe_instances()

# Print menu with options to stop or start instances
print(Fore.CYAN + "--------------------------------------")
print(Fore.CYAN + "Select the EC2 iInstance you want to manage:")
print(Fore.CYAN + "--------------------------------------")
for i, reservation in enumerate(instances["Reservations"]):
    for instance in reservation["Instances"]:
        name = next((tag["Value"] for tag in instance["Tags"] if tag["Key"] == "Name"), "No Name")
        status = instance["State"]["Name"]
        print(f"{Fore.CYAN}{i+1}. {instance['InstanceId']} - {name} - Status: {status}")
print(Style.RESET_ALL)

# Get user input
user_input = int(input())
instance_id = instances["Reservations"][user_input-1]["Instances"][0]["InstanceId"]

# Ask user if they want to start or stop the instance
action = input("Do you want to start or stop the instance? Input: (start or stop):")

if action == "start":
    ec2.start_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} started.")
elif action == "stop":
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f"Instance {instance_id} stopped.")
else:
    print("Invalid input. Exiting.")

