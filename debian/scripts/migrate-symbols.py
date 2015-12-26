#!/usr/bin/python3

# Script to migrate symbols from old symbols versioning to new symbols versioning
# Author: Dmitry Shachnev <mitya57@debian.org>

import glob
import re
import subprocess
import sys

options_re = re.compile(r'\([^)]+\)')
symbol_re = re.compile(r'([^@]+)@([0-6ABEIPQRTVaest_.]+) (\S+)')
cxx_symbol_re = re.compile(r'"([^@]+)@(Base)" (\S+)')


def apply_substs(symbol):
    # this is the version for amd64
    # see SymbolsHelper/Substs/TypeSubst.pm for details
    symbol = symbol.replace('{size_t}', 'm')
    symbol = symbol.replace('{ssize_t}', 'l')
    symbol = symbol.replace('{int64_t}', 'l')
    symbol = symbol.replace('{uint64_t}', 'm')
    symbol = symbol.replace('{qptrdiff}', 'x')
    symbol = symbol.replace('{quintptr}', 'y')
    symbol = symbol.replace('{intptr_t}', 'l')
    return symbol


def main(buildlog_path):
    new_symbols = {}
    with open(buildlog_path) as buildlog:
        for line in buildlog:
            if not line.startswith('+ '):
                continue
            match = symbol_re.match(line[2:])
            if match:
                symbol, version = match.group(1, 2)
                if symbol.startswith('_ZThn'):
                    symbol = subprocess.check_output(('c++filt', symbol))
                    symbol = symbol.decode('ascii').rstrip()
                new_symbols[symbol] = version

    for symbols_file_path in glob.glob('debian/*.symbols'):
        new_lines = []
        with open(symbols_file_path) as symbols_file:
            for line in symbols_file:
                line = line.rstrip()
                was_private = line.endswith(' 1')
                if was_private:
                    line = line[:-2]
                if not line.startswith(' '):
                    new_lines.append(line)
                    continue
                match = options_re.search(line)
                options = match.group(0) if match else ''
                symbol_part = line[1:]
                if symbol_part.startswith('('):
                    symbol_part = options_re.sub('', symbol_part, count=1)
                if 'c++' in options:
                    match = cxx_symbol_re.match(symbol_part)
                else:
                    match = symbol_re.match(symbol_part)
                symbol = match.group(1)
                symbol_subst = apply_substs(symbol)
                abi = new_symbols.get(symbol_subst, match.group(2))
                if not was_private and 'optional' not in options and symbol_subst not in new_symbols:
                    print('Missing symbol in %s: %s' % (symbols_file_path, symbol_subst), file=sys.stderr)
                format_string = ' %s"%s@%s" %s' if 'c++' in options else ' %s%s@%s %s'
                if 'PRIVATE' in abi:
                    format_string += ' 1'
                new_lines.append(format_string % (options, symbol, abi, match.group(3)))
        with open(symbols_file_path, 'w') as symbols_file:
            for line in new_lines:
                print(line, file=symbols_file)

if __name__ == '__main__':
    main(sys.argv[1])
