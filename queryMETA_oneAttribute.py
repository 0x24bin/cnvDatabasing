__author__ = 'm088378'

import sys, os, csv
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from pprint import pprint

from argparse import ArgumentParser

parser = ArgumentParser(description='Query Meta data from centeralized database.')
parser.add_argument("-a", "--attrib",dest="attribute",
                    help="Known attribute for querying samples metadata",required=True)
parser.add_argument("-v", "--value",dest="metavalue",
                    help="Filter value, from query attribute",required=True)
args = parser.parse_args()


####### Setup database connection #######
client = MongoClient('localhost', 27017)
#client = MongoClient('10.146.103.76', 27017)
db = client["cnvDB-test"]
cnvSmp = db["meta"]


