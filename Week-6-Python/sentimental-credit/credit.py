def sumValidation(n):
    total_sum = 0
    every_other_num = True

    # Check if the number is in the valid range
    if n < 10**12 or n > 10**16:
        return False

    while n > 0:
        if every_other_num:
            total_sum += n % 10
            n //= 10
            every_other_num = False
        else:
            last_digit = n % 10
            double_last_digit = last_digit * 2

            if double_last_digit > 9:
                total_sum += double_last_digit % 10
                total_sum += double_last_digit // 10
            else:
                total_sum += double_last_digit

            n //= 10
            every_other_num = True

    return total_sum % 10 == 0


def cardIdentification(n):
    if not sumValidation(n):
        return "INVALID"

    length = 1
    temp = n
    while temp >= 10:
        temp //= 10
        length += 1

    first_digit = temp

    while n >= 100:
        n //= 10
    second_digit = n % 10

    if length == 15 and first_digit == 3 and second_digit in [4, 7]:
        return "AMEX"
    elif length == 16 and first_digit == 5 and 1 <= second_digit <= 5:
        return "MASTERCARD"
    elif length in [13, 16] and first_digit == 4:
        return "VISA"
    else:
        return "INVALID"


while True:
    try:
        num = int(input("Number: "))
        if num > 0:
            break
    except ValueError:
        pass

print(cardIdentification(num))