from pprint import pprint
import re

operators = ["=", "+", "-", '*']
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

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
        eq[0] = re.sub(r'\b0+(?!\b)', '', eq[0])
        eq[1] = re.sub(r'\b0+(?!\b)', '', eq[1])
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

def getFreshFeedback():
    return {
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
}

def getFreshPossibles():
    all = numbers + operators
    return {
        0: numbers + ["-"],
        1: all,
        2: all,
        3: all,
        4: all,
        5: all,
        6: all,
        7: numbers
    }

def getFeedbackAndColors(solution, guess, feedback):
    colors = ['', '', '', '', '', '', '', '']
    for i in range(0, 8):
        g = guess[i]
        s = solution[i]
        if g not in solution:
            if g not in feedback['grays']:
                feedback['grays'].append(g)
            colors[i] = 'gray'
        
        if g in solution:
            if s == g:
                feedback['greens'][i] = g
                colors[i] = 'green'
            else:
                feedback['yellows'][i].append(g)
                colors[i] = 'yellow'
    return {
        "f": feedback,
        "c": colors
    }

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


def attempt(feedback, possibles):
    equation = ['', '', '', '', '', '', '', ''] 
    def solve(possibles, r = 0):
        if r == len(equation):
            return
        for i in getFilteredPossibles(r, possibles, equation):
            equation[r] = str(i)
            if r == len(equation) - 1:
                if isValidEquation(equation) == True and meetsCriteria(equation, feedback) == True:
                    return ''.join(equation)
            guess = solve(possibles, r + 1)
            if guess is not None:
                return guess
    return solve(possibles)

def solve(solution, FIRST_GUESS = '6-1+2=03'):
    numbers.sort(key=lambda x: x in FIRST_GUESS, reverse=False)
    answer = None
    guess = None
    a = 0
    attempts = []
    possibles = getFreshPossibles()
    feedback = getFreshFeedback()
    while answer is None:
        if a == 0:
            guess = FIRST_GUESS
        else:
            guess = attempt(feedback, possibles)
        print('-----')
        print(guess)
        feedbackAndColors = getFeedbackAndColors(solution, guess, feedback)
        feedback = feedbackAndColors['f']
        colors = feedbackAndColors['c']
        possibles = applyFeedback(feedback, possibles)
        attempts.append({
            "feedback": feedback,
            "guess": guess,
            'colors': colors
        })
        if guess == solution:
            answer = guess
        a += 1
    return attempts