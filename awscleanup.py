#!/usr/bin/python
import boto3
import botocore
import datetime
# Loop trough all regions with this to do it general:
# boto3.setup_default_session(region_name='eu-central-1')
ec2 = boto3.resource('ec2')


def volume_cleanup():
    """ Cleanup volumes that are not in use and are older than a week """
    print("Cleaning up volumes")
    for volume in ec2.volumes.all():
        if volume.state == "available" and \
           volume.create_time.replace(tzinfo=None) < \
           datetime.datetime.now()-datetime.timedelta(hours=7):
            print ("Deleting volume " + volume.id)
            try:
                volume.delete()
            except botocore.exceptions.ClientError:
                print("Error deleting volume, probably already" +
                      "deleted by instance termination")


def instance_cleanup():
    """ Terminate instances that are older than a month """
    print("Cleaning up instances")
    for instance in ec2.instances.all():
        if instance.launch_time.replace(tzinfo=None) < \
           datetime.datetime.now()-datetime.timedelta(days=7):
            print("Terminating instnace " + instance.id)
            try:
                instance.terminate()
            except botocore.exceptions.ClientError:
                print("Instance " + instance.id +
                      " has termination protection enabled")


def elastic_ips_cleanup():
    """ Cleanup elastic IPs that are not being used """
    print("Cleaning up elastic IPs")
    client = boto3.client('ec2')
    addresses_dict = client.describe_addresses()
    for eip_dict in addresses_dict['Addresses']:
        if "InstanceId" not in eip_dict:
            print (eip_dict['PublicIp'] +
                   " doesn't have any instances associated, releasing")
            try:
                client.release_address(AllocationId=eip_dict['AllocationId'])
            except botocore.exceptions.ClientError:
                print("IP " + eip_dict['PublicIp'] +
                      " is being used")


def main():
    client = boto3.client('ec2')
    regions = client.describe_regions()['Regions']
    for region in regions:
        print("Working on region " + region['RegionName'])
        boto3.setup_default_session(region_name=region['RegionName'])
        global ec2
        ec2 = boto3.resource('ec2')
        instance_cleanup()
        volume_cleanup()
        elastic_ips_cleanup()

if __name__ == "__main__":
    main()
