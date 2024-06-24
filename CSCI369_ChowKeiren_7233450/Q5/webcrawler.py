# Question 5
# Chow Keiren 7233450
import requests

ip = "10.0.2.4"  # Your Metasploitable’s IP can be different
target = "http://" + ip + "/mutillidae"

# Read possible directory names from "dirs.txt"
with open("dirs.txt", "r") as f:
    directory_names = f.read().splitlines()

for name in directory_names:
    url = f"{target}/{name}"
    response = requests.get(url)

    if response.status_code == 200:
        print(f"Subdirectory {name} found: {url}")