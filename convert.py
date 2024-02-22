#!/usr/bin/env python3

import hcl2 # pip install python-hcl2
import json
import re
import sys
import argparse

def read_hcl(FILE):
    with open(FILE, 'r') as file:
        try:
            dict = hcl2.load(file)
        except:
            print("Failed to open source file")
            exit(1)
        return dict

def write_hcljson(FILE, DICT):
    with open(FILE, 'w') as file:
        try:
            json.dump(DICT, file, indent=2)
        except:
            print("Failed to write destination file")
            exit(1)
        return 0

parser = argparse.ArgumentParser(
                    prog='Terraform HCL to JSON Converter',
                    description='Takes a source Terraform file in native HCL format and converts it to JSON')

parser.add_argument('--source', type=str, help="Source HCL File", required=True)
parser.add_argument('--destination', type=str, help="Destination JSON File", required=True)
args = parser.parse_args()

write_hcljson(args.destination, read_hcl(args.source))
