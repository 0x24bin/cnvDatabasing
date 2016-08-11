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

def is_valid_dir(parser,arg):
    arg = os.path.abspath(arg)
    if not os.path.isdir(arg):
        parser.error("readable_dir:{0} is not a valid path".format(arg))
    else:
        return arg

parser = argparse.ArgumentParser(description='Load CNV data to centeralized database.')
parser.add_argument("-f", "--meta",
                    dest="filename",
                    type=lambda x: is_valid_file(parser, x),
                    help="Tab-delimited file meta data (sample name first column)",
                    metavar="FILE",required=True)
parser.add_argument("-d", "--dir",
                    dest="directory",
                    type=lambda x: is_valid_dir(parser, x),
                    help="Input directory containing CNV datafiles",
                    metavar="DIR",required=True)
args = parser.parse_args()


####### Setup database connection #######
client = MongoClient('localhost', 27017)
#client = MongoClient('10.146.103.76', 27017)
db = client["cnvDB-test"]
cnvSmp = db["meta"]
cnvClc = db["cnv"]


####### Detect and Load This Meta Data ######
sampleMap = {}
metaCSVFile = csv.reader(open(args.filename), delimiter='\t')
metaCSVHeaders = metaCSVFile.next()
metaCSVHeaders = [s.replace('.', '_') for s in metaCSVHeaders]
for row in metaCSVFile:
    my_Samp = dict(zip(metaCSVHeaders, row))
    _id = cnvSmp.insert(loads(dumps(my_Samp)))
    sampleMap[row[0]] = _id


for i in os.listdir(args.directory):
    fname = os.path.basename(i).split("(")[0]

    if fname in sampleMap:
        id = sampleMap[fname]
        print "Uploading: {}".format(i)
        sCSVFile = csv.reader(open(os.path.join(args.directory,i)), delimiter='\t')

        if i.endswith('_CNV.txt'):   #args.ftype == 'EXON':
            sCSVHeaders = sCSVFile.next()
            sCSVHeaders = [s.replace('.', '_') for s in sCSVHeaders]
            for row in sCSVFile:
                row[1] = int(row[1])
                row[2] = int(row[2])
                for e in [4,5,6,7,8]:
                    row[e] = float(row[e])
                my_Var = dict(zip(sCSVHeaders, row))
                my_Var["Sample"] = id
                my_Var["SampleName"] = fname
                my_Var["varType"]="EXON"
                cnvClc.insert(loads(dumps(my_Var)))
        elif i.endswith('_CNV_seg_.txt'):  #args.ftype == 'SEG':
            sCSVHeaders = ["chr","start_pos","stop_pos","CNV_log2ratio","N_exon"]
            for row in sCSVFile:
                row[1] = int(row[1])
                row[2] = int(row[2])
                row[3] = float(row[3])
                row[4] = int(row[4])

                my_Var = dict(zip(sCSVHeaders, row))
                my_Var["Sample"] = id
                my_Var["SampleName"] = fname
                my_Var["varType"]="SEG"
                cnvClc.insert(loads(dumps(my_Var)))
        else:
            print "Uncertain File Type: {}".format(i)



    else:
        print "No Data File for: {}".format(fname)

