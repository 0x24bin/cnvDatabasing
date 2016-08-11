__author__ = 'm088378'

import sys, os, csv
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.json_util import dumps
from bson.json_util import loads
import argparse


def is_valid_file(parser, arg):
    arg = os.path.abspath(arg)
    if not os.path.exists(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

parser = argparse.ArgumentParser(description='Load CNV Matrix-Format data to centeralized database.')
parser.add_argument("-f", "--input",
                    dest="input",
                    type=lambda x: is_valid_file(parser, x),
                    help="Tab-delimited text file.",
                    metavar="FILE",required=True)
parser.add_argument("-m", "--meta",
                    dest="meta",
                    type=lambda x: is_valid_file(parser, x),
                    help="Meta File (sample name first column)",
                    metavar="FILE",required=True)
args = parser.parse_args()


####### Setup database connection #######
client = MongoClient('localhost', 27017)
#client = MongoClient('10.146.103.76', 27017)
db = client["cnvDB-test"]
cnvSmp = db["meta"]
cnvClc = db["cnv"]


####### Detect and Load This Meta Data ######
sampleMap = {}
metaCSVFile = csv.reader(open(args.meta), delimiter='\t')
metaCSVHeaders = metaCSVFile.next()
metaCSVHeaders = [s.replace('.', '_') for s in metaCSVHeaders]
for row in metaCSVFile:
    my_Samp = dict(zip(metaCSVHeaders, row))
    _id = cnvSmp.insert(loads(dumps(my_Samp)))
    sampleMap[row[0]] = _id


##### Load Matrix of CNV Data #####
####### Load each CNV data entry #######
sCSVFile = csv.reader(open(args.input), delimiter='\t')
dataDimensionLine = sCSVFile.next()
dataTypeLine = sCSVFile.next()
dataTypeArr = dataTypeLine[0].split("=")
print dataTypeArr
sCSVHeaders = sCSVFile.next()
sCSVHeaders = [s.replace('.', '_') for s in sCSVHeaders]

for row in sCSVFile:
    acc = {'k':row[0], 'v':row[1]}
    vals = {'varType':dataTypeArr[1], 'chr':row[2], 'start':int(row[3]), 'end':int(row[4]), 'features':acc}
    print acc
    for e in range(5, len(row)):
        sname = sCSVHeaders[e]
        my_Var = vals
        my_Var['log2ratio'] = float(row[e])
        my_Var["Sample"] = sampleMap[sname]
        my_Var["SampleName"] = sname
        cnvClc.insert(loads(dumps(my_Var)))