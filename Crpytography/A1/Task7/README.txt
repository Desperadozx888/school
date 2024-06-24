The output files for what i have tested are in the 3 folders. File name used and file generated are described below:

Synchronous cipher encryption & decryption function(inputfile, outputfile) produces: "otp_encrypted.txt"

inputfile = textfile.txt
outputfile = synOutput

1bit encryption & decryption function(inputfile, outputfile) produces: "cfb_encrypted.txt"
inputfile = text.txt
outputfile = cfbOutput

due to some error i cannot resolve some textfile with certain number of character might not be able to encrypt and decrypt but some can. I tried to include spaces and fullstops. so the 1bit might have error for some text files.

Combined encryption & decryption function (inputfile, outputfile) produces:
    print("even_characters.txt generated")
    print("odd_characters.txt generated")
    print("decrypted_even.txt generated")
    print("encrypted_even.txt generated")
    print("decrypted_odd.txt generated")
    print("encrypted_odd.txt generated")

inputfile = textfile.txt
outputfile = cedOutput.txt

=======================================================================================================
Help option:
python Task7.py -h

Command lines: 

combined encryption & decryption:
python Task7.py -ced <inputfile> <outputfile> 
python Task7.py -ced textfile.txt cedOutput.txt

1bit encryption & decryption:
python Task7.py -cfb <inputfile> <outputfile> 
python Task7.py -cfb text.txt cfbOutput.txt

Synchronous cipher encryption & decryption
python Task7.py -otp <inputfile> <outputfile> 
python Task7.py -otp textfile.txt synOutput.txt

 
