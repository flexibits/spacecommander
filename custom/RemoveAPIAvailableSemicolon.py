# RemoveVoidBlockDeclaration.py
# Converts "^(void) {" to "^{" since the (void) is unnecessary
#
# If a filename is specified as a parameter, it will change that file in place.
# If input is provided through stdin, it will send the result to stdout.

from AbstractCustomFormatter import AbstractCustomFormatter

class RemoveAPIAvailableSemicolon(AbstractCustomFormatter):
    def format_lines(self, lines):

        lines_to_write = []
        for line in lines:
            to_append = line
            stripped_line = line.strip()

            if stripped_line.startswith("API_AVAILABLE(") and stripped_line.endswith(");"): 
                to_append = line.replace(";", "")

            lines_to_write.append(to_append)

        return "".join(lines_to_write)

if __name__ == "__main__":
    RemoveAPIAvailableSemicolon().run()
