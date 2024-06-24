import binascii
import ctypes
from itertools import islice
import string
import time
import os
import argparse


def encryption(v, k):
    y = ctypes.c_uint32(v[0])
    z = ctypes.c_uint32(v[1])
    sum = ctypes.c_uint32(0)
    delta = 0x9e3779b9
    n = 32
    w = [0, 0]

    while (n > 0):
        sum.value += delta
        y.value += (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        z.value += (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        n -= 1

    w[0] = y.value
    w[1] = z.value
    return w


def e_cfb(plaintext, cbit):
    v = [0x24495402, 0x38e0a1d1]
    k = [0x29039b12, 0Xa09df511, 0x5abc0006, 0x90ff3d80]
    b = "0b"  # for formatting required for conversion of binary to decimal
    v_full_length_str = bin(v[0])[2:].zfill(32) + bin(v[1])[2:].zfill(32)
    v_full_length_hex = int(b + v_full_length_str, 2)
    ciphertext = ""

    counter = 0

    plaintext = plaintext.encode('ascii')
    plaintext = bytearray(plaintext)
    plaintext = int(binascii.hexlify(plaintext), 16)  # convert to long
    print("Plaintext: ", bin(plaintext)[2:].zfill(64))
    p_len = len(bin(plaintext)[2:])
    if not p_len % 8 == 0:
        r = p_len % 8
        p_len = p_len + (8 - r)
    print(p_len)
    if p_len % cbit == 0:
        num_of_round = p_len / cbit
        extra_bit = 0
    else:
        num_of_round = (p_len // cbit) + 1
        extra_bit = (num_of_round * cbit) - p_len

    plaintext_hex = plaintext << (64 - (p_len + extra_bit))
    plaintext_bin = bin(plaintext_hex)[2:].zfill(64)

    while counter < num_of_round:
        print(
            f"\n=============================================== ENCRYPTION ROUND: {counter + 1} ===============================================\n")
        bit_length = counter * cbit

        if counter == 0:

            print(f"{'IV:':<12}{v_full_length_str:>1}")
            print("Plaintext: ", plaintext_bin)
            output = encryption(v, k)

            # combine v into a string of binary numbers
            output_bin = bin(output[0])[2:].zfill(32) + bin(output[1])[2:].zfill(32)
            print("output_bin:", output_bin)  # Output binary

            # print("Output: ", int(b + output_bin, 2))
            # XOR output and plaintext
            output_bin = int(b + output_bin, 2) ^ int(b + plaintext_bin, 2)
            print("XOR Output:", bin(output_bin)[2:].zfill(64))

            # obtain ciphertext by shifting
            cbit_bin = output_bin >> 64 - cbit
            temp_cipher = bin(cbit_bin)[2:].zfill(cbit)
            ciphertext += temp_cipher
            print("ciphertext:", temp_cipher)


        elif 0 < counter < num_of_round:
            print("Plaintext: ", plaintext_bin)
            print(f"{'IV:':<12}{v_full_length_str:>1}")

            temp_pt_bits = plaintext_hex >> (64 - bit_length)
            temp_pt_bits = temp_pt_bits << 64 - bit_length
            temp_pt_bits = plaintext_hex ^ temp_pt_bits
            temp_pt_bits = temp_pt_bits << bit_length

            print("Shifted PT:", bin(temp_pt_bits)[2:].zfill(64))

            # get the first cbits before shifting back to the front
            temp_iv_bits = bin(v_full_length_hex)[2:].zfill(64)
            temp_iv_bits = temp_iv_bits[bit_length:].zfill(64 - bit_length)
            temp_iv_bits = "0b" + temp_iv_bits + ciphertext

            # temp_iv_bits = temp_iv_bits << 64 - bit_length + ((counter - 1) * cbit)

            print("Shifted IV:", temp_iv_bits[2:].zfill(64))

            # split shifted iv
            temp_iv = []
            # Using islice
            temp_iv_bits = temp_iv_bits[2:].zfill(64)
            res_first = ''.join(islice(temp_iv_bits, None, len(temp_iv_bits) // 2))
            res_second = ''.join(islice(temp_iv_bits, len(temp_iv_bits) // 2, None))
            temp_iv.insert(0, (int((b + res_first), 2)))
            temp_iv.insert(1, (int((b + res_second), 2)))

            output = encryption(temp_iv, k)

            # combine v into a string of binary numbers
            output_bin = bin(output[0])[2:].zfill(32) + bin(output[1])[2:].zfill(32)
            print("output_bin:", output_bin)  # Output binary

            # XOR output and plaintext
            output_bin = int(b + output_bin, 2) ^ int(bin(temp_pt_bits), 2)
            print("XOR Output:", bin(output_bin)[2:].zfill(64))

            # obtain ciphertext by shifting
            cbit_bin = output_bin >> 64 - cbit
            temp_cipher = bin(cbit_bin)[2:].zfill(cbit)
            ciphertext += temp_cipher
            print("ciphertext:", temp_cipher)

        counter += 1
    print(
        "=================================================== Output =========================================================\n")
    print("CT Binary: ", ciphertext)
    ciphertext2 = b + ciphertext
    ciphertext_long = int(ciphertext2, 2)
    final_ciphertext = str(hex(ciphertext_long))
    print(f"{'CT Long:':<12}{ciphertext_long:>1}")
    print(f"{'CT Hex:':<12}{final_ciphertext} ")
    print(
        "====================================================================================================================\n")
    return ciphertext


def d_cfb(ciphertext, cbit):
    cbit = (int(cbit))
    v = [0x24495402, 0x38e0a1d1]
    k = [0x29039b12, 0Xa09df511, 0x5abc0006, 0x90ff3d80]
    b = "0b"  # for formatting required for conversion of binary to decimal
    v_full_length_str = bin(v[0])[2:].zfill(32) + bin(v[1])[2:].zfill(32)
    v_full_length_hex = int(b + v_full_length_str, 2)
    plaintext = ""

    p_len = len(ciphertext[2:])
    if not p_len % 8 == 0:
        r = p_len % 8
        p_len = p_len + (8 - r)
    print(p_len)
    counter = 0
    ciphertext = int(ciphertext, 2)
    print("ciphertext: ", bin(ciphertext)[2:])
    num_of_round = p_len / cbit

    ciphertext_hex = ciphertext << (64 - p_len)
    ciphertext_bin = bin(ciphertext_hex)[2:].zfill(64)
    while counter < num_of_round:
        print(
            f"\n=============================================== DECRYPTION ROUND: {counter + 1} ===============================================\n")
        bit_length = counter * cbit

        if counter == 0:

            print(f"{'IV:':<12}{v_full_length_str:>1}")
            print("ciphertext:", ciphertext_bin)
            output = encryption(v, k)

            # combine v into a string of binary numbers
            output_bin = bin(output[0])[2:].zfill(32) + bin(output[1])[2:].zfill(32)
            print("output_bin:", output_bin)  # Output binary

            # XOR output and ciphertext
            output_bin = int(b + output_bin, 2) ^ int(b + ciphertext_bin, 2)
            print("XOR Output:", bin(output_bin)[2:].zfill(64))

            # obtain plaintext by shifting
            cbit_bin = output_bin >> 64 - cbit
            temp_cipher = bin(cbit_bin)[2:].zfill(cbit)
            plaintext += temp_cipher
            print("plaintext: ", temp_cipher)


        elif 0 < counter < num_of_round:
            print("ciphertext:", ciphertext_bin)
            print(f"{'IV:':<12}{v_full_length_str:>1}")

            temp_pt_bits = ciphertext_hex >> (64 - bit_length)
            temp_cbit = bin(temp_pt_bits)[2:].zfill(bit_length)
            temp_pt_bits = temp_pt_bits << 64 - bit_length
            temp_pt_bits = ciphertext_hex ^ temp_pt_bits
            temp_pt_bits = temp_pt_bits << bit_length

            print("Shifted PT:", bin(temp_pt_bits)[2:].zfill(64))

            # get the first cbits before shifting back to the front
            temp_iv_bits = bin(v_full_length_hex)[2:].zfill(64)
            temp_iv_bits = temp_iv_bits[bit_length:].zfill(64 - bit_length)
            temp_iv_bits = "0b" + temp_iv_bits + temp_cbit

            # temp_iv_bits = temp_iv_bits << 64 - bit_length + ((counter - 1) * cbit)
            print("Shifted IV:", temp_iv_bits[2:].zfill(64))

            # split shifted iv
            temp_iv = []
            # Using islice
            temp_iv_bits = temp_iv_bits[2:].zfill(64)
            res_first = ''.join(islice(temp_iv_bits, None, len(temp_iv_bits) // 2))
            res_second = ''.join(islice(temp_iv_bits, len(temp_iv_bits) // 2, None))
            temp_iv.insert(0, (int((b + res_first), 2)))
            temp_iv.insert(1, (int((b + res_second), 2)))

            output = encryption(temp_iv, k)

            # combine v into a string of binary numbers
            output_bin = bin(output[0])[2:].zfill(32) + bin(output[1])[2:].zfill(32)
            print("output_bin:", output_bin)  # Output binary

            # XOR output and ciphertext
            output_bin = int(b + output_bin, 2) ^ int(bin(temp_pt_bits), 2)
            print("XOR Output:", bin(output_bin)[2:].zfill(64))

            # obtain plaintext by shifting
            cbit_bin = output_bin >> 64 - cbit
            temp_cipher = bin(cbit_bin)[2:].zfill(cbit)
            plaintext += temp_cipher
            print("plaintext: ", temp_cipher)

        counter += 1
    final_plaintext = "0b" + plaintext
    final_plaintext = int(final_plaintext, 2)
    final_plaintext = hex(final_plaintext)[2:]
    final_plaintext = bytearray.fromhex(final_plaintext)
    final_plaintext = final_plaintext.decode('ascii')
    return final_plaintext


def fileEncrypt(inputfile, outputfile):
    with open(inputfile, 'r') as f:
        with open(outputfile, "w") as o:
            tempStr = ""
            blocks = f.readlines()
            for block in blocks:
                block = [block[i:i + 8] for i in range(0, len(block), 8)]
                for b in block:
                    tempblock = e_cfb(b, 1)
                    tempStr += tempblock + "||"
            o.write(tempStr)
        f.close()
    f.close()


def fileDecrypt(inputfile, outputfile):
    with open(inputfile, 'r') as f:
        with open(outputfile, "w") as o:
            block = f.read()
            tempStr = block[:-2]
            templist = tempStr.split("||")
            temps = ""
            for tl in templist:
                ciphertext = '0b' + tl
                ciphertext = d_cfb(ciphertext, 1)
                temps += ciphertext.upper()
            o.write(temps)
        f.close()
    f.close()


def otp_encrypt(plaintext, key):
    alphabet = string.ascii_uppercase
    ciphertext = ""
    n = 1
    for char in plaintext:
        if char.isalpha():
            keystream = (pow(key, 2) + n) % 26
            key = keystream
            index = (alphabet.index(char) + keystream) % 26
            ciphertext += alphabet[index]
            n += 1

        else:
            ciphertext += char
    return ciphertext


def otp_encrypt_file(inputfile, outputfile):
    with open(inputfile, 'r') as input_file, \
            open(outputfile, 'w') as en_even:
        pt = input_file.read()
        ct = otp_encrypt(pt.upper(), 3)
        en_even.write(ct)


def otp_decrypt(ciphertext, key):
    alphabet = string.ascii_uppercase
    plaintext = ""
    counter = 1
    for char in ciphertext:
        if char.isalpha():
            n = counter
            keystream = (pow(key, 2) + n) % 26
            key = keystream
            index = ((alphabet.index(char) - keystream) % 26)
            plaintext += alphabet[index]
            counter += 1
        else:
            plaintext += char
    return plaintext


def otp_decrypt_file(inputfile, outputfile):
    with open(inputfile, 'r') as input_file, \
            open(outputfile, 'w') as de_even:
        ct = input_file.read()
        pt = otp_decrypt(ct.upper(), 3)
        de_even.write(pt)


def splitFile(filename):
    with open(filename, "r") as input_file, \
            open("even_characters.txt", "w") as even_file, \
            open("odd_characters.txt", "w") as odd_file:
        line = input_file.read()
        for x in range(0, len(line)):
            if x % 2 == 0:
                even_file.write(line[x])
            else:
                odd_file.write(line[x])


def joinFile(filename):
    with open("decrypted_even.txt", "r") as even_file, \
            open("decrypted_odd.txt", "r") as odd_file, \
            open(filename, "w") as output_file:
        even_lines = even_file.read()
        odd_lines = odd_file.read()
        output_line = ""
        for even_char, odd_char in zip(even_lines, odd_lines):
            output_line += even_char + odd_char
        output_file.write(output_line)


def combine_encryption_decryption(args):
    inputfile = args.combine_encryption_decryption[0]
    outputfile = args.combine_encryption_decryption[1]
    start_time = time.time()
    splitFile(inputfile)
    otp_encrypt_file("even_characters.txt", "encrypted_even.txt")
    otp_decrypt_file("encrypted_even.txt", "decrypted_even.txt")
    fileEncrypt("odd_characters.txt", "encrypted_odd.txt")
    fileDecrypt("encrypted_odd.txt", "decrypted_odd.txt")
    joinFile(outputfile)
    end_time = time.time() - start_time
    print("even_characters.txt generated")
    print("odd_characters.txt generated")
    print("decrypted_even.txt generated")
    print("encrypted_even.txt generated")
    print("decrypted_odd.txt generated")
    print("encrypted_odd.txt generated")
    print("Time taken %s seconds" % end_time)
    print("Time taken %s minutes" % (end_time / 60))


# Press the green button in the gutter to run the script.

def onebitcfb(args):
    inputfile = args.onebitcfb[0]
    outputfile = args.onebitcfb[1]
    start_time = time.time()
    fileEncrypt(inputfile, "cfb_encrypted.txt")
    fileDecrypt("cfb_encrypted.txt", outputfile)
    end_time = time.time() - start_time
    print("cfb_encrypted.txt generated")
    print("Time taken %s seconds" % end_time)
    print("Time taken %s minutes" % (end_time / 60))


def synchronous(args):
    inputfile = args.synchronous[0]
    outputfile = args.synchronous[1]
    start_time = time.time()
    otp_encrypt_file(inputfile, "otp_encrypted.txt")
    otp_decrypt_file("otp_encrypted.txt", outputfile)
    end_time = time.time() - start_time
    print("cfb_encrypted.txt generated")
    print("Time taken %s seconds" % end_time)
    print("Time taken %s minutes" % (end_time / 60))


def main():
    # create parser object
    parser = argparse.ArgumentParser(description="Help options")

    # defining arguments for parser object
    parser.add_argument("-ced", "--combine_encryption_decryption", type=str, nargs=2,
                        metavar=("inputfile, outputfile"), default=None,
                        help="Encrpytion and decryption of combined 1-bit and synchronous ")

    parser.add_argument("-cfb", "--onebitcfb", type=str, nargs=2,
                        metavar=("inputfile, outputfile"), default=None,
                        help="Encrpytion and decryption of 1-bit")

    parser.add_argument("-otp", "--synchronous", type=str, nargs=2,
                        metavar=("inputfile, outputfile"), default=None,
                        help="Encrpytion and decryption of synchronous")

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument
    if args. combine_encryption_decryption is not None:
        combine_encryption_decryption(args)
    elif args.onebitcfb is not None:
        onebitcfb(args)
    elif args.synchronous is not None:
        synchronous(args)


if __name__ == '__main__':
    main()
    # combine_encryption_decryption("textfile.txt", "cedOutput.txt")
    # onebitcfb("test.txt", "cfbOutput.txt")
    #
    # synchronous("textfile.txt", "synOutput.txt")
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
