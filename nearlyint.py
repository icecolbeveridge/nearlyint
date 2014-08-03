# string contains: (constants) 0123456789EP (ops) */+-^L
# preceded by list of 0, followed by list of *
# p7* would give ~ 22

from math import exp, pi, log, floor, ceil
from random import choice, random

def prm(a,b):
    if abs(a) > 1.e-3 and abs(b) > 1.e-3:
        return a*b
    else:
        return 0.

def handleString( str, stack, verbose = False ):
    # if it's empty, multiply the stack together
    if verbose:
        print str, stack
    if (not str):
        try:
            
            return reduce( prm, stack )
        except:
            return 0
            
    a, b = str[0], str[1:]
    # if it's a number, stick it on the stack
    if ( a in "0123456789" ):
        stack.append( float(a) )
    elif a == "e":
        stack.append( exp(1) )
    elif a == "p":
        stack.append( pi )
    else:
        try:
            x = stack.pop()
        except IndexError:
            x = 0.
        if a == "l":
            try:
                stack.append( log(x) )
            except ValueError:
                stack.append(0.)
        
        else:
            try:
                y = stack.pop()
            except IndexError:
                y = 0.
            if a == "*":
                stack.append(x * y)
            elif a == "^":
                try:
                    stack.append(x ** y)
                except OverflowError:
                    stack.append(0.)
                except ZeroDivisionError:
                    stack.append(0.)
                except ValueError:
                    stack.append(0.)
            elif a == "/":
                try:
                    stack.append(x / y)
                except ZeroDivisionError:
                    stack.append(0.)
            elif a == "+":
                stack.append(x + y)
            elif a == "-":
                stack.append(x - y)
    return handleString(b, stack, verbose = verbose)

def scoreString( str ):
    x = handleString( str, [] )
    score = min( abs(x - floor(x)), abs(x - ceil(x)))
    if score == 0:
        score = 0.5
    return (score, x)
     
def combine( str1, str2 ):
    x1 = choice(range(len(str1)))
    x2 = choice(range(len(str2)))
    return( str1[:x1] + str2[x2:], str2[:x2] + str1[x2:] )

def mutate( str ):
    x = choice(range(len(str)))
    return str[:x] + randomChar() + str[x+1:]

def randomChar():
    return choice("0123456789epl*/+-^")


def randomString(p = 0.1):
    out = randomChar()
    while random() > p:
        out += randomChar()
    return out
# simple GA
#  - population of 100
#  - top 10 replicate
#  - top 10 mutate
#  - top 80 crossover

def rankPop( pop ):
    out = [ (scoreString(p), p) for p in pop ]
    out.sort()
    return out
        
        

def doGA( pop = 100 ):
    pop = [ randomString() for i in range(100) ]
    gen = 0
    while True:
        print "**** %d ****" % gen
        gen += 1
        
        pr = rankPop(pop)
        pop = []
        start = True
        for k in range(10):
            i = pr[k]

            if start:
                start = False
                print handleString(i[1], [], True)
                print i
                kk = raw_input("Kill?")
                if kk:
                    i = (() ,randomString() )
            else:
                print i
            
            if i[1] != pr[k+1][1]:
                pop.append(i[1])
                pop.append(mutate(i[1]))

        while len(pop) < 100:
            i1 = choice(range(80))
            i2 = choice(range(80))
            x = combine(pr[i1][1], pr[i2][1])
            pop.append(x[0])
            pop.append(x[1])
        
doGA()
