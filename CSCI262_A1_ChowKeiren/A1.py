#CSCI_262_A1_ChowKeiren_7233450

import hashlib


class PasswordAttribute:
    def __init__(self, password, hashed_password, reduction_value, password_usage):
        self.password = password
        self.hashed_password = hashed_password
        self.reduction_value = reduction_value
        self.password_usage = password_usage


class RainbowAttribute:
    def __init__(self, password, hashed_password):
        self.password = password
        self.hashed_password = hashed_password


def read_file():
    print("CSCI_262_A1_ChowKeiren_7233450")
    file_name = input("Enter filename: ")
    password_list = []

    try:
        # Open and read the password file
        with open(file_name, "r") as open_file:
            clean_passwords = [line.strip() for line in open_file]
            total_passwords = len(clean_passwords)

            for clean_password in clean_passwords:
                # Hash the password using MD5
                hashed_password = hashlib.md5(clean_password.encode()).hexdigest()
                long_int = int(hashed_password, 16)
                # Calculate the reduction function
                reduction_value = long_int % total_passwords
                password_list.append(PasswordAttribute(clean_password, hashed_password, reduction_value, False))
    except FileNotFoundError:
        print("Invalid filename or file does not exist")
    print(f"Number of passwords: {total_passwords}")
    rainbow_table = generate_rainbow_table(password_list)
    pre_images(rainbow_table, password_list, total_passwords)


def generate_rainbow_table(password_list):
    rainbow_table = []  # Initialize an empty list to store rainbow table entries

    # Iterate through the password attributes in the provided password_list
    for password_attribute in password_list:
        if not password_attribute.password_usage:
            password_attribute.password_usage = True  # Mark the password attribute as used
            temp_num = password_attribute.reduction_value
            temp_pw = password_attribute.password
            temp_hp = ""
            # print(f"RB Password: {password_attribute.password}")
            # print(f"RB Password: {password_attribute.hashed_password}")
            # print(f"RB reduction value: {password_attribute.reduction_value}")
            # print("--------------------------------------------------")
            for _ in range(4):
                password_list[temp_num - 1].password_usage = True  # Mark the next attribute as used
                # print(f"Password: {password_list[temp_num - 1].password}")
                # print(f"Password: {password_list[temp_num - 1].hashed_password}")
                # print(f"reduction value: {password_list[temp_num - 1].reduction_value}")
                # print("____________________________________________________________")
                temp_hp = password_list[temp_num - 1].hashed_password
                temp_num = password_list[temp_num - 1].reduction_value

            # print("==================================================================")
            rainbow_entry = RainbowAttribute(temp_pw, temp_hp)
            rainbow_table.append(rainbow_entry)

    # Sort the rainbow_table by hashed_password for easier lookup
    rainbow_table = sorted(rainbow_table, key=lambda x: x.hashed_password)

    # Open "Rainbow.txt" file in write mode using a context manager
    with open("Rainbow.txt", "w") as openFile:
        # Iterate through rainbow_table using enumerate, starting from index 1
        for i, rainbow_entry in enumerate(rainbow_table, start=1):
            # Create a formatted password_line string with index, password, and hashed_password
            password_line = f"{i}: Password: {rainbow_entry.password} || Final current hashes: {rainbow_entry.hashed_password}\n"

            # Write the formatted password_line to the "Rainbow1.txt" file
            openFile.write(password_line)

        # Write the total number of data (length of rainbow_table) to the end of the file
        openFile.write(f"Total number of data: {len(rainbow_table)}")

    return rainbow_table  # Return the generated rainbow table


def pre_images(rainbow_table, password_list, total_passwords):
    user_input = input("Please enter choice 1(Hash) or 2(password): ")
    # Hash
    if user_input == "1":
        user_hash_password = input("Enter Hash Value: ")
        print(f"HASH: {user_hash_password}")
    # Password
    elif user_input == "2":
        user_password = input("Enter Password: ")
        user_hash_password = hashlib.md5(user_password.encode()).hexdigest()
        print(f"HASH: {user_hash_password}")
    else:
        print("Invalid choice. Please enter 1 for Hash or 2 for Password.")
        return

    found = False
    max_iterations = len(rainbow_table)  # Set a limit on the number of iterations

    # Iterate through each entry in the rainbow table
    for rainbow_entry in rainbow_table:
        # Check if the current rainbow table entry's hashed_password matches the user's input hash
        if rainbow_entry.hashed_password == user_hash_password:
            found = True  # Mark that a match has been found
            print("Hash password Matched")
            print(f"rainbow Table: {rainbow_entry.password}||{rainbow_entry.hashed_password}")
            print("Hash-list:")

            hashed_password = hashlib.md5(rainbow_entry.password.encode()).hexdigest()
            long_int = int(hashed_password, 16)
            # Calculate the reduction function
            reduction_value = long_int % total_passwords
            for _ in range(4):
                temp_pw = password_list[reduction_value - 1]
                if user_hash_password == temp_pw.hashed_password:
                    print(f"Password: {temp_pw.password} || Hashed Password: {temp_pw.hashed_password}")

                else:
                    reduction_value = temp_pw.reduction_value
            break

    # If no match is found in the rainbow table, continue searching using reduction functions
    if not found:
        temp_user_int = int(user_hash_password, 16)
        reduction_value = temp_user_int % total_passwords
        temp_attribute = password_list[reduction_value - 1]
        iterations = 0  # Initialize the iteration counter
        # print(f"user_hash_password: {user_hash_password}")
        # print(f"temp_user_int: {temp_user_int}")
        # print(f"total_passwords: {total_passwords}")
        # print(f"reduction_value: {reduction_value}")

        # Continue searching using reduction functions until a match is found or maximum iterations are reached
        while not found and iterations < max_iterations:
            print(f"temp: {temp_attribute.password} || Hashed Password: {temp_attribute.hashed_password}")
            for rainbow_entry in rainbow_table:
                # Check if the current rainbow table entry's hashed_password matches the temporary attribute's hashed_password
                if rainbow_entry.hashed_password == temp_attribute.hashed_password:
                    hashed_password = hashlib.md5(rainbow_entry.password.encode()).hexdigest()
                    long_int = int(hashed_password, 16)
                    # Calculate the reduction function
                    reduction_value2 = long_int % total_passwords
                    for _ in range(4):
                        temp_pw = password_list[reduction_value2 - 1]
                        if user_hash_password == temp_pw.hashed_password:
                            found = True  # Mark that a match has been found
                            print("Hash password Matched")
                            print(f"rainbow Table: {rainbow_entry.password}||{rainbow_entry.hashed_password}")
                            print("Hash-list:")
                            print(f"Password: {temp_pw.password} || Hashed Password: {temp_pw.hashed_password}")
                            break
                        else:
                            reduction_value2 = temp_pw.reduction_value

                    if found:
                        break
            iterations += 1
            temp_attribute = password_list[temp_attribute.reduction_value - 1]

    # If no match is found in both searches, indicate that the hash password was not found in the rainbow table.
    if not found:
        print("Hash password not found in the rainbow table.")


if __name__ == "__main__":
    read_file()
