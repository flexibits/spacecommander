# ReplaceAtImport.py
# Convert "@import Foundation" to "#import <Foundation/Foundation.h>"
#
# If a filename is specified as a parameter, it will change that file in place.
# If input is provided through stdin, it will send the result to stdout.

from AbstractCustomFormatter import AbstractCustomFormatter
import re

class ReplaceAtImport(AbstractCustomFormatter):
    def format_lines(self, lines):

        lines_to_write = []
        for line in lines:
            to_append = line

            if line.strip().startswith("@import "):
                to_append = re.sub("@import (\\w+);", "#import <\\1/\\1.h>", line)

            lines_to_write.append(to_append)

        return "".join(lines_to_write)

if __name__ == "__main__":
    ReplaceAtImport().run()
