# simple-fuzzer

(base) D:\>;python sfuzzer.py --help
usage: sfuzzer.py [-h] [--o O] [--p P] [--d D] [--s S] InputFileName  
  
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
  
file1.txt :-  
  
abcd  
efgh  
mn;.  
.,#$  
  
20% of the above file to be fuzzed and the seed value is 500  
  
(base) D:\>python sfuzzer.py file.txt --p 20 --s 500  
**********************************  
Input file Name:  file.txt  
file size: 22  
Bytes to modify : 4  
**********************************

Contents of fuzzed File:- file.txt.fz  
abcd  
efh  
mn�.�  
,#$  
  
