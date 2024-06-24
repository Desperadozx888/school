UOWID: 7233450
results mod 7 = 2 #Therefore 2bit cfb 


Help option:
python 2bitCFB.py -h

commands:
python 2bitCFB.py -e <student number> <cbit>
python 2bitCFB.py -d <ciphertext(binary)> <cbit>

encryption:
python 2bitCFB.py -e 7233450 2

command for output file for easier viewing of printed text:
python 2bitCFB.py -e 7233450 2 >encryptionOutput.txt

decryption:
python 2bitCFB.py -d 1000000101000000001001011000 2

command for output file for easier viewing of printed text:
python 2bitCFB.py -d 1000000101000000001001011000 2 >decryptionOutput.txt



