# This is a sample Python script.
import ctypes
from itertools import islice
import argparse



# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

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


def e_cfb(args):
    plaintext = args.e_cfb[0]
    cbit = args.e_cfb[1]
    cbit = int(cbit)

    v = [0x24495402, 0x38e0a1d1]
    k = [0x29039b12, 0Xa09df511, 0x5abc0006, 0x90ff3d80]
    b = "0b"  # for formatting required for conversion of binary to decimal
    v_full_length_str = bin(v[0])[2:].zfill(32) + bin(v[1])[2:].zfill(32)
    v_full_length_hex = int(b + v_full_length_str, 2)
    ciphertext = ""
    counter = 0

    plaintext = int(plaintext, 16)  # convert to long
    print("Plaintext: ", bin(plaintext)[2:])
    p_len = len(bin(plaintext)[2:])

    if p_len % cbit == 0:
        num_of_round = p_len / cbit
        extra_bit = 0;
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

    with open("ciphertext.txt", 'w') as f:
        f.write("=================================================== Output =========================================================\n")
        f.write(f"CT Binary: {ciphertext}\n")
        f.write(f"{'CT Long:':<12}{ciphertext_long:>1}\n")
        f.write(f"{'CT Hex:':<12}{final_ciphertext}\n")
        f.write("====================================================================================================================\n")
    f.close()


def d_cfb(args):
    ciphertext = args.d_cfb[0]
    cbit = args.d_cfb[1]
    cbit = int(cbit)
    v = [0x24495402, 0x38e0a1d1]
    k = [0x29039b12, 0Xa09df511, 0x5abc0006, 0x90ff3d80]
    b = "0b"  # for formatting required for conversion of binary to decimal
    v_full_length_str = bin(v[0])[2:].zfill(32) + bin(v[1])[2:].zfill(32)
    v_full_length_hex = int(b + v_full_length_str, 2)
    plaintext = ""

    counter = 0
    p_len = len(ciphertext)
    ciphertext = b + ciphertext
    ciphertext = int(ciphertext, 2)  # convert to long
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

            print("Shifted CT:", bin(temp_pt_bits)[2:].zfill(64))

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
    print("=================================================== Output =========================================================\n")
    print("PT Binary: ", plaintext)
    plaintext = b + plaintext
    plaintext_long = int(plaintext, 2)
    final_plaintext = str(hex(plaintext_long))
    print(f"{'PT Long:':<11} {plaintext_long : >1}")
    print(f"{'PT Hex:':<12}{final_plaintext[2:]:>1} ")
    print(
        "====================================================================================================================\n")

    with open("plaintext.txt", 'w') as f:
        f.write("=================================================== Output =========================================================\n")
        f.write(f"PT Binary: {plaintext}\n")
        f.write(f"{'PT Long:':<11} {plaintext_long : >1}\n")
        f.write(f"{'PT Hex:':<12}{final_plaintext[2:]:>1}\n")
        f.write("====================================================================================================================\n")
    f.close
    return final_plaintext


def main():
    # create parser object
    parser = argparse.ArgumentParser(description="Help options")

    # defining arguments for parser object
    parser.add_argument("-e", "--e_cfb", type=str, nargs=2,
                        metavar=("Student No", "C-bit"),
                        default=None,
                        help="Input student number, followed by C-bit")

    parser.add_argument("-d", "--d_cfb", type=str, nargs=2,
                        metavar=("CipherText", "C-bit"), default=None,
                        help="Input ciphertext(Hex), followed by Cbit")

    # parse the arguments from standard input
    args = parser.parse_args()

    # calling functions depending on type of argument

    if args.e_cfb is not None:
        e_cfb(args)
    elif args.d_cfb is not None:
        d_cfb(args)


if __name__ == "__main__":
    # calling the main function
    start_time = time.time()
    main()
    end_time = time.time() - start_time
    print("Time taken %s seconds" % end_time)
    print("Time taken %s minutes" % (end_time / 60))
