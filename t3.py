def findnum():
    num = 0
    riboa = num * num
    while len(str(riboa)) < 11:
        mone = False
        for number in range(10):
            for char in str(riboa):
                if str(number) == char:
                    mone = True
                    break
            if not mone:
                break
            else:
                mone = False
            if number == 9:
                print(num, riboa)
        num = num + 1
        riboa = num * num

findnum()