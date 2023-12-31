#!/usr/bin/python

'''assumes sgf file has each problem in a different fork
all labeled with handicap notation (AW and AB)
'''

import argparse
import process
import boardlib
import re

def tex_title(title):
    s = """\
\\begin{titlepage}
    \\null
    \\vfill
    \\begin{center}
        \\textbf{%s}\\\\
    \\end{center}
    \\vfill
\\end{titlepage}
\\newpage
""" % (title)
    return s

def parse(row):
    pattern = "\(;AW((\[[^\]]*\])*)AB((\[[^\]]*\])*)C\[([^\]]*)\]\)"
    m = re.match(pattern, row)
    ws = m.groups()[0].lstrip('[').rstrip(']').split('][')
    bs = m.groups()[2].lstrip('[').rstrip(']').split('][')
    comment = m.groups()[4].split('--')[0].strip()
    return ws, bs, comment

def write_row(row, f, i):
    whandi, bhandi, comment = parse(row)
    wtex = [process.convert(s) for s in whandi]
    btex = [process.convert(s) for s in bhandi]

    header = '\\begin{subsection}{Problem %d}\n' % (i)
    footer = '\\end{subsection}\n'

    # This dictionary is useful for quickly turning a letter into a color
    tmp_D = {"B": "black", "W": "white"}

    headered = False

    if not headered:
        f.write(header)
        headered = True

    f.write('\\begin{center}\n')
    f.write('\\cleargoban\n')

    if wtex:
        f.write('\\white{')
        f.write(','.join(wtex))
        f.write('}\n')

    if btex:
        f.write('\\black{')
        f.write(','.join(btex))
        f.write('}\n')

    f.write('\\showfullgoban\n')

    f.write('\\\\')

    # Comments
    #f.write('\parbox{4.5in}{\n')

    f.write('\\begin{lstlisting}\n')
    f.write(comment)
    f.write('\\end{lstlisting}\n')

    #f.write('}\n')

    f.write('\\end{center}\n')

    if headered:
        f.write(footer)

def make(infile, outfile, title):
    with open(infile) as f:
        raw = f.read()
        rows = []
        for line in raw.split('\n'):
            if line.startswith("(;A"):
                rows.append(line)
        keys = process.get_keys(raw)

    with open(outfile,'w') as f:
        # optional:
        f.write('\\documentclass[twocolumn]{article}\n')
        #f.write('\\documentclass{article}\n')

        # removes section numbering
        f.write('\\setcounter{secnumdepth}{0}\n')
        f.write('\\setlength\\parskip{\\baselineskip}\n')
        f.write('\\usepackage{igo}\n')
        f.write('\\usepackage{listings}\n')
        f.write('\\lstset{\n')
        f.write('    basicstyle=\\small\\ttfamily,\n')
        f.write('    columns=flexible,\n')
        f.write('    breaklines=true\n')
        f.write('}\n')
        f.write('\\begin{document}\n')
    
        f.write(tex_title(title))
        i = 1
        for row in rows:
            write_row(row, f, i)
            i += 1

        f.write('\\end{document}\n')

   
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--infile', '-i', required=True)
    ap.add_argument('--title', '-t', required=True)
    ap.add_argument('out')

    args = ap.parse_args()
    
    make(args.infile, args.out, args.title)
