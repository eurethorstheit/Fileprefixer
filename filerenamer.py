'''File loading and renaming'''

import os
import fnmatch
import re
from operator import itemgetter


class FileRenamer:
    def __init__(self, directory, suffix):
        self.directory = directory
        self.suffix = suffix
        self.filter = "*" + self.suffix
        self.regex = (r"^(\d+_){0,1}(.+" + re.escape(suffix) + r")$")
        self.items = []

    def get_directory(self):
        return self.directory

    def get_suffix(self):
        return self.suffix

    def refresh(self):
        self.items = []

        try:
            files = os.listdir(self.directory)
        except FileNotFoundError:
            print("directory", self.directory, "does not exist")
            files = []

        for item in sorted(files):
            if fnmatch.fnmatch(item, self.filter):
                match = re.search(self.regex, item)
                if match:
                    # (orig, base, if numbered)
                    self.items.append(
                        (item, match.group(2), bool(match.group(1))))

        return [i[0] for i in self.items]

    def rename(self):
        if not any(not x[2] for x in self.items):
            print("files already sorted")
            return

        sorted_items = sorted(
            self.items,
            # sort all already numbered files at first
            key=lambda x: str(int(not x[2])) + x[1])

        # renumber and rename files
        for number, (orig, base, _) in enumerate(sorted_items, 1):
            renamed = "{0:03d}_{1}".format(number, base)
            if orig == renamed:
                print("renaming", orig, "skipped")
            else:
                print("renaming", orig, "->", renamed)
                os.rename(
                    os.path.join(self.directory, orig),
                    os.path.join(self.directory, renamed))
