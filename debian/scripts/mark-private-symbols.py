#!/usr/bin/python3

# Script to mark private symbols
# Author: Dmitry Shachnev <mitya57@debian.org>

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
