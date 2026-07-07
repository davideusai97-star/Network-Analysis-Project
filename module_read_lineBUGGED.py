import csv
import pandas as pd

'''
Read data of a line from a csv file. The line is identified by its unique id.
'''

filename='./full_datasets/full_posts.csv'
id='6fe6491e-5e9c-4371-961d-f90c4d357d0f'

with open(filename, 'r', newline='') as inp:
    reader = csv.reader(inp)
    rows = [row for row in reader if (row[0] == id)] # Select line by id

print(rows)


'''
ISSUE:


 File "C:\Users\david\miniconda3\lib\encodings\cp1252.py", line 23, in decode
    return codecs.charmap_decode(input,self.errors,decoding_table)[0]
UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 8116: character maps to <undefined>
'''