#!/usr/bin/env bash

# remove .txt from the filenames
for f in $1/*;
do
   full_path=$(realpath $f)
   mv "$full_path" "${full_path/.txt}"
done

# replace extension with .fq
rename 's/.fq/.fastq/'  $1/*

# zip
gzip $1/*
