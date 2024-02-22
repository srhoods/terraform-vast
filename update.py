#!/usr/bin/env python3

import json
import re
import sys
import argparse

def read_hcljson(FILE):
    with open(FILE, 'r') as file:
        try:
            dict = json.load(file)
        except:
            print("Failed to open file")
            exit(1)
        return dict

def write_hcljson(FILE, DICT):
    with open(FILE, 'w') as file:
        try:
            json.dump(DICT, file, indent=2)
        except:
            print("Failed to write file")
            exit(1)
        return 0

def quota_valid(QUOTA):
    if isinstance(QUOTA, int) == False:
        return False
    if QUOTA < 1:
        return False
    return True

def view_valid(VIEW, DICT):
    for item in DICT['locals'][0]['NFS_VIEWS']:
        if item == VIEW:
            return True
    return False

def update_quota(VIEW, DICT, QUOTA):
    # Check if View exists
    if view_valid(VIEW, DICT) == False:
        print('Unable to find view')
        exit(2)

    # Check if quota is a valid int
    if quota_valid(QUOTA) == False:
        print('Quota is not a valid integer')
        exit(2)

    update = re.sub("'hard_limit_gib': [0-9]+","'hard_limit_gib': " + str(QUOTA),DICT['locals'][0]['NFS_VIEWS'][VIEW])
    DICT['locals'][0]['NFS_VIEWS'][VIEW] = update

    # Return updated DICT if successful
    return DICT


parser = argparse.ArgumentParser(
                    prog='Terraform_VAST_Quota_Updater',
                    description='Updates the quota value in a Terraform JSON file')

parser.add_argument('filename', type=str, help="Terraform environment file (json format)")
parser.add_argument('--view', type=str, help="Name of VAST view to modify", required=True)
parser.add_argument('--quota', type=int, help="New Quota size in GiB", required=True)
args = parser.parse_args()

dict = read_hcljson(args.filename)
#print("BEFORE: ", dict)

write_hcljson(args.filename, update_quota(args.view, dict, args.quota))

#print()
#print("AFTER: ", dict)
