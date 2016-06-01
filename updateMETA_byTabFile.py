__author__ = 'm088378'

import sys, os, csv
import pymongo
from pymongo import MongoClient
from bson.code import Code
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
from pprint import pprint

from argparse import ArgumentParser


def is_valid_file(parser, arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

parser = ArgumentParser(description='Query Meta data from centeralized database.')
parser.add_argument("-f", "--meta",
                    dest="filename",
                    type=lambda x: is_valid_file(parser, x),
                    help="Tab-delimited file meta data (sample name first column)",
                    metavar="FILE",required=True)
args = parser.parse_args()


####### Setup database connection #######
client = MongoClient('localhost', 27017)
#client = MongoClient('10.146.103.76', 27017)
db = client["cnvDB-test"]
cnvSmp = db["meta"]

metaCSVFile = csv.reader(open(args.filename), delimiter='\t')
metaCSVHeaders = metaCSVFile.next()
metaCSVHeaders = [s.replace('.', '_') for s in metaCSVHeaders]

for row in metaCSVFile:
    my_Samp = dict(zip(metaCSVHeaders, row))
    my_Samp = {key: value for key, value in my_Samp.items() if value is not '.'}
    pprint(my_Samp)
    dbMatch = cnvSmp.find( {"_id": ObjectId(my_Samp['DatabaseID'])} )
    pprint(dbMatch)

    #_id = cnvSmp.insert(loads(dumps(my_Samp)))
    #sampleMap[row[0]] = _id