# string contains: (constants) 0123456789ep (ops) */+-^l
# preceded by list of 0, followed by list of *
# p7* would give ~ 22

from math import exp, pi, log, floor, ceil
from random import choice, random

def prm(a,b):
    # attempt to lose 'uninteresting' answers by killing stacks with tiny numbers in
    if abs(a) > 1.e-3 and abs(b) > 1.e-3:
        return a*b
    else:
        return 0.

def handleString( str, stack, verbose = False ):
    # if genome is empty, multiply the stack together
    if verbose:
        print str, stack
    if (not str):
        try:
            
            return reduce( prm, stack )
        except:
            return 0
            
    a, b = str[0], str[1:]
    # if it's a constant, stick it on the stack
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
            # default value is 0 if there's nothing on the stack
            x = 0.
        if a == "l":
            try:
                stack.append( log(x) )
            except ValueError:
                # can't log non-positive numbers: define this to be 0.
                stack.append(0.)
        
        else:
            try:
                y = stack.pop()
            except IndexError:
                # default to 0
                y = 0.
            if a == "*":
                stack.append(x * y)
            elif a == "^":
                try:
                    stack.append(x ** y)
                except OverflowError:
                    # handle enormous numbers by saying they're 0.
                    stack.append(0.)
                except ZeroDivisionError:
                    # handle e.g. (0)**(-1) 
                    stack.append(0.)
                except ValueError:
                    # handle e.g. (-1)**(1/2)
                    stack.append(0.)
            elif a == "/":
                try:
                    stack.append(x / y)
                except ZeroDivisionError:
                    # handle div by zero
                    stack.append(0.)
            elif a == "+":
                stack.append(x + y)
            elif a == "-":
                stack.append(x - y)
    return handleString(b, stack, verbose = verbose)

def scoreString( str ):
    x = handleString( str, [] )
    # how far from nearest integer...
    score = min( abs(x - floor(x)), abs(x - ceil(x)))
    if score == 0:
        # but ACTUAL integers are really bad!
        score = 0.5
    return (score, x)
     
     
# GA operations
def combine( str1, str2 ):
    # crossover two genomes at random cut-points
    x1 = choice(range(len(str1)))
    x2 = choice(range(len(str2)))
    return( str1[:x1] + str2[x2:], str2[:x2] + str1[x2:] )

def mutate( str ):
    # change one character in a genome
    x = choice(range(len(str)))
    return str[:x] + randomChar() + str[x+1:]

def randomChar():
    return choice("0123456789epl*/+-^")


def randomString(p = 0.1):
    out = randomChar()
    while random() > p:
        out += randomChar()
    return out

def removeDuplicates( pop ):
    s = frozenset(pop)
    return list(s)

def rankPop( pop ):
    pop = removeDuplicates(pop)
    out = [ (scoreString(p), p) for p in pop ]
    # a bit ugly, that - nested tuples. Should make objects like a grown-up.
    out.sort()
    
    return out
        

def doGA( npop = 100, rep = 0.1, mut = 0.1, xthresh =0.8, nav = 10 ):
    # create population
    pop = [ randomString(1./nav) for i in range(npop) ]
    gen = 0
    while True:
        print "**** %d ****" % gen
        
        gen += 1
        
        pr = rankPop(pop)
        print "Population: %d" % len(pr) 

        
        #**** diagnostic printing
        
        print handleString(pr[0][1], [], True) # just to see what the best one's doing

        # print top ten
        for i in range(10):
            print pr[i]

        #****

        pop = [] # for next generation
        
        j = 0
        torep = ceil(rep * len(pr))
        tomut = ceil(mut * len(pr))
        xt = int(ceil(xthresh * len(pr)))
        k = 0 
        while k < min([torep, tomut]):
            i = pr[k]
            if (k < torep):
                # replicate the right proportion of the population
                pop.append(i[1])
            if (k < tomut):
                # mutate the right proportion of the population
                pop.append(mutate(i[1]))
            k += 1

        while len(pop) < npop:
            i1 = choice(range(xt))
            i2 = choice(range(xt))
            x = combine(pr[i1][1], pr[i2][1])
            pop.append(x[0])
            pop.append(x[1])
        raw_input()
doGA()


#TODO: find way to kill numerical errors (
