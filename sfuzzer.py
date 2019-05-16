import sys
import logging
import os
import random
import argparse

''' Parsing the arguments 
(base) D:\>python sfuzzer.py --help
usage: sfuzzer.py [-h] [--o O]
                  [--p {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49}]
                  [--d D] [--s S]
                  InputFileName

A Simple File Fuzzer
********************

positional arguments:
  InputFileName         Input File Name to be fuzzed

optional arguments:
  -h, --help            show this help message and exit
  --o O                 Name of Output Fuzzed File
  --p {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49}
                        Percentage of Bytes to be fuzzed
  --d D                 Debug Level: INFO, DEBUG, WARNING
  --s S                 Seed Value : Any random integer

Contact:- joysn1980@yahoo.com
'''
parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description='''
A Simple File Fuzzer 
********************''',epilog='''
Contact:- joysn1980@yahoo.com
''')
parser.add_argument('InputFileName', help='Input File Name to be fuzzed')
parser.add_argument('--o', help='Name of Output Fuzzed File')
parser.add_argument('--p', help='Percentage of Bytes to be fuzzed ',type=int,default=50, choices=range(0, 50))
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