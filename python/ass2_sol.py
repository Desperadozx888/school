name = 'John Snow'  # (1) REPLACE THE STRING VARIABLE WITH YOUR NAME in string type
student_num = '1234567' # (2) REPLACE THIS STRING VARIABLE WITH YOUR UOW ID in string type
subject_code = 'CSIT110'

def hocusPocus(N):
    obj = []
    for i in range(1, N + 1):
        txt = ""
        if i % 5 == 0:
            txt += "Hocus"
        elif i % 9 == 0:
            txt += "Pocus"
        if txt:
            obj.append(txt)
        else:
            obj.append(i)
    return obj      


def question_2():
    age = int(input("Enter current age: "))
    OA = float(input("Enter current amount in OA: "))
    SA = float(input("Enter current amount in SA: "))
    MA = float(input("Enter current amount in MA: "))
    # calculate basic interest
    interest = 0
    interest += OA* 0.025
    interest += SA*0.04
    interest += MA*0.04

    # calculate extra interest
    # get first 60k
    basic_sum = 0
    if OA >= 20000:
        basic_sum += 20000
    else:
        basic_sum += OA
    # basic_sum += min(OA, 20000)
    basic_sum += SA + MA
    if basic_sum >=60000:
        basic_sum = 60000

    if age >= 55:
        RA = float(input("Enter current amount in RA: "))
        interest += RA*0.04
        if basic_sum + RA >=60000:
            basic_sum = 60000
        else:
            basic_sum += RA
        # 
        if basic_sum >=30000:
            # 2% for first 30k and 1% for next 30k
            interest += 30000*0.02 + (basic_sum-30000)*0.01
        else:
            interest += basic_sum*0.02
    else:
        interest += basic_sum*0.01
    
    print(f"Your interest rate this year will be ${interest:.2f}")


def question_3():
    PRICE_SINGLE = 90
    PRICE_TWIN = 150
    PRICE_DELUXE = 250
    PRICE_SUITE = 1050
    # get input
    num_single = int(input("Number of Single rooms: "))
    num_twin = int(input("Number of Twin rooms: "))
    num_deluxe = int(input("Number of Deluxe rooms: "))
    num_suite = int(input("Number of Suites: "))
    length_of_stay = int(input("Length of stay(number of nights): "))
    print()
    print(f"Summary of your booking for {length_of_stay} night(s)")
    # compute prices for each room type and its str format. 
    total_single = num_single*PRICE_SINGLE*length_of_stay
    price_single_str = f"${total_single:.2f}"
    total_twin = num_twin*PRICE_TWIN*length_of_stay
    price_twin_str = f"${total_twin:.2f}"
    total_deluxe = num_deluxe*PRICE_DELUXE*length_of_stay
    price_deluxe_str = f"${total_deluxe:.2f}"
    total_suite = num_suite*PRICE_SUITE*length_of_stay
    price_suite_str = f"${total_suite:.2f}"
    subtotal = total_single + total_twin + total_deluxe + total_suite
    subtotal_str = f"${subtotal:.2f}"
    total = subtotal*1.07
    total_str = f"${total:.2f}"
    print(f"{'Single room':<13}{num_single:^3}{price_single_str:>10}")
    print(f"{'Twin room':<13}{num_twin:^3}{price_twin_str:>10}")
    print(f"{'Deluxe room':<13}{num_deluxe:^3}{price_deluxe_str:>10}")
    print(f"{'Suite':<13}{num_suite:^3}{price_suite_str:>10}")
    num_total = num_single + num_twin + num_deluxe + num_suite
    print(f"{'Subtotal':<13}{num_total:^3}{subtotal_str:>10}")
    print(f"{'Total(7% g.s.t)':<16}{total_str:>10}")
    
    # or 
    def format_price(price):
      return f"${price:.2f}"
    total_single = num_single*PRICE_SINGLE*length_of_stay
    total_twin = num_twin*PRICE_TWIN*length_of_stay
    total_deluxe = num_deluxe*PRICE_DELUXE*length_of_stay
    total_suite = num_suite*PRICE_SUITE*length_of_stay
    subtotal = total_single + total_twin + total_deluxe + total_suite
    total = subtotal*1.07
		print(f"{'Single room':<13}{num_single:^3}{format_price(total_single):>10}")
    print(f"{'Twin room':<13}{num_twin:^3}{format_price(total_twin):>10}")
    print(f"{'Deluxe room':<13}{num_deluxe:^3}{format_price(total_deluxe):>10}")
    print(f"{'Suite':<13}{num_suite:^3}{format_price(total_suite):>10}")
    num_total = num_single + num_twin + num_deluxe + num_suite
    print(f"{'Subtotal':<13}{num_total:^3}{format_price(total_single):>10}")
    print(f"{'Total(7% g.s.t)':<16}{total_str:>10}")

def recover_files():
    cleaned = ""
    while True:
        filename = input("Filename?")
        if not filename:  # if filename == "" or len(filename) == 0
            break
        while filename.rfind("{") != -1:
            open_idx = filename.rfind("{")
            close_idx = filename[open_idx:].find("}") + open_idx
            filename = filename[:open_idx] + filename[close_idx+1:]

        cleaned += filename + ","
    return cleaned[:-1]


def main():
    print("Assignment2")
    print(hocusPocus(45))
    print(hocusPocus(90))