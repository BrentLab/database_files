#!/usr/bin/env bash

# this was used for a number of files. The for loop removes .txt. the rename functions replaces .fq for the most part. in some cases, needed to change first . to _ in middle of filename

# remove .txt from the filenames
#for f in $1/*;
#do
#   full_path=$(realpath $f)
#   mv "$full_path" "${full_path/.txt}"
#done

# replace extension with .fq
#rename 's/.fq//'  $1/*

# zip
#gzip $1/*

##############################################################################

# for run 314 -- replace first . in file name with _, replace .fq with .fastq and zip

# replace extension with .fq
rename 's/\./_/'  $1/*
rename 's/.fq/.fastq/' $1/*

# zip
gzip $1/*

###############################################################################
