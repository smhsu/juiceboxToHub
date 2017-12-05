import json
import copy
import HubConfig

DEFAULT_VOCAB = {
    "Assay": "http://vizhub.wustl.edu/metadata/Experimental_assays",
    "Institution": "http://vizhub.wustl.edu/metadata/Institutions"
}

HEADER = {
    "show_terms": {
        "Sample": [
            "Sample"
        ],
        "Assay": [
            "Assay"
        ]
    },
    "vocabulary_set": DEFAULT_VOCAB,
    "type": "metadata",
    "facet_table": [
        "Sample",
        "Assay"
    ]
}

BASE_TRACK_OBJECT = {
    "qtc": {
        "unit_res": "BP",
        "matrix": "oe",
        "norm": "KR",
        "hasChr": 1,
        "bin_size": 0
    }, 
    "name": None,
    "url": None,
    "height": 50,
    "mode": "hide",
    "metadata": {
        "Sample": None,
        "Assay": "27003"
    }, 
    "type": "hic",
    "public": True,
    "defaultmode": "trihm"
}

class HubWriter:
    def __init__(self, file_suffix):
        self.file_suffix = file_suffix

    def write_hubs(self, tracks):
        species_to_tracks = {}
        for track in tracks:
            if track.species not in species_to_tracks:
                species_to_tracks[track.species] = []
            species_to_tracks[track.species].append(track)

        for (species, tracks) in species_to_tracks.items():
            out_name = species.value + self.file_suffix
            with open(out_name, "w") as out:
                # Header (er, first item) stuff
                header = HEADER.copy()
                vocab = {**DEFAULT_VOCAB, **HubConfig.species_to_custom_vocab[species]} # Merge the two dicts
                header["vocabulary_set"] = vocab
                blob = [header]

                for track in tracks:
                    if None in (track.name, track.url, track.sample):
                        raise ValueError("One of track objects has missing information")
                    track_blob = copy.deepcopy(BASE_TRACK_OBJECT)
                    track_blob["name"] = track.name
                    track_blob["url"] = track.url
                    track_blob["metadata"]["Sample"] = track.sample
                    if (track.details):
                        track_blob["details"] = track.details
                    blob.append(track_blob)

                json.dump(blob, out, indent=4)
            
            print("Wrote {} tracks to {}.".format(len(tracks), out_name))
