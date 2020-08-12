#!/usr/bin/env python

# name: verify_metadata_accuracy
# purpose: check metadata tables for expected entries
# input: an individual sheet, a directory of sheets, or the top most directory
# output: Warnings and prompts to the user to either ignore or change entries
# written by: chase mateusiak(chase.mateusiak@gmail.com)
# date included in rnaseq_pipe: 1/21/2020
# See the end of the script for a description of the environment used to write/test

import pandas as pd
import sys
import argparse
import re
import os
from glob import glob
#from queryDB import *

# Each subdirectory (all sheets in a given category concatenated) should be unique on the following columns
unique_key_by_subdirectory = {"fastqFiles": ['libraryDate', 'libraryPreparer', 'librarySampleNumber', 'fastqFileName'],
                              "library":['libraryDate', 'libraryPreparer', 'librarySampleNumber','s2cDNADate', 's2cDNAPreparer', 's2cDNASampleNumber'],
                              "s2cDNASample": ['s2cDNADate', 's2cDNAPreparer', 's2cDNASampleNumber','s1cDNADate', 's1cDNAPreparer', 's1cDNASampleNumber'],
                              "s1cDNASample": ['s1cDNADate', 's1cDNAPreparer', 's1cDNASampleNumber', 'rnaDate', 'rnaPreparer', 'rnaSampleNumber'],
                              "rnaSample": ['rnaDate', 'rnaPreparer', 'rnaSampleNumber','harvestDate', 'harvester', 'bioSampleNumber'],
                              "bioSample": ['harvestDate', 'harvester', 'bioSampleNumber']}

# Each sheet should be unique on the following columns
unique_key_by_sheet = {"fastqFiles": ['libraryDate', 'libraryPreparer', 'librarySampleNumber'],
                       "library": ['libraryDate', 'libraryPreparer', 'librarySampleNumber'],
                       "s2cDNASample": ['s2cDNADate', 's2cDNAPreparer', 's2cDNASampleNumber'],
                       "s1cDNASample": ['s1cDNADate', 's1cDNAPreparer', 's1cDNASampleNumber'],
                       "rnaSample": ['rnaDate', 'rnaPreparer', 'rnaSampleNumber'],
                       "bioSample": ['harvestDate', 'harvester', 'bioSampleNumber']}

#metadata_subdirectories = ['fastqFiles', 'library', 's2cDNASample', 's1cDNASample', 'rnaSample', 'bioSample']
metadata_subdirectories = ['bioSample', 'rnaSample', 's1cDNASample', 's2cDNASample', 'library', 'fastqFiles']



# print full database
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

def main(argv):
    
    args = parseArgs(argv)
    print("...parsing cmd line arguments")
    try:
        # check that args.database is a valid path
        if not os.path.isdir(args.database):
            raise NotADirectoryError('%s does not point to a valid directory' %args.database)
    except NotADirectoryError:
        print('%s not a valid path' %args.database)

    try:
        # check that the subdirectory exists in args.database
        if not os.path.isdir(os.path.join(args.database, args.database_surdir)):
            raise NotADirectoryError('%s/%s not a valid path' %(args.database, args.database_subdir))
    except NotADirectoryError:
        print('%s/%s not a valid path -- check that the subdiretory is spelled correctly and exists' %(args.database, args.database_subdir))
    # if the database_subdir flag is not used in the cmd line, then just ignore this error and move on
    except AttributeError:
        pass

    print("...creating dictionary of database or subdirectory")
    if args.database_subdir:
        # datadir_dict has structure {subdirectory: [list, of, paths, ...]
        metadata_directory_dict = getFilePaths(args.database, args.database_subdir)
    else:
        metadata_directory_dict = getFilePaths(args.database)

    # instatiate a dictionary
    metadata_concat_dict = {}
    print('...checking that the key of each sheet is unique (eg, that harvestDate, harvester, bioSampleNumber is unique in a given bioSample sheet')
    for subdirectory in metadata_directory_dict:
        metadata_concat_dict[subdirectory] = concatMetadata(subdirectory, metadata_directory_dict[subdirectory])
        cols = '\t'.join(metadata_concat_dict[subdirectory].columns)
        cols = cols.lower()
        # look for unnamed columns, raise error if there is one
        try:
            if "unnamed" in cols:
                raise ValueError('UnnamedColumn')
        except ValueError:
            print("\nThere is an unnamed column in one of the sheets in subdirectory {}. This must be found and fixed before proceeding.".format(subdirectory))

    print('...checking that the keys in each subdirectory are unique after concatenating (eg rnaSample would be harvester, harvestDate, bioSampleNumber, rnaDate, rnaPreparer, rnaSampleNumber')
    for subdirectory in metadata_concat_dict:
        uniqueKeys(unique_key_by_subdirectory[subdirectory], metadata_concat_dict[subdirectory])

    print('\n::verify_metadata_complete::\nPlease fix any issues found before pushing to remote')

def parseArgs(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--database', required=True,
                        help='Suggested usage: database-files path to metadata base')
    parser.add_argument('-k', '--database_subdir', required=False,
                        help='if you do not wish to verify all metadata subdirectories, you may list the ones you would like to check. Default is to check all metadata subdirs in database')

    return parser.parse_args(argv[1:])

def getFilePaths(metadata_path, metadata_subdirectories = metadata_subdirectories):
    # create dictionary of filepaths to the various types of metadata sheets
    # Args: base_path to data directory, datadir_keys are the subdirectories in the datadir
    # Returns: dictionary {metadata-database/subdir: [filepaths]} i.e. {bioSample: [filepaths], experimentDesign:[filepaths]}

    datadir_dict = {}

    # associate each key (relevant subdirs of datadir) with a list of of files (complete path) in each key directory
    for metadata_subdirectory in metadata_subdirectories:
        dir_path = os.path.join(metadata_path, metadata_subdirectory)
        subdir_files = glob(os.path.join(dir_path, '*'))
        for file in subdir_files:
            basename = os.path.basename(file)
            if basename.startswith('~') or basename.startswith('._') or basename.startswith('.~') or basename.startswith('~$'):
                subdir_files.remove(file)

        # test whether any of the key subdirectories of datadir are empty, throw error if so
        try:
            if len(subdir_files) == 0:
                raise FileNotFoundError('NoFilesFoundInSubdirectory' %metadata_subdirectory)
        except FileNotFoundError:
            print("No files found in %s. These files are necessary to creating the sample_summary." % os.path.join(metadata_path, metadata_subdirectory))
        else:
            datadir_dict.setdefault(metadata_subdirectory, []).extend(subdir_files)

    return datadir_dict

def concatMetadata(subdirectory_name, subdirectory_file_list):
    # creates concatenated dataframe from all files in a given list of paths (files of a certain subdirectory of user inputted data directory
    # Args: a dictionary {subdirectory: [list, of, sheet, paths]} eg {bioSample: [path/to/sheet1, path/to/sheet2, ...]}
    # Returns: all of the sheets concatenated vertically

    metadata_sheet_key = unique_key_by_sheet[subdirectory_name]

    # create concatenated_df initially with the first sheet in the list
    try:
        print(subdirectory_file_list[0])
        concatenated_df = readInDataframe(subdirectory_file_list[0])
        uniqueKeys(metadata_sheet_key, concatenated_df)
    except FileNotFoundError:
        print("%s not a valid path to a metadata sheet" %subdirectory_file_list[0])

    # for each subsequent sheet, concatenate (row_bind) to concatenated_df
    for sheet_path in subdirectory_file_list[1:]:
        # read in query sheet
        try:
            print(sheet_path)
            next_df = readInDataframe(sheet_path)
            uniqueKeys(metadata_sheet_key, next_df)
        except FileNotFoundError:
            print('%s not a valid path to a metadata sheet' %next_df)
        else:
            concatenated_df = concatenated_df.append(next_df)

    return concatenated_df

def createDB(datadir_dict, subdirectory_list = metadata_subdirectories, drop_fastq_na = True, coerce_cols = False):
    # create joined data frame from data directory
    # Args: datadir_dict is a dictionary of subdirectories (keys) and lists of files in the subdirs (values);
    #       datadir_keys are the subdirectories to search through; drop_fastq_na = True means that rows that are entirely
    #       na will be dropped (dropping any fastq
    # Returns: a complete database of information from data directory, minus entries that do not have fastq paths entered

    concat_dict = {}

    # return dictionary of structure {datadir/subdir: concatenated_table_of_all_files_in_datadir/subdir}
    for key in datadir_dict:
        concat_dict[key] = concatMetadata(datadir_dict[key])

    # drop rows with na in column fastqFileName of table fastqFiles
    if drop_fastq_na:
        concat_dict['fastqFiles'].dropna(subset=['fastqFileName'], inplace=True)

    # get keys to merge dataframes on -- note order is important
    key_cols = getKeys(subdirectory_list, concat_dict)

    # merge the first two sets of data, the concatenated fastqFiles and Library sheets
    merged_df = pd.merge(concat_dict[subdirectory_list[0]], concat_dict[subdirectory_list[1]], how='left', on=list(key_cols[0]))
    # merge the subsequent sheets on the columns identified in key_cols
    for i in range(1,len(subdirectory_list)-1):
        merged_df = pd.merge(merged_df, concat_dict[subdirectory_list[i+1]], how='left', on=list(key_cols[i]))

    if coerce_cols:
        merged_df = coerceAllCols(merged_df)
    return merged_df

def queryDB(df, query):
    # filters combined_df on user-inputted columns/values
    # Args: query (user input json at cmd line)
    # Return: a filtered df
    #TODO: make query case insensitive

    # read in json
    query = pd.read_json(query, typ='series')

    # begin a string to store the query formula
    fltr_str='('
    # loop through columns in json query (i.e. 'timePoint' and 'treatment')S
    for key, value in query.items():
        fltr_str = fltr_str + '{} == {}'.format(key, value) + ' & '
    # once out of both loops, split the string on the final &, retain the substring before the split, and eliminate whitespace
    fltr_str = fltr_str.rsplit('&',1)[0].strip() + ')'
    # use the fltr_str formula to filter the dataframe
    df = df.query(fltr_str)
    return df

def checkCSV(file_path):
    """
        test whether a given file is a .csv or something else
        :param file_path: a file that ends with .csv, .xlsx, .tsv, etc.
        :returns: True if .csv, false otherwise
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError('PathToColumnarDataDNE')
    else:
        # test whether a given file is a .csv or .xlsx
        if re.search('\.csv', file_path):
            return True
        else:
            return False


def checkTSV(file_path):
    """
        test whether a given file is a .tsv
        :param file_path: a file path
        :returns: True if .tsv, false otherwise
        :raises: FileNotFoundError
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError('PathToColumnarDataDNE')
    else:
        if re.search('\.tsv', file_path):
            return True
        else:
            return False


def checkExcel(file_path):
    """
        test whether a given file is a .xlsx
        :param file_path: a file path
        :returns: True if .tsv, false otherwise
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError('PathToColumnarDataDNE')
    else:
        # test whether a given file is a .xlsx
        if re.search('\.xlsx', file_path):
            return True
        else:
            return False


def readInDataframe(path_to_csv_tsv_or_excel):
    """
        read in .csv, .tsv or .xlsx
        :param path_to_csv_tsv_or_excel: path to a .csv, .tsv .xlsx
        :returns: a pandas dataframe
    """
    if not (path_to_csv_tsv_or_excel.endswith('csv') or
            path_to_csv_tsv_or_excel.endswith('tsv') or
            path_to_csv_tsv_or_excel.endswith('xlsx')):
        raise ValueError('UnrecognizedFileExtension')
    try:
        if checkCSV(path_to_csv_tsv_or_excel):
            return pd.read_csv(path_to_csv_tsv_or_excel)
        elif checkTSV(path_to_csv_tsv_or_excel):
            return pd.read_csv(path_to_csv_tsv_or_excel, sep='\t')
        elif checkExcel(path_to_csv_tsv_or_excel):
            return pd.read_excel(path_to_csv_tsv_or_excel)
    except FileNotFoundError:
        raise FileNotFoundError('PathToColumnarDataDNE')


def getKeys(datadir_keys, concat_dict):
    # create list of shared columns between successive pairs of keys in datadir_keys i.e. the columns which are shared between the sheets in fastqFiles and Library
    # Args: a list of subdirectories in datadir and a dictionary of concatenated sheets from within each one of those directories
    # PLEASE NOTE: DICTIONARIES ARE ORDERED IN PYTHON 3.6+. KEY/DIRECTORIES NEED TO BE ADDED TO CONCAT DICT IN ORDER YOU WISH TO MERGE
    # Returns: a list of key columns
    key_cols = []
    num_keys = len(datadir_keys)
    for i in range(num_keys-1):
        key_cols.append(concat_dict[datadir_keys[i]].keys().intersection(concat_dict[datadir_keys[i+1]].keys()))
    return key_cols

def uniqueKeys(key, df):
    # test whether the key columns in a given sheet are unique
    # Args: the keys (passed as list) and the path to the dataframe
    # Return: none
    # to std_out: info on uniqueness of key
    if not isinstance(df, pd.DataFrame) and os.path.isfile(df):
        if checkCSV(df):
            sheet = pd.read_csv(df)
        else:
            sheet = pd.read_excel(df)
    else:
        sheet = df
    # make a tuple of the key columns and store them as pandas series
    key_tuples = sheet[key].apply(tuple, axis=1)
    num_keys = key_tuples.size
    num_unique_keys = key_tuples.unique().size
    print(key)
    print("\nThe number of unique keys is {}. The number of rows is {}. If these are equal, the keys are unique.".format(num_keys, num_unique_keys))
    if not num_keys == num_unique_keys:
        print("\nThe following indicies are not unique:\n\t{}".format(sheet[sheet[key].duplicated()]))
        print("\nDo you want to continue? Enter y or n: ")
        user_response = input()
        if user_response == 'n':
            quit()

def coerceAllCols(sheet):
    # converts columns specific in functions below to floats and datetime
    sheet = floatColCoerce(sheet)

    sheet = datetimeColCoerce(sheet)

    # forcing all to lowercase is not working in the search
    #sheet = strColCoerce(sheet)

    return sheet

def colCoerce(cols, sheet, dtype):
    # general function to coerce column to certain data type
    # Args: a list of columns to coerce (can be a subset of columns of a data frame. must be a list), a dataframe,
    #       and a datatype (see pandas .astype documentation for which datatypes are possible. didn't work for datetime, for example)
    # Return: the dataframe with the specified columns coerced
    coerce_cols = cols

    for col in sheet.columns[sheet.columns.isin(coerce_cols)]:
        sheet[col] = sheet[col].astype(dtype)
    return sheet

def floatColCoerce(sheet):
    # coerce columns specified below to int
    int_columns = ['librarySampleNumber', 'runNumber', 'tapestationConc', 'readsObtained', 'rnaSampleNumber',
                   'inductionDelay', 'replicate', 'timePoint']

    sheet = colCoerce(int_columns, sheet, 'float')

    return sheet

def datetimeColCoerce(sheet):
    # coerce columns specified below to datetime
    datetime_columns = ['libraryDate', 's2cDNADate', 's1cDNADate', 'rnaDate', 'harvestDate']

    for col in datetime_columns:
        sheet[col] = pd.to_datetime(sheet[col])

    return sheet

def strColCoerce(sheet):
    # coerce any column NOT in int_col or datetime_col to a string and make it lower case

    int_columns = ['librarySampleNumber', 'tapestationConc', 'readsObtained', 'rnaSampleNumber','inductionDelay', 'replicate', 'timePoint']
    datetime_columns = ['libraryDate', 's2cDNADate', 's1cDNADate', 'rnaDate', 'harvestDate']

    typed_cols = int_columns + datetime_columns

    for col in sheet.columns:
        if col not in typed_cols:
            sheet[col] = sheet[col].astype(str).apply(lambda x: x.lower())

    return sheet

if __name__ == '__main__':
	main(sys.argv)
