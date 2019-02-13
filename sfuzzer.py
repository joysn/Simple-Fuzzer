import sys
import logging
import os
import random
import argparse

''' Parsing the arguments 
(base) D:\>python datagen.py --help
usage: datagen.py [-h] [--o O] [--c C] [--r R] [--cs CS [CS ...]] [--d D]

A Simple Data Generator
***********************
row delimiter = Space
column delimiter = New line

optional arguments:
  -h, --help            show this help message and exit
  --o O                 Name of Output Data File
  --c C                 No of columns
  --r R                 No of rows
  --cs CS [CS ...], --list CS [CS ...]
                        Space separated list of colum sizes
  --d D                 Debug Level: INFO, DEBUG, WARNING

Contact:- joysn1980@yahoo.com
'''
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='''
A Simple File Fuzzer 
********************''',epilog='''
Contact:- joysn1980@yahoo.com
''')
parser.add_argument('InputFileName', help='Input File Name to be fuzzed')
parser.add_argument('--o', help='Name of Output Fuzzed File')
parser.add_argument('--p', help='Percentage of Bytes to be fuzzed ',type=int,default=50, choices=range(0, 50)
parser.add_argument('--d', help='Debug Level: INFO, DEBUG, WARNING')
parser.add_argument('--s', help='Seed Value : Any random integer', type= int, default= 0)

args = vars(parser.parse_args())

if args["o"] == None:
	args["o"] = args["InputFileName"]+".fz"


''' Debuging '''
if args["d"] == 'DEBUG':
	logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', datefmt = '%m/%d/%y %I:%M%S %p')
if args["d"] == 'INFO':
	logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s', datefmt = '%m/%d/%y %I:%M%S %p')


''' Modify each byte '''
def modify_byte(byte):
	return int.from_bytes(byte,byteorder='little') >> random.randint(1,10)
	
''' Covert integer to byte'''
def int_to_bytes(x):
	return x.to_bytes((x.bit_length() + 7) // 8, byteorder='little')
	

''' Check the arguments '''
logging.debug(args)
logging.debug(args["InputFileName"])
logging.debug(args["o"])
logging.debug(args["p"])
logging.debug(args["d"])
logging.debug(args["s"])

''' Randomize based on seed '''
random.seed(args["s"])

''' Get the file name '''
ifile = args["InputFileName"]
ofile = args["o"]

''' How much do we fuzz? '''
percent_modify = args["p"]

''' Input Details '''
print("**********************************")
print('Input file Name: ',ifile)
logging.info("Percent to modify:" + str(percent_modify/100))

file_size = os.path.getsize(ifile)
print('file size:',file_size)
bytes_to_modify = percent_modify * file_size // 100
print('Bytes to modify :',bytes_to_modify)

''' Bytes we need to modify '''
places_to_modify = random.sample(range(0, file_size), bytes_to_modify)
logging.debug("Places to modify: %s", places_to_modify)
print("**********************************")

if os.path.exists(ofile):
	os.remove(ofile)

# replace the contents
with open(ifile, 'r+b') as inf, open(ofile, 'a+b') as ouf:
	for i in range(0, file_size):
		input_b = inf.read(1)
		logging.debug("Input[%s]: %s",i, input_b)
		
		# Randomly choose if we need to modify this byte or not
		to_modify = 0
		if i in places_to_modify:
			to_modify = 1
		if to_modify == 1:
			new_b = modify_byte(input_b)
			ouf.write(int_to_bytes(new_b))
			logging.debug("Output[%s]: %s",i,new_b)
		else:
			new_b = input_b
			ouf.write(new_b)
			logging.debug("Output[%s]: No change",i)

print("\nContents of fuzzed File:-", ofile, " ")
with open(ofile, 'r') as f:
	print(f.read())