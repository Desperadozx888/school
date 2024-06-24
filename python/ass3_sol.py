def generate_qns_from_list(lst: list): # e.g. [[1,3,3], [2, 5, -1], [3,2], [4,5,3],...
    math_qns = []
    for ele in lst:  # [1,3,3], [2,5,-1],...
        if len(ele) >= 2:
            qns = str(ele[0]) #"1"
            ans = ele[0]      #1
            for idx in range(1, len(ele)):  # 3,3
                qns += " - " + str(ele[idx]) # "1 - 3", "1 - 3 - 3"
                ans -= ele[idx] # 4, 7
            math_qns.append({"qns": qns, "ans": ans})
    return math_qns

class Catalogue:
    services = {
        "Singapore Power": 12.98,
        "Water Works": 32.99,
        "SG Telecomms": 16.98,
        "TV Licensing": 21.98,
        "New Age Data Hub": 23.98,
        "Waste Collection and Recycling": 18.98
    }
    hotline = "1800-9999-4567"
    def __init__(self, serial_num: str):
        self.serial_num = serial_num

    @classmethod
    def display(cls):
        print("List of default service subscription:")
        print(f"{'Service':<30}{'Price/mth':>10}")
        def format_price(float):
            return f"${float:.2f}"
        for service, price in cls.services.items():
            print(f"{service:<30}{format_price(price):>10}")
    
    @classmethod
    def get_subscription(cls):
        subscription = []
        for service in cls.services:
            ans = input(f"Opt out of {service}? (Y/N): ")
            if ans.lower() == "n":
                subscription.append(service)
        return subscription


class Customer():
    count = 0
    def __init__(self, name):
        self.name = name
        Customer.count += 1
        self.subscription = Catalogue.get_subscription()

		
def get_nric_checksum(input_string):
    digits = []
    weights = [2,7,6,5,4,3,2]
    checksum_letters = ["J","Z","I","H","G","F","E","D","C","B","A"]
	# or 
	checksum_letters = "JZIHGFEDCBA"
    for char in input_string: #"1234567"
        # assumes there are all valid
        digits.append(int(char)) #[1,2,3,4,5,6,7]
    total = 0
    for i in range(0,len(digits)): #1*2+ 2*7...
        total  += weights[i]*digits[i]
	# if you do not want to use digits
	# for i in range(0,len(input_string)): #1*2+ 2*7...
    #     total  += weights[i]*int(input_string[i])
    R = total % 11
    return checksum_letters[R]


def get_vehicle_plate_checksum(input_string: str):
    checksum_letters = ["A", "Z", "Y", "X", "U", "T",
                        "S", "R", "P", "M", "L", "K",
                        "J", "H", "G", "E", "D", "C", "B"]
	# OR
	# checksum_letters = "AZYXUTSRPMLKJHGEDCB"
    prefix = []
    digits = []
    six_digits = []
    weights = [9,4,5,4,3,2]
    letters = '_abcdefghijklmnopqrstuvwxyz'
    # or 
    #initialise alphabet mapping
    letter2num = {} #{'a':1, 'b':2, 'c':3, 'd':4, 'e':5, ...}
    counter = 0
    for l in letters:
        letter2num[l] = counter
        counter +=1
	
	# Conversion
    for ith_char in input_string: #"E15"
        # try:
        #     number = int(ith_char)
        # except ValueError:  # character is a letter 
        #     prefix.append(letter2num[ith_char.lower()]) # letter2num['e']
        # else:
        #     digits.append(number)
        if ith_char.isalpha():
			number = letter2num[ith_char.lower()]
            prefix.append(number)
			# if we use the 'letters' variable instead of letter2num
			# number = letters.find(ith_char.lower())
			# prefix.append(number)

        else:  # if ith_char.isdigit(): 
            digits.append(int(ith_char))
    
	# get 6 digits
	# work on the prefixes first
    if len(prefix)==3: #if SHA then prefix= [19,8,1]
        six_digits.extend(prefix[1:]) # prefix[1:] is [8,1]
    elif len(prefix)<2: # 1 letter e.g. E prefix is [5]
        six_digits = [0] 
        six_digits.extend(prefix) # [0,5]
    else: # 2 letters # e.g SA, [19,1]
        six_digits.extend(prefix) #six_digits = prefix

    #pad zeros for digits
    if len(digits)<4:
        six_digits.extend([0]*(4-len(digits))) 
        six_digits.extend(digits)
    else:
        six_digits.extend(digits)
    total = 0
    for i in range(0,len(six_digits)):
        total += six_digits[i]*weights[i]

    R = total % 19
    return checksum_letters[R]