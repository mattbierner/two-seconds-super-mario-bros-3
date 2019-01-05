"""
Convert a directory of frame files into html that can be printed or converted to a pdf
"""
import argparse
import os
import re
import sys
from collections import Counter

style = """
    body {
        margin: 0 auto;
        max-width: 1200px;
        font-family: 'IBM Plex Mono', monospace;
        font-size: 16px;
    }

    section {
        page-break-after: always;
    }

    .code {
            column-count: 4;
            font-size: 6px;
            white-space: pre;
    }

    header {
        padding-top: 2em;
        text-align: center;
        padding-bottom: 2em;
    }

    h1 {
        font-size: 100px;
        margin-top: 0;
        margin-bottom: 0rem;
    }

    h1 {
        display: inline-block;
        position: relative;
    }

    h1:before {
        content: "frame";
        position: absolute;
        left: 0;
        top: 50%;
        transform: translateX(-110%);
        margin-right: 1em;
        font-size: 30px;
    }

    .operation-list {
        list-style: none;
        column-count: 4;
        font-size: 10px;
        white-space: pre;
        padding-left: 0;
    }

    .operation-list li {
        padding-left: 0;
    }

    @page {
        size: auto;
        margin-left: 0.75in;
        margin-right: 0.5in
    }
"""

def create_html(in_dir, out_file, start, end, images_path):
    """
    Build the html from the input directory of frames

    Pretty damn ugly code :)
    """
    content = """<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <title>Document</title>
            <style>
                {style}
            </style>
        </head>
        <body>
    """.format(style=style)

    i = 1
    for p in range(start, end):
        with open(os.path.join(in_dir, '{0}.log'.format(p)), 'r') as log:
            operationCounts = {}
            lineCount = 0
            for line in log:
                lineCount += 1
                match = re.match(r'^\$\S+\s+(\S+)\s', line)
                instr = match.group(1)
                if instr not in operationCounts:
                    operationCounts[instr] = 0
                operationCounts[instr] += 1
            
            table = '<ul class="operation-list">'
            for instr, count in Counter(operationCounts).most_common():
                table += '<li>{0} — {1}</li>'.format(instr.rjust(6), str(count).ljust(6))
            table += '</ul>'

            content += """
                <section>
                    <header style="display: flex; align-items: center;">
                        <div style="flex: 1;">
                            <h1>{index}</h1>
                            <h3>{lineCount} operations</h3>
                            {table}
                        </div>
                        <div style="flex: 1;">
                            <img src="{image}" />
                        </div>
                    </header>
            """.format(index=i, image='./{0}/{1}.png'.format(images_path, p), table=table, lineCount=lineCount)

            log.seek(0)
            content += '<div class="code">{0}</div>'.format(log.read())
        content += '</section>'
        i = i + 1

    content += '</body></html>'
    return content

def main(in_dir, out_file, start, end, images_path):
    html = create_html(in_dir, out_file, start, end, images_path)
    with open(out_file, 'w') as out:
        out.write(html)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Convert a directory of frame files into html that can be printed or converted to a pdf.")
    parser.add_argument('--trace-files', dest='in_dir', required=True, help="Path to directory containing files with frame data. Frames files are expected to be name `x.log` where `x` is the frame number")
    parser.add_argument('--out', dest='out_file', required=True, help="Path to output html file")
    parser.add_argument('--start', type=int, dest='start', required=True, help="Starting frame number")
    parser.add_argument('--end', type=int, dest='end', required=True, help="Ending frame number")
    parser.add_argument('--images-path', dest='images_path', required=True, help="Path to directory where screenshots are stored. Screenshots should be named `x.png` where `x` is the frame number")

    args = parser.parse_args()

    main(os.path.abspath(args.in_dir), os.path.abspath(args.out_file), args.start, args.end, args.images_path)
