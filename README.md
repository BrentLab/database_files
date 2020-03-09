# Fastq Filenames

All file names *must* be named in the following format. There should be no exception to this without agreement and updates to the format itself -- the goal is to achieve a standardized fastq filename for all libraries moving forward.

Some care may need to be taken to ensure that the sequence facility follows our naming format.

The format as of 2/28/2019 is: 

LabOwner_ arbitraryLibraryNumber_GTAC_index#_index1_index2_<sequencer stuff>.fastq.gz

Example:
BRENT_1_GTAC_1_AAGATTA_GTAACCA_S1_R1_001.fastq.gz 

Within any given run, the index1 sequence must be unique. Please make sure that the indicies are in the correct order (i.e. index1 is unique to the run). To re-emphasize -- there should be no additional information in the filename and order matters.

# Database files

See the [wiki](https://github.com/BrentLab/database_files/wiki) for a detailed explanation of all subdirectories and sheet structure

This is a repository for all of the database files from Brent Lab.

You can find the specifications of the database files in specification.docx in the repository.

All dates should be in format: mm.dd.yy, all numeric. E.g 07.29.19  
All names should be FIRSTINITIAL.LASTNAME, all caps. E.g. “M.BRENT”  
Each table should be in a separate .csv file, named according to the following scheme:

* bioSample_M.BRENT_07.29.19
* rnaSample_M.BRENT_07.30.19
* s1cDNASample_M.BRENT_07.31.19
* s1s2Pooling_M.BRENT_07.31.19
* s2cDNASample_M.BRENT_08.01.19
* library_M.BRENT_08.02.19
* fastqFiles_08.04.19 (may contain files for libraries prepared by multiple people)


You can find the specifications(the column headers as well as entries of the files) of the database files in specification.docx in the repository.

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
