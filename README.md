###loadSingleCNVFile.py
Accepts one file, two possible formats, resulting from PatternCNV.


Commandline examples:
    python loadSingleCNVFile.py -f segmentData/s_SN1_JW_CNV_seg.txt -t SEG -p Moore_Raymond -s ThisBigStudy -c Germline
    python loadSingleCNVFile.py -f exonData/s_SN1_JW_CNV.txt -t EXON -p Moore_Raymond -s ThisBigStudy -c Somatic


###loadMultiCNVDir_metaFile.py
Accepts one tab-delimited file, first column is samplename, which correspondes to filename.
Load every file within given directory two possible formats, resulting from PatternCNV.

Commandline examples:
    python loadMultiCNVDir_metaFile.py -f segmentInput_meta.tsv -d segmentData/ -t SEG
    python loadMultiCNVDir_metaFile.py -f exonInput_meta.tsv -d exonData/ -t EXON

