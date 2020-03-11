#!/usr/bin/env python
"""
    This is how I removed .txt and replaced .fq with .fastq.gz in all fastqFile sheets' fastqFileName column.
    chase.mateusiak@gmail.com

"""

import pandas as pd

fastq_sheet_path = ['/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1755.xlsx']

#fastq_sheet_path = ['/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0647.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0648.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0659.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0673.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0674.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0684.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0731.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0748.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0759.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0769.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0773.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0779.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_869.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_894.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1028.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1045.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1272.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1337.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1344.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1476.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_1573.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0629_0618.xlsx',
#                    '/home/chase/code/brentlab/database-files/old_database/crypto/fastqFiles/fastq_0711_5_0718_7.xlsx',]

for df_path in fastq_sheet_path:
    df = pd.read_excel(df_path)
    for i, r in df.iterrows():
        df.loc[i, 'fastqFileName'] = r['fastqFileName'].replace('.txt', '').replace('.fq', '.fastq.gz')
    df.to_excel(df_path, index = False)
