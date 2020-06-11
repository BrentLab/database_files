#!/usr/bin/env python

"""
    From a text file created from the email from the sequencer (copy and paste the fastqfilenames exactly as in the email)
    create a .xlsx with the fastqfilenames listed as a column
    output will be path/to/output_directory/fastqfiles_as_column.xlsx
    usage: extract_fastq_filename_as_column.py -t path/to/text/file/with/list/of/fastqfilenames.txt -o path/to/output_directory
"""

import sys
import argparse
import os
import re
import pandas as pd

def main(argv):
    # parse cmd line arguments
    print('...parsing cmd line input')
    args = parseArgs(argv)
    # test paths
    try:
        if not os.path.isfile(args.txt_file):
            raise FileNotFoundError('TextFilePathNotValid')
    except FileNotFoundError:
        print('The path to the text file is not valid. Check it and try again')
    try:
        if not os.path.isdir(args.output_dir):
            raise NotADirectoryError('OutputDirPathNotVaid')
    except NotADirectoryError:
        print('Output directory does not exist. Either check the path, or create the directory, and try again')

    # open file, clean lines down to fastqfilename
    with open(args.txt_file) as input_file:
        lines = input_file.readlines()
        lines = list(map(lambda x: re.sub(r":\d+\n", '', x), lines))
        lines = list(map(lambda x: re.sub(r"Brent/", '', x), lines))

    # convert to dataframe
    df = pd.DataFrame(lines, columns=['fastqFileName'])
    # write out
    output_path = os.path.join(args.output_dir, 'fastq_column_from_email.xlsx')
    df.to_excel(output_path)

def parseArgs(argv):
    parser = argparse.ArgumentParser(description="convert a text file copied/pasted from sequencer folks to a dataframe column for fastqFile sheets")
    parser.add_argument("-t", "--txt_file", required=True,
                        help="[REQUIRED] ")
    parser.add_argument("-o", "--output_dir", required=True,
                        help="[REQUIRED] directory in which to output results. This WILL overwrite any previous output of this script,\n"
                             "if there is any in the output directory")
    args = parser.parse_args(argv[1:])
    return args


if __name__ == "__main__":
    main(sys.argv)
