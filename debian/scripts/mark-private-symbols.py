#!/usr/bin/python3

# Script to mark private symbols
# Author: Dmitry Shachnev <mitya57@debian.org>

# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

from difflib import unified_diff
import glob
import sys


def main(argv):
    for symbols_file_path in glob.glob('debian/*.symbols'):
        old_lines = []
        new_lines = []
        with open(symbols_file_path) as symbols_file:
            for line in symbols_file:
                old_lines.append(line)
                line = line.rstrip()
                if line.endswith(' 1'):
                    line = line[:-2]
                if '@Qt_5_PRIVATE_API' in line:
                    line += ' 1'
                new_lines.append(line + '\n')
        if '--write-results' in argv:
            with open(symbols_file_path, 'w') as symbols_file:
                for line in new_lines:
                    symbols_file.write(line)
        else:
            for line in unified_diff(old_lines, new_lines,
                                     fromfile=symbols_file_path,
                                     tofile=symbols_file_path):
                sys.stdout.write(line)


if __name__ == '__main__':
    main(sys.argv)
