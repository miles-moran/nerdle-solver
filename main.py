operators = ['+', "="]
numbers = [0, 1, 2]
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

def isValidEquation(equation):
    valid = False
    try:
        eq = ''.join(equation)
        eq = eq.split("=")
        if eval(eq[0]) == eval(eq[1]):
            valid = True
    except:
        valid = False
   
    return valid

equation = ['', '', '', '', '', '', '', '']
guess = None
for i in range(0, 8):
    if guess is not None:
        break
    pis = possibles[i]
    for pi in pis:
        if guess is not None:
            break
        equation[i] = str(pi)
        for j in range(i + 1, 8):
            if guess is not None:
                break
            pjs = possibles[j]
            for pj in pjs:
                if guess is not None:
                    break
                equation[j] = str(pj)
            if j == 7:
                print(equation)
                if isValidEquation(equation) == True:
                    guess = equation
                    break


print(guess)

