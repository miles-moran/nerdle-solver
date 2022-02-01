from pprint import pprint

operators = ["=", "+", "-", '*']
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
all = numbers + operators

possibles = {
    0: numbers + ["-"],
    1: all,
    2: all,
    3: all,
    4: all,
    5: all,
    6: all,
    7: numbers
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


def getFilteredPossibles(i, pos, eq):
    ops = ['+', '/', '*', '=']
    filtered = list(pos[i])
    if i > 0:
        previous = eq[i-1]
        #if the previous character is +, *, / or =, it this character must be a number or negative
        if previous in ops:
            filtered = list(filter(lambda x: x not in ops, filtered))
        #if the previous character is a -, this character must be a number
        elif previous == "-":
            filtered = list(filter(lambda x: x in numbers, filtered))
        #if any previous character is an equals sign, this character cannot be an equal sign
        if "=" in eq[:i-1]:
            filtered = list(filter(lambda x: x != "=", filtered))
        if i > 3:
            numbersInLast4Spaces = list(filter(lambda x: x in numbers, eq[i-4:i]))
            #if last 4 items are numbers, next cannot be number
            if len(numbersInLast4Spaces) >= 4:
                filtered = list(filter(lambda x: x not in numbers, filtered))
    
    return filtered

def getFeedback(solution, guess, feedback = {
    "greens": {
        0: None,
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
        7: None,
    },
    "grays": [],
    "yellows": {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: [],
        6: [],
        7: [],
    }
}):
    for i in range(0, 8):
        g = guess[i]
        if g not in solution and g not in feedback['grays']:
            feedback['grays'].append(g)
        else:
            for j in range(0, 8):
                s = solution[j]
                if i == j and s == g:
                    feedback['greens'][i] = g
                elif i != j and s == g and g not in feedback['yellows'][i]: #fix this
                    feedback['yellows'][i].append(g)
    return feedback

def applyFeedback(feedback, pos):
    for i in range(0, 8):
        for y in feedback['yellows'][i]:
            if y in pos[i]:
                pos[i] = list(filter(lambda x: x!= y, pos[i]))
        for g in feedback['grays']:
            pos[i] = list(filter(lambda x: x!= g, pos[i]))
        if feedback['greens'][i] is not None:
            pos[i] = [feedback['greens'][i]]
    return pos

def meetsCriteria(eq, feedback):
    valid = True
    mustHaves = []
    for f in feedback['yellows']:
        mustHaves += feedback['yellows'][f]
    for m in mustHaves:
        if m not in eq:
            return False
    return valid


def attempt(feedback):
    equation = ['', '', '', '', '', '', '', ''] 
    global guess
    global best
    guess = None
    best = None
    def solve(possibles, r = 0, a = 1):
        global guess
        global best
        if r == len(equation):
            return
        for i in getFilteredPossibles(r, possibles, equation):
            if guess is not None:
                return guess
            equation[r] = str(i)
            if r == len(equation) - 1:
                #equation must have every unique number from yellows
                if isValidEquation(equation) == True and meetsCriteria(equation, feedback) == True:
                    g = ''.join(equation)
                    if best is None or len(set(g)) > len(set(best)):
                        best = g
                        if a == 1:
                            if len(set(best)) == 8:
                                guess = ''.join(equation)
                    
            solve(possibles, r + 1)
    solve(possibles)
    if guess is None and best is not None:
        return best
    return guess

solution = "3-7*1=-4"
guess = '1=4-6+03'
print('-1-')
print(guess)
feedback = getFeedback(solution, guess)
possibles = applyFeedback(feedback, possibles)
guess = '01=2*5-9'
print('-2-')
print(guess)
feedback = getFeedback(solution, guess)
possibles = applyFeedback(feedback, possibles)
guess = attempt(feedback)
print('-3-')
print(guess)
feedback = getFeedback(solution, guess)
possibles = applyFeedback(feedback, possibles)
guess = attempt(feedback)
print('-4-')
print(guess)
