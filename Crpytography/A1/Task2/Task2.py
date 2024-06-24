import string
import os
import argparse

# error messages
INVALID_FILETYPE_MSG = "Error: Invalid file format. %s must be a .txt file."
INVALID_PATH_MSG = "Error: Invalid file path/name. Path %s does not exist."

e_dict_key = {}
d_dict_key = {}


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


def keywords(args):
    # obtaining Keyword from user
    desc_letters = string.ascii_uppercase[::-1]  # descending letters from Z..A
    kw_string = args.keywords[0]
    kw_string = kw_string.upper()
    temp = ""
    for x in kw_string:
        if x.isalpha():
            temp += x
    kw_string = temp
    kw_string += desc_letters
    kw_string = "".join(dict.fromkeys(kw_string))
    kw_string = [*kw_string.upper()]
    get_keys(kw_string)


def get_keys(kw_string):
    global e_dict_key
    global d_dict_key
    e_letters = string.ascii_uppercase
    d_letters = [*string.ascii_uppercase]
    for i in range(len(e_letters)):
        e_dict_key[e_letters[i]] = kw_string[i]

    for i in range(len(d_letters)):
        d_dict_key[kw_string[i]] = d_letters[i]


def encrypt(args):
    data = ""
    global e_dict_key
    # get the file name/path
    file_name = args.encrypt[0]

    # validate the file name/path
    validate_file(file_name)

    file = open("CipherOutput.txt", "w")
    # read and print the file content
    with open(file_name, 'r') as f:
        while True:
            # Now we need the file character by character
            c = f.read(1)  # When we read a file send a boolean value there
            if not c:
                print("End of file")
                break
            if c in e_dict_key:
                data = e_dict_key[c]
            else:
                data = c

            file.write(data)  # Writing the converted texts into Output_text.txt
    f.close()


def decrypt(args):
    data = ""
    global d_dict_key
    # get the file name/path
    file_name = args.decrypt[0]

    # validate the file name/path
    validate_file(file_name)
    file = open("PlainTextOutput.txt", "w")
    # read and print the file content
    with open(file_name, 'r') as f:
        while True:
            # Now we need the file character by character
            c = f.read(1)  # When we read a file send a boolean value there
            if not c:
                print("End of file")
                break
            if c in d_dict_key:
                data = d_dict_key[c]
            else:
                data = c
            file.write(data)  # Writing the converted texts into Output_text.txt
        file.close()


def main():
    # create parser object
    parser = argparse.ArgumentParser(description="Help options")

    # defining arguments for parser object
    parser.add_argument("-k", "--keywords", type=str, nargs=1,
                        metavar="key", default=None,
                        help="Please input a string as a keyword to generate key")

    parser.add_argument("-e", "--encrypt", type=str, nargs=1,
                        metavar="path", default=None,
                        help="Take a plaintext file in the same folder directory and encrypt to output a ciphertext")

    parser.add_argument("-d", "--decrypt", type=str, nargs=1,
                        metavar="file_name", default=None,
                        help="Take a ciphertext file in the same folder directory and encrypt to output a plaintext")

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args.keywords and args.encrypt is not None:
        keywords(args)
        encrypt(args)
    elif args.keywords and args.decrypt is not None:
        keywords(args)
        decrypt(args)
    elif args.keywords is not None:
        keywords(args)

if __name__ == "__main__":
    # calling the main function
    main()
