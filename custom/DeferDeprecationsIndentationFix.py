# DeferDepracationIndentationFixer.py
# clang-format gets confused by BEGIN_DEFER_DEPRECATION_UNTIL_IOS_<> and
# END_DEFER_DEPRECATION_UNTIL_IOS_<>, indenting the line after them wrongly.
#
from AbstractCustomFormatter import AbstractCustomFormatter
import re

class DeferDepracationIndentationFixer(AbstractCustomFormatter):
    def format_lines(self, lines):

        lines_to_write = lines
        for index, line in enumerate(lines):
            lines_to_write[index] = line

            begin_defer_match = re.match(r"^(\s*)BEGIN_DEFER_DEPRECATION_UNTIL_IOS_[\d]{2}", line)
            if begin_defer_match:
                whitespace = begin_defer_match.group(1)

                # next line afer beginning a deprecation block must match the
                # previous line indentation (lines after it are usually fine).
                if index + 1 <= len(lines):
                    next_line = lines[index + 1]
                    if next_line.strip() != "":
                        lines_to_write[index + 1] = whitespace + re.sub(r"^(\s)*([^\s])", r"\2", next_line)

                # find the matching END_DEFER_DEPRECATION and ensure it's got
                # the same indentation
                for matching_end_defer_depraction_index, matching_end_defer_deprecation_line in enumerate(lines[index:]):
                    end_deprecation_match = re.match(r"^(\s*)(END_DEFER_DEPRECATION_UNTIL_IOS_[\d]{2})", matching_end_defer_deprecation_line)
                    if end_deprecation_match:
                        lines_to_write[matching_end_defer_depraction_index + index] = matching_end_defer_deprecation_line.replace(end_deprecation_match.group(1), whitespace)
                        break

            end_defer_match = re.match(r"^(\s*)END_DEFER_DEPRECATION_UNTIL_IOS_[\d]{2}", line)
            if end_defer_match and index + 1 < len(lines):
                whitespace = end_defer_match.group(1)

                # next non-empty line should match the indentation if it's
                # starting with `[`
                for next_line_index, next_line in enumerate(lines[index + 1:]):
                    if next_line.strip() != "":
                        messaging_object_match = re.match(r"^(\s*)\[", next_line)
                        if messaging_object_match:
                            lines_to_write[next_line_index + index + 1] = next_line.replace(messaging_object_match.group(1), whitespace)
                        break

        return "".join(lines_to_write)

if __name__ == "__main__":
    DeferDepracationIndentationFixer().run()
