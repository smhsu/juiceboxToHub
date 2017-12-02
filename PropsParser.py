import sys

PARENT_KEY_COLUMN = 0
DETAILS_COLUMN = 1
URL_COLUMN = -1

class PropertyEntry:
    def __init__(self, line_number, columns):
        self.line_number = line_number
        self.columns = columns
    
    def get_parent_key(self):
        return self._safe_get_column(PARENT_KEY_COLUMN)
    
    def get_details(self):
        return self._safe_get_column(DETAILS_COLUMN)

    def get_url(self):
        return self._safe_get_column(URL_COLUMN)

    def is_track(self):
        url = self.get_url()
        return url.startswith("http")

    def _safe_get_column(self, index):
        if len(self.columns) > index:
            return self.columns[index]
        else:
            return None

    def __repr__(self):
        return str(self.line_number) + ": " + repr(self.columns)

class PropsParser:
    def parse_file(self, file_name):
        entries = {}
        line_number = 0
        with open(file_name, "r") as input_file:
            for line in input_file:
                line_number += 1

                if line.startswith("#"):
                    continue

                split = line.split("=", 1)
                if len(split) < 2:
                    continue

                key = split[0].strip()
                if key in entries:
                    print("Warning (line {}): duplicate key `{}`.  ".format(line_number, key) + 
                        "Previous mentions of the key will be discarded.", file=sys.stderr)
                value = split[1]
                value_columns = [item.strip() for item in value.split(",")]
                entries[key] = PropertyEntry(line_number, value_columns)

        return entries
