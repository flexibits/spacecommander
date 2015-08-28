# RemoveVoidBlockDeclaration.py
# Converts "^(void) {" to "^{" since the (void) is unnecessary
#
# If a filename is specified as a parameter, it will change that file in place.
# If input is provided through stdin, it will send the result to stdout.

from AbstractCustomFormatter import AbstractCustomFormatter

class RemoveVoidBlockDeclaration(AbstractCustomFormatter):
    def format_lines(self, lines):

        lines_to_write = []
        for line in lines:
            to_append = line

            if line.strip().endswith("^(void) {"): 
                to_append = line.replace("^(void) {", "^{")

            lines_to_write.append(to_append)

        return "".join(lines_to_write)

if __name__ == "__main__":
    RemoveVoidBlockDeclaration().run()
