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

curBool = cnvSmp.find({args.attribute : {'$exists':1}})
if curBool.count() < 1:
    sys.stderr.write("No Attribute Exists: {}\n\n".format(args.attribute))
    quit()


map = Code("function(){ for (var key in this) { emit(key, null); }}")
reduce = Code("function(key, stuff) { return null; }")
allFields = cnvSmp.map_reduce(map, reduce, "meta_keys")
fieldList = []
for doc in allFields.find():
    if doc["_id"] == "_id":
        continue
    fieldList.append(doc["_id"])

sfieldList = sorted(fieldList)
print( "DatabaseID\t{}".format("\t".join(sfieldList)) )

qMetaRez = cnvSmp.find({args.attribute : args.metavalue})
for doc in qMetaRez:
    vals = [doc[e] for e in sfieldList]
    print("{}\t{}".format( str(doc['_id']),"\t".join(vals) ) )
    #pprint(vals)