import collections
from enum import Enum

class Species(Enum): # Each species will be written to a hub file called "$species_name-juiceboxhub"
    HUMAN = "hg19"
    MOUSE = "mm9"

ignore = [ # Property keys that match these strings will be ignored.
    "_Other_MiSeq",
    "3PNAS_2016_3Rhesus",
    "5biorxiv_2017",
    "4Science_2017",
    "Drosophila",
    "External_rowley2017", # Contains 5 Drosophila tracks, among others
    "External_2014Feng", # Arabidopsis.  https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4347903/
]

SampleInfo = collections.namedtuple("SampleInfo", "id species")

sample_lookup = { # The script will look in the input's keys and fields for a mention of ANY of these
    "HeLa":    SampleInfo("14001", Species.HUMAN),
    "HUVEC":   SampleInfo("13052", Species.HUMAN),
    "KBM7":    SampleInfo("14051", Species.HUMAN),
    "K562":    SampleInfo("14018", Species.HUMAN),
    "NHEK":    SampleInfo("13056", Species.HUMAN),
    "HMEC":    SampleInfo("13049", Species.HUMAN),
    "IMR90":   SampleInfo("11310", Species.HUMAN),
    "GM12878": SampleInfo("13047", Species.HUMAN),
    "Kalhor":  SampleInfo("13047", Species.HUMAN),
    "Hap1":    SampleInfo("15049", Species.HUMAN),
    "GM06990": SampleInfo("13076", Species.HUMAN),
    "RWPE1":   SampleInfo("13293", Species.HUMAN),
    "NB4":     SampleInfo("14008", Species.HUMAN),
    # FIXME so RPE1 cells are Human Retinal Pigment Epithelial Cells, similar to "HRPEpiC" cells, but they are not
    # HRPEpiC.  So I've just specified them as eye cells.
    "RPE1":    SampleInfo("15037", Species.HUMAN),
    "HEK293":  SampleInfo("12220", Species.HUMAN),

    "Patski":                   SampleInfo("10007", Species.MOUSE),
    "CH12-LX":                  SampleInfo("10003", Species.MOUSE),
    "External_2015Rudan_mouse": SampleInfo("10009", Species.MOUSE),
    "2012Dixon_mES_HindIII":    SampleInfo("10049", Species.MOUSE),
    "mES_cortex":               SampleInfo("10031", Species.MOUSE),
    "mNSC":                     SampleInfo("10084", Species.MOUSE),
    "mAST":                     SampleInfo("10085", Species.MOUSE),
    "2013Seitan_Tcell_Rad21":   SampleInfo("10086", Species.MOUSE),
    "Mouse brain":              SampleInfo("10019", Species.MOUSE),
    "2013Nagano_cell":          SampleInfo("10080", Species.MOUSE),
    "External_2012Zhang":       SampleInfo("10050", Species.MOUSE)
}

species_to_custom_vocab = { # Custom props for each species' "vocabulary"
    Species.HUMAN: {
            "Sample": "http://vizhub.wustl.edu/metadata/human/Samples",
            "Donor": "http://vizhub.wustl.edu/metadata/human/Donor",
        },
    Species.MOUSE: {
            "Sample": "http://vizhub.wustl.edu/metadata/mouse/Samples",
        },
}
