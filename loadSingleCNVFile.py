__author__ = 'm088378'

import sys, os, csv
import pymongo
from pymongo import MongoClient
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


parser = ArgumentParser(description='Load CNV data to centeralized database.')
parser.add_argument("-f", "--file",dest="filename",
                    type=lambda x: is_valid_file(parser, x),
                    help="Input file containing CNV data.",
                    metavar="FILE",
                    required=True)
parser.add_argument("-t", "--type",dest="ftype",
                    help="File Format. Type of file (EXON/SEG)",
                    required=True)
parser.add_argument("-s", "--study",dest="study",
                    help="Single descriptive word to tie this sample")
parser.add_argument("-p", "--person",dest="pi",
                    help="Single descriptive PI name to tie this sample")
parser.add_argument("-m", "--meta",dest="metafile",
                    type=lambda x: is_valid_file(parser, x),
                    help="Input xml file containing key value pairs of metadata. (not working)",
                    metavar="FILE")
args = parser.parse_args()



####### Setup database connection #######
client = MongoClient('localhost', 27017)
#client = MongoClient('10.146.103.76', 27017)
db = client["cnvDB-test"]
cnvClc = db["cnv"]
cnvSmp = db["meta"]


###### Get Sample Name from Filename #######
base=os.path.basename(args.filename)
sname=base.split("(")[0]

####### Single Sample Meta ##########
my_Samp = {"Sample":sname}
if args.study is not None:
    my_Samp['Study'] = args.study
if args.pi is not None:
    my_Samp['PI'] = args.pi

_id = cnvSmp.insert(loads(dumps(my_Samp)))


####### Load each CNV data entry #######
sCSVFile = csv.reader(open(args.filename), delimiter='\t')
if args.ftype == 'EXON':
    sCSVHeaders = sCSVFile.next()
    sCSVHeaders = [s.replace('.', '_') for s in sCSVHeaders]
    for row in sCSVFile:
        row[1] = int(row[1])
        row[2] = int(row[2])
        for e in [4,5,6,7,8]:
            row[e] = float(row[e])
        my_Var = dict(zip(sCSVHeaders, row))
        my_Var["Sample"] = _id
        my_Var["SampleName"] = sname
        my_Var["varType"]="EXON"
        #pprint(my_Var)
        cnvClc.insert(loads(dumps(my_Var)))

elif args.ftype == 'SEG':
    sCSVHeaders = ["chr","start_pos","stop_pos","CNV_log2ratio","N_exon"]
    for row in sCSVFile:
        row[1] = int(row[1])
        row[2] = int(row[2])
        row[3] = float(row[3])
        row[4] = int(row[4])

        my_Var = dict(zip(sCSVHeaders, row))
        my_Var["Sample"] = _id
        my_Var["SampleName"] = sname
        my_Var["varType"]="SEG"
        #pprint(my_Var)
        cnvClc.insert(loads(dumps(my_Var)))


else:
    print "Uncertain File Type"


