from re import match
def getAllPositions(file1, file2):
    """Collects all the positions in two vcfs without duplicates"""
    locationArray = []
    with open(file1, 'rt') as vcf1:
        for line1 in vcf1:
            if not match('^#', line1):
                columns = line1.split('\t')
                #chromosome = columns[0]
                position = columns[1]
                locationArray.append(position)
                
    with open(file2, 'rt') as vcf2:
        for line2 in vcf2:
            if not match('^#', line2):
                columns = line2.split('\t')
                #chromosome = columns[0]
                position = columns[1]
                locationArray.append(position)
    return list(set(locationArray))


def getLinesWithLocation(chromloc, vcf):
    """Takes a location and fetches the corresponding line in the vcf"""
    myline = []
    with open(vcf, 'rt') as vcflines:
        for line in vcflines:
            if chromloc in line:
                myline.append(line)
    return myline


def getFormatTags(format1, format2, tool1, tool2):
    """Updates the common FORMAT tags by adding respective tool names"""
    formatTags = []
    format1 = format1.split(':')
    format2 = format2.split(':')
    for i in range(len(format1)):
        if format1[i] in format2:
            formatTags.append(tool1+ "_" + format1[i])
        else:
            formatTags.append(format1[i])
    
    for i in range(len(format2)):
        if format2[i] in format1:
            formatTags.append(tool2 + "_" + format2[i])
        else:
            formatTags.append(format2[i])

    return ':'.join(formatTags)