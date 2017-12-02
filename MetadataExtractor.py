import collections

ExtractedMetadata = collections.namedtuple("ExtractedMetadata", "sample hierarchy publication")

class MetadataExtractor:
    def __init__(self, known_samples):
        self.known_samples = known_samples

    def get_hierarchy_keys(self, metadata, key):
        entry = metadata[key]
        parent_key = entry.get_parent_key()
        if parent_key not in metadata:
            return [key]
        else:
            return_list = self.get_hierarchy_keys(metadata, parent_key)
            return_list.append(key)
            return return_list

    def extract_metadata(self, metadata, key):
        hierarchy_keys = self.get_hierarchy_keys(metadata, key)
        sample = self.find_sample(metadata, hierarchy_keys)
        hierarchy = [metadata[key].get_details() for key in hierarchy_keys]
        publication = None
        for item in hierarchy:
            if "et al. | " in item:
                publication = item

        return ExtractedMetadata(sample=sample, hierarchy=hierarchy, publication=publication)

    def find_sample(self, metadata, metadata_keys):
        found = self._search_iterable(self.known_samples, metadata_keys)
        if found is None:
            meta_details = [metadata[key].get_details() for key in metadata_keys]
            found = self._search_iterable(self.known_samples, meta_details)

        return found

    def _search_iterable(self, iterable, string_list):
        """
        Finds the first element in `iterable` that is a substring of one of the elements in string_list.
        Returns None if not found.
        """
        for item in iterable:
            for string in string_list:
                if item in string:
                    return item
        return None
