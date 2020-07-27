# Fastq Filenames

All file names *must* be named in the following format. There should be no exception to this without agreement and updates to the format itself -- the goal is to achieve a standardized fastq filename for all libraries moving forward.

Some care may need to be taken to ensure that the sequence facility follows our naming format.

The format as of 2/28/2019 is: 

LabOwner_ arbitraryLibraryNumber_GTAC_index#_index1_index2_sequencer-stuff.fastq.gz

Example:
BRENT_1_GTAC_1_AAGATTA_GTAACCA_S1_R1_001.fastq.gz 

Within any given run, the index1 sequence must be unique. Please make sure that the indicies are in the correct order (i.e. index1 is unique to the run). To re-emphasize -- there should be no additional information in the filename and order matters.

# Database files

See the [wiki](https://github.com/BrentLab/database_files/wiki) for a detailed explanation of all subdirectories and sheet structure

# verify_metadata_accuracy.py

Before pushing any changes, please run the script verify_metadata_accuracy.py located in the database_files/scripts directory. Assuming that you are in a terminal, located in the database_files directory, do the following:

```
scripts/verify_metadata_accuracy.py -h

# note: to run the script on the database, again assuming you are currently located in the database_files directory, enter:

scripts/verify_metadata_accuracy.py -d .
```
This script only checks the uniqueness of keys within each subdirectory. It checks from fastqFiles --> bioSample. If you don't like the script, please feel free to post a "issue report" with suggestions.

# DatabaseAccuracyObject
This script is currently only available on htcf (it is part of the rnaseq_pipeline module).

note: if you pass key_columns_only=True to fullReport(), a shorter form of the report will be generated with key columns only:

```
ml rnaseq_pipeline
python
>>> from rnaseq_tools.DatabaseAccuracyObject import DatabaseAccuracyObject
>>> db = DatabaseAccuracyObject() # there are options here in the event that you are on an interactive node, etc. Please message me if you need more options
# the first option will report every discrepency in any column
>>> db.fullReport()
# the next only reports discrepencies in key columns and filenames
>>> db.fullReport(key_columns_only=True)

```
The output will go into your /scratch/mblab/$USER/rnaseq_pipeline/reports directory with the name database_accuracy_date_time.txt

# Git workflow

1. Pull the most up-to-date repository. This can be done with the following command: 
```
git pull
```
2. Make edits or create new files.
3. Add the changes made to git.
```
git add <filenames>
```
4. Commit the changed files to git. 
```
git commit -m "<message of what was done>"
```
5. Push the changes to the central repository.
```
git push
```
