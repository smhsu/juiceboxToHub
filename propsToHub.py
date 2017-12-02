#!/usr/bin/python
# programmer : Daofeng
# usage:

import sys,json

meta =    {
        "show_terms": {
            "Sample": [
                "Sample"
            ],
            "Assay": [
                "Assay"
            ]
        },
        "vocabulary_set": {
            "Sample": "http://vizhub.wustl.edu/metadata/human/Samples",
            "Donor": "http://vizhub.wustl.edu/metadata/human/Donor",
            "Assay": "http://vizhub.wustl.edu/metadata/Experimental_assays",
            "Institution": "http://vizhub.wustl.edu/metadata/Institutions"
        },
        "type": "metadata",
        "facet_table": [
            "Sample",
            "Assay"
        ]
    }

sample2id = {
    'HeLa':'14001',
    'HUVEC':'13052',
    'KBM7':'14051',
    'K562':'14018',
    'NHEK':'13056',
    'HMEC':'13049',
    'IMR90':'11310',
    'GM12878':'13047',
    #'':'',
    'CH12-LX':'10003',
}

def main():
    tklst = []
    tklst.append(meta)
    with open('juicebox.properties',"rU") as infile:
        #with open('hg19-juiceboxhub','w') as outfile:
        with open('ext-juiceboxhub','w') as outfile:
            for line in infile:
                #if line.startswith('2PNAS_2015'): break  # this one added manually
                if line.strip().endswith('.hic'):
                    if '__External' in line:
                        t = line.strip().split('=')
                        tk = {}
                        tk['name'] = t[0].strip().replace('__External_','')
                        tk['url'] = t[1].strip().split(',')[-1].strip()
                        tk['type'] = 'hic'
                        tk['defaultmode'] = 'trihm'
                        tk['public'] = True
                        tk['mode'] = 'hide'
                        tk['height'] = 50
                        tk['metadata'] = {}
                        tk['metadata']['Sample'] = 0
                        tk['metadata']['Assay'] = '27003'
                        tk['qtc'] = {}
                        tk['qtc']['matrix'] = 'oe'
                        tk['qtc']['norm'] = 'KR'
                        tk['qtc']['unit_res'] = 'BP'
                        tk['qtc']['bin_size'] = 0
                        tklst.append(tk)
                    else:
                        continue
                        t = line.strip().split('=')
                        tk = {}
                        tk['name'] = t[0].strip()
                        sample = t[0].lstrip('_').split('_')[0]
                        if sample not in sample2id:
                            print "Warning: could not find id for sample " + sample
                            continue
                        #tk['sample'] = sample2id[sample]
                        tk['url'] = t[1].strip().split(',')[-1].strip()
                        tk['type'] = 'hic'
                        tk['defaultmode'] = 'trihm'
                        tk['public'] = True
                        tk['mode'] = 'hide'
                        tk['height'] = 50
                        tk['metadata'] = {}
                        tk['metadata']['Sample'] = sample2id[sample]
                        tk['metadata']['Assay'] = '27003'
                        tk['qtc'] = {}
                        tk['qtc']['matrix'] = 'oe'
                        tk['qtc']['norm'] = 'KR'
                        tk['qtc']['unit_res'] = 'BP'
                        tk['qtc']['bin_size'] = 0
                        tklst.append(tk)
            print 'tracks:',len(tklst) - 1
            json.dump(tklst, outfile, indent=4)

if __name__=="__main__":
    main()


