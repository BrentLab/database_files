#!/usr/bin/env python

# name: cp_rename_files
# purpose: move old files from old storage system to new
# input:
# output:
# written by: chase mateusiak(chase.mateusiak@gmail.com)
# date included in rnaseq_pipe: 1/23/2020
# See the end of the script for a description of the environment used to write/test

from shutil import copy2 as cp
import pandas as pd
import re
import os
import sys
import argparse
sys.path.append('../../rnaseq_pipe/tools')
from utils import checkCSV
# UPDATE FOR CLUSTER/ALL SYSTEMS

def main(argv, rows_to_skip = -1):
    args = parseArgs(argv)

    src_path = addForwardSlash(args.src_path)
    dest_path = addForwardSlash(args.dest_path)

    summary_df = readInDataFramesCoerceToString(args.summary_sheet)
    crypto_combined_df = readInDataFramesCoerceToString(args.database)
    crypto_combined_df['runNumber'] = crypto_combined_df['runNumber'].apply(addZero)

    # create src_file_path from each row in the sample_summary
    for index, row in summary_df.iterrows():
        if index < rows_to_skip:
            pass
        else:
            # get relevant information from the row
            run_num = row['RUN_NUMBER']
            index_seq = row['INDEX']
            index_seq = removeIndex2(index_seq)
            # in the destination directory, create a directory called "run_####" if one doesn't already exist
            run_num_dest_path = os.path.join(dest_path, 'run_{}'.format(run_num))
            os.system('mkdir -p {}'.format(run_num_dest_path))

            # feed this info into the functions below to generate src and dest filepaths from the current row
            src_file_path = getSourceFilePath(row, args.cols, src_path, args.src_suffix)
            destination_file_path = getDestinationFilePath(run_num_dest_path, index_seq, run_num, args.dest_suffix, crypto_combined_df)
            if destination_file_path:
                moveFiles(src_file_path, destination_file_path, args.log_dest, run_num, index_seq)
            else:
                print('The filepath with index_seq: {} and run_num: {} does not exist'.format(index_seq, run_num))

def parseArgs(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--summary_sheet', required = True,
                        help = 'path to sample_summary')
    parser.add_argument('-db', '--database', required = True,
                        help = 'path to metadata combined database')
    parser.add_argument('-c', '--cols', required = True, nargs='+', default=[],
                        help = 'columns of the sample summary sheet to iterate over. used to create src file path. Usage so far w/ yimings sample_summary: [GENOTYPE, SAMPLE]')
    parser.add_argument('-sp', '--src_path', required = True,
                        help = 'path to source directory')
    parser.add_argument('-ss', '--src_suffix', required = True,
                        help = 'what the src file is called which you intend to move')
    parser.add_argument('-dp', '--dest_path', required = True,
                        help = 'where you wish to deposit the copies')
    parser.add_argument('-ds', '--dest_suffix', required = True,
                        help = 'suffix to append to files in dest directory')
    parser.add_argument('-l', '--log_dest', required = True,
                        help = 'where to deposit log (a tsv with cols run_num, index, original file, new file name')

    return parser.parse_args(argv[1:])


def addZero(value):
    value = str(value)
    runNumsWithZero = ['641','647','648','659','673','674', '684','731','748','759','769','773','779']
    if value in runNumsWithZero:
        entry = '0' + str(value)
        return entry
    else:
        return value

def removeIndex2(identifier):
    # if there is an index2, remove it. however, skip this process for the retrofit indicies
    if identifier.startswith('retrofit'):
        return identifier
    elif '_' in identifier:
        regex = r".*(?=_)"
        return re.search(regex, identifier).group()
    else:
        return identifier

def getDestinationFilePath(dest_path, index_seq, run_num, suffix, df):
    # create a filepath from a common root path, the common suffix and a dataframe from which to pull the information)
    # Args: common root path, common suffix, and a pandas series of items to be searched to create unique filename
    # Returns: a single filename

    name = df[df['runNumber'].str.contains(run_num) & df['index1Sequence'].str.contains(index_seq)]['fastqFileName']
    if name.empty:
        return ''
    else:
        for index in name:
            filename = index
        regex_remove_file_prefix = r"[^/]+$"
        basename = re.search(regex_remove_file_prefix, filename).group()
        basename = getFilenameWithoutExtension(basename)
        if not index_seq in basename:
            basename += '_' + index_seq
        destination = os.path.join(dest_path, basename + '_' + suffix)
        return destination

def getFilenameWithoutExtension(file_path):
    # found on SO at: https://stackoverflow.com/a/56546373
    # Credit: https://www.alanwsmith.com/
    file_basename = os.path.basename(file_path)
    filename_without_extension = file_basename.split('.')[0]
    return filename_without_extension

def getSourceFilePath(row, cols_to_iterate, src_path, src_suffix):
    src_dir = ''
    for col in cols_to_iterate:
        src_dir = src_dir + '{}-'.format(row[col])
    src_file_path = src_path + src_dir[0:-1] + '/' + src_suffix
    return src_file_path

def moveFiles(src_file_path, desination_file_path, log_dest, run_num, index_seq):
    if os.path.isfile(src_file_path):
        cp(src_file_path, desination_file_path)
        log_dest = addForwardSlash(log_dest)
        log_file = os.path.join(log_dest, 'copy_log.tsv')
        with open(log_file, 'a+') as cp_log:
            cp_log.write('{}\t{}\t{}\t{}\n'.format(run_num, index_seq, src_file_path, desination_file_path))

def readInDataFramesCoerceToString(df_path):
    # read in dataframes and coerce specified columns to string (use verify_metadata)
    if checkCSV(df_path):
        return_df = pd.read_csv(df_path).astype(str)
    else:
        return_df = pd.read_excel(df_path).astype(str)
    return return_df

def addForwardSlash(path):
    if not path[-1] == '/':
        path = path + '/'
    return path

if __name__ == '__main__':
	main(sys.argv)