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
