import sys
import collections
import HubConfig
from PropsParser import PropsParser
from MetadataExtractor import MetadataExtractor
from HubWriter import HubWriter

Track = collections.namedtuple("Track", "species name url sample details")

def should_ignore(key):
    for ignore_string in HubConfig.ignore:
        if ignore_string in key:
            return True
    return False

def make_track_object(all_entries, key, entry, meta_extractor):
    metadata = meta_extractor.extract_metadata(all_entries, key)
    if metadata.sample is None:
        print("Could not match sample or cell line for track {} (line {}); skipping...".format(key, entry.line_number),
            file=sys.stderr)
        return None

    (sample_id, species) = HubConfig.sample_lookup[metadata.sample]
    name = key.replace("__External_", "")
    details = {"Juicebox path": " > ".join(metadata.hierarchy)}
    if metadata.publication:
        details["Publication"] = metadata.publication
    return Track(species=species, name=name, url=entry.get_url(), sample=sample_id, details=details)

def main(args):
    parser = PropsParser()
    meta_extractor = MetadataExtractor(HubConfig.sample_lookup)

    tracks_to_write = []
    total_ignored = 0
    prop_entries = parser.parse_file(args[1])
    for (key, entry) in prop_entries.items():
        if entry.is_track():
            if should_ignore(key):
                total_ignored += 1
                continue

            track = make_track_object(prop_entries, key, entry, meta_extractor)
            if track is None:
                total_ignored += 1
            else:
                tracks_to_write.append(track)
    
    writer = HubWriter()
    writer.write_hubs(tracks_to_write)
    print("Total tracks written: {}\nTotal tracks skipped or ignored: {}".format(len(tracks_to_write), total_ignored))

if __name__ == "__main__":
    main(sys.argv)
