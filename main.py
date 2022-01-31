from turtle import pos


operators = ["="]
numbers = [0]
all = numbers + operators
possibles = {
    0: all,
    1: all,
    2: all,
    3: all,
    4: all,
    5: all,
    6: all,
    7: all
}

def find(s, ch):
    return [i for i, ltr in enumerate(s) if ltr == ch]

def isValidEquation(equation):
    eq = ''.join(equation)
    equals = find(eq, '=')
    if len(equals) != 1:
        return False
    valid = False
    try:
        eq = eq.split("=")
        if eval(eq[0]) == eval(eq[1]):
            valid = True
    except:
        valid = False
    return valid

equation = ['', '', ''] 
guess = None
b = 0

def test(r = 0):
    global b
    global guess
    if r == len(equation):
        return
    for i in possibles[r]:
        equation[r] = str(i)
        if r == len(equation) - 1:
            print(equation)
            b += 1
            if isValidEquation(equation) == True:
                guess = ''.join(equation)
                print('guess found', guess)
        test(r + 1)

test()
print(b)
print(guess)



