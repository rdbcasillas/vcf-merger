#!/Users/rdbcasillas/miniconda3/bin/python
from argparse import ArgumentParser
import csv
from helperfuncs import getLinesWithLocation,getFormatTags,getAllPositions

parser = ArgumentParser()
requiredNamed = parser.add_argument_group('Required Arguments')
requiredNamed.add_argument("-v1", "--vcf1", dest = "vcf1",  help="First VCF", required=True)
requiredNamed.add_argument("-v2", "--vcf2", dest = "vcf2", help="Second VCF", required=True)
requiredNamed.add_argument("-o", "--output",dest ="output", help="Output merged file",  required=True)
requiredNamed.add_argument("-t", "--tools",dest = "tools", help="Comma separated list of tools to be merged" , required=True)

args = parser.parse_args()

tool1 = args.tools.split(',')[0]
tool2 = args.tools.split(',')[1]


chromLocations = set(getAllPositions(args.vcf1,args.vcf2))


def mergeVCFs(file1, file2):
    with open(args.output, 'a') as out:
        for loc in chromLocations:
            tmp1 =  getLinesWithLocation(loc, file1)
            tmp2 =  getLinesWithLocation(loc, file2)

            if len(tmp1) > 0 and len(tmp2) > 0:
                newlist = []
                vcf1cols = tmp1[0].split('\t')
                vcf2cols = tmp2[0].split('\t')
                newinfotags = vcf1cols[7] + ";" + vcf2cols[7] + ";calledBy=" + tool1 + "+" + tool2
                newformattags = getFormatTags(vcf1cols[8], vcf2cols[8], tool1, tool2)
                newformattagvals = vcf1cols[9].strip('\n') + ":" + vcf2cols[9].strip('\n')
                newlist.extend((vcf1cols[0], vcf1cols[1], vcf1cols[2], vcf1cols[3],vcf1cols[4],vcf2cols[5],vcf2cols[6],newinfotags,newformattags, newformattagvals))
                commonline = '\t'.join(newlist)
                out.write(commonline + "\n")
            elif len(tmp1) > 0 and len(tmp2) == 0:
                tmpcols = tmp1[0].split('\t')
                tmpcols[7] = tmpcols[7]+";"+ tool1 + "_Only"
                firstToolLine = '\t'.join(tmpcols)
                out.write(firstToolLine)
            else:
                tmpcols2 = tmp2[0].split('\t')
                tmpcols2[7] = tmpcols2[7]+";"+ tool2 + "_Only"
                secondToolLine = '\t'.join(tmpcols2)
                out.write(secondToolLine)

def sortOutput(unsortedvcf):
    with open(unsortedvcf, 'rt') as vcf, open("sorted_" + args.output, 'a') as outfile:
            outfile.write('##fileformat=VCFv4.1\n')
            outfile.write('##source=newmerge.py\n')
            outfile.write('\t'.join(['#CHROM','POS','ID','REF','ALT','QUAL','FILTER','INFO','FORMAT'])+'\n')
            reader = csv.reader(vcf, delimiter='\t')
            writer = csv.writer(outfile, delimiter='\t')
            writer.writerows(sorted(reader, key=lambda row: (int(row[0][3:]), int(row[1]))))

def main():
   mergeVCFs(args.vcf1,args.vcf2) 
   sortOutput(args.output)

if __name__ == "__main__":
    main()
