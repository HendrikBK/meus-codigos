def pad_num(num, amt):
    num = str(num)
    if len(str(num)) >= amt:
        return str(num)
    else:
        while len(str(num)) < amt:
            num = '0' + num
        return str(num)