The below reduction function is used for the Assignment

Reduction Value = MD5(password) MOD NumberOfPasswordInFile

The logic flow:
1:Search for the given hash in the rainbow table.
2:If found:
  a. Apply the reduction function to the corresponding entry from the rainbow table.
  b. Continue applying the hash and reduction functions alternately in a   sequence (forming a hash chain) until a match with the original password hash is found.
  c. Once matched, output the original password (pre-image).
3:If not found:
 a. Apply the reduction function to the hash input and then hash the result, repeating this process until a hash that is in the rainbow table is produced.
 b. Once a match is found in the rainbow table, follow the steps in (2a) and (2b).
 c. Output the original password (pre-image) upon finding a match.


How to run the file: 
open terminal in the folder, run python3 A1.py
Enter filename: password.txt
Enter choice 1(hash) or 2(password): 1
Enter Hash Value: 
