import os
import argparse
import random
import string

# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .txt file."
INVALID_PATH_MSG = "Error: Invalid file path/name. File %s does not exist."


def validate_file(f_name):
    if not validate_path(f_name):
        print(INVALID_PATH_MSG % f_name)
        quit()
    elif not validate_filetype(f_name):
        print(INVALID_FILETYPE_MSG % f_name)
        quit()
    return


def validate_filetype(f_name):
    # validate file type
    return f_name.endswith('.txt')


def validate_path(path):
    # validate file path
    return os.path.exists(path)


def random_key(args):
    # obtaining filename from user
    f_name = args.random_key[0]
    # check if key text exist proceeds to encryption, if not generate one
    if (validate_filetype(f_name) and validate_path(f_name)) is False:
        generate_key_string(f_name)
    elif (validate_filetype(f_name) and validate_path(f_name)) is True:
        print("Keyfile has already been generated")


def generate_key_string(f_name):
    gkey = list(string.ascii_uppercase)  # obtain alphabets from A to Z
    random.shuffle(gkey)
    gkey = ''.join(gkey)
    with open(f_name, 'w') as f:
        f.write(gkey)
    f.close()


def read_keyfile(f_name):
    with open(f_name, 'r') as f:
        key_string = f.read()
        keys = {key_string[i]: key_string[i + 1] for i in range(0, len(key_string), 2)}
    f.close()
    return keys


def get_key_pair(keys):
    for k, v in keys.items():
        if 'F' == k:
            alpha = v
        elif 'F' == v:
            alpha = k
    return alpha


def translate(keys, text_file):
    # Empty String
    output = ""
    data = ""
    # get the key value pair from 'F'
    alpha_str = get_key_pair(keys)
    # Now we have to read the text file
    with open(text_file) as f:
        while True:
            # Now we need the file character by character
            c = f.read(1)  # When we read a file send a boolean value there
            if not c:
                print("End of file")
                break
            if c.isalpha():
                for k, v in keys.items():
                    if c == 'F':
                        data = c
                    elif c == alpha_str:
                        data = c
                    elif c == k:
                        data = v
                    elif c == v:
                        data = k
            else:
                data = c
            output += data
    f.close()
    return output


def encryption(args):
    keyfile = args.encryption[0]
    p_text = args.encryption[1]
    c_text = args.encryption[2]

    # translate to data while reading keyfile and converting to dictionary and reading the plaintext
    with open(c_text, 'w') as f:
        f.write(translate(read_keyfile(keyfile), p_text))
    f.close()


def decryption(args):
    keyfile = args.decryption[0]
    c_text = args.decryption[1]
    p_text = args.decryption[2]

    # translate to data while reading keyfile and converting to dictionary and reading the ciphertext
    with open(p_text, 'w') as f:
        f.write(translate(read_keyfile(keyfile), c_text))
    f.close()


def main():
    # create parser object
    parser = argparse.ArgumentParser(description="Help options")

    # defining arguments for parser object
    parser.add_argument("-k", "--random_key", type=str, nargs=1,
                        metavar="key", default=None,
                        help="Generate random key if keyfile.txt is not in folder directory")

    parser.add_argument("-e", "--encryption", type=str, nargs=3,
                        metavar=("keyfile", "plaintext", "ciphertext"),
                        default=None,
                        help="Input plaintext file in the same folder directory and obtain encrypted ciphertext output")

    parser.add_argument("-d", "--decryption", type=str, nargs=3,
                        metavar=("keyfile", "ciphertext", "plaintext"), default=None,
                        help="Input ciphertext file in the same folder directory and obtain decrypted ciphertext output")

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.random_key is not None:
        random_key(args)
    elif args.encryption is not None:
        encryption(args)
    elif args.decryption is not None:
        decryption(args)


if __name__ == "__main__":
    # calling the main function
    main()
