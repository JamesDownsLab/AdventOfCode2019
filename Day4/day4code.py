# Secure Container

# It is a 6 digit number
# Value is within 284639 and 748759
# Two adjacent digits are the same
# From left to right digits never decrease
start = 284639
end = 748759

def digits_do_not_decrease(digits):
    for i in range(len(digits)-1):
        if digits[i+1] < digits[i]:
            return False
    return True

def has_repeated_adjacent_digits(digits):
    for i in range(len(digits)-1):
        if digits[i+1] == digits[i]:
            return True
    return False

def has_repeated_adjacent_digits_not_part_of_larger_set(digits):
    result = False
    repeats = []
    di = 0
    while di < len(digits):
        digit = digits[di]
        repeat = 0
        remaining_digits = digits[di+1:]
        if len(remaining_digits) == 0:
            di += 1
            break
        for digit2 in remaining_digits:
            if digit2 == digit:
                repeat += 1
                di += 1
            else:
                di += 1
                break
        repeats.append(repeat)
        # di += 1
    print(digits, repeats)
    if 1 in repeats:
        return True
    else:
        return False



# def has_repeated_adjacent_digits_not_part_of_larger_set(digits):
#     pairs_match = [digits[i+1]==digits[i] for i in range(len(digits)-1)]
#     splits = []
#     for p in range(len(pairs_match)-1):
#         if pairs_match[p+1] != pairs_match[p]:
#             splits.append(p+1)
#     if len(splits) == 0:
#         return True
#     if len(splits) == 1:
#         groups = [pairs_match[:splits[0]], pairs_match[splits[0]:]]
#     else:
#         indices = [(0, splits[0])] + [(a, b) for a, b in zip(splits[:-1], splits[1:])]
#         if splits[-1] != len(splits):
#             indices += [(splits[-1], len(splits))]
#         groups = [pairs_match[a:b] for a, b in indices]
#     for group in groups:
#         if True in group:
#             if len(group) == 1:
#                 print(groups)
#                 print(digits)
#                 return True
#     return False




passwords_part1 = []
passwords_part2 = []
for p in range(start, end+1):
    password = [int(a) for a in str(p)]

    if not digits_do_not_decrease(password):
        pass
    else:
        if has_repeated_adjacent_digits(password):
            passwords_part1.append(p)
        if has_repeated_adjacent_digits_not_part_of_larger_set(password):
            passwords_part2.append(p)
print(len(passwords_part1))
print(len(passwords_part2))