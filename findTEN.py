import time
import string

def loopTen(num):
    while(len(str(num)) > 9):
        tenDigitNum = int(str(num)[:10])
        num = num % (10 ** (len(str(num)) - 1))
        if(is_Prime(tenDigitNum)):
            return num, tenDigitNum
    return num, -1

# Taken from: https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test#Python
#####################################################################################
def _try_composite(a, d, n, s):
    if pow(a, d, n) == 1:
        return False
    for i in range(s):
        if pow(a, 2**i * d, n) == n-1:
            return False
    return True # n  is definitely composite

def is_Prime(n, _precision_for_huge_n=16):
    if n in _known_primes:
        return True
    if any((n % p) == 0 for p in _known_primes) or n in (0, 1):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])

_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_Prime(x)]
######################################################################################

def FibMe(oldZero, oldOne): return oldOne, oldZero + oldOne

def CatMe(daCat, newFib):
    d = 10 ** len(str(newFib))
    daCat = (daCat * d) + newFib
    return daCat

def mod26(num):
    numElements = 5#int(len(str(num))/2)
    chrRay = ['a'] * numElements
    i = 0
    while(i < numElements):
        i1 = i * 2
        twoDnum = int(str(num)[i1:i1+2]) # Need to specify both indexes (single digit nums (eg 03)) cause issues otherwise
        charIndex = twoDnum % 26
        chrRay[i] = string.ascii_uppercase[charIndex]
        i += 1
    strOut = "".join(chrRay)
    return strOut

# Used soley to match English words.  In other words, scanned for 10-digit cyphers well before/after my presumed targets 
#   for things that maybe made sense (since what I did find did not)
# Requires txt file of words (presumed english)
# Driver code not in submission
def getWords():
    with open("dd.txt") as wordFile:
        daWords = wordFile.readlines()
    daWords = [x.strip() for x in daWords]
    da5words = []
    for w in daWords:
        if(len(w) == 5):
            da5words.append(w.upper())
    return da5words
wordFile = getWords()
start = time.perf_counter()

# Variables
first10Dprime = 2584418167
fibIndexZero = 0
fibIndexOne = 1
fibConcat = 1
primeCounter = 0
target1 = 44722 # What I found>> 2263772191(w/ repeats): WLZVN, 4700031773(no repeats): VADRV
target2 = 53215 # What I found>> 2675019371(w/ repeats): AXBPT, 2887676977(no repeats): CJPRZ
tenPs = [0] * target2 # Used to skip repeat 10 digit primes

print("=======================\tSTARTING THE FIB FUN\t=======================")
more = True
while more:
    fibIndexZero, fibIndexOne = FibMe(fibIndexZero, fibIndexOne)
    fibConcat = CatMe(fibConcat, fibIndexOne)
    current10P = 1
    while(current10P > 0):
        fibConcat, current10P = loopTen(fibConcat)
        if(current10P > 0):
            tenPs[primeCounter] = current10P
            primeCounter += 1
            if(primeCounter  == 1):
                print("First 10d prime should be: ", first10Dprime, 
                      "( ZGPDP )\tActual is: ", current10P, "(", mod26(current10P), ")")
            if(primeCounter == target1):
                print("target1: ", current10P,  "\tmod26(): ", mod26(current10P))
            if(primeCounter == target2):
                print("target2: ", current10P,  "\tmod26(): ", mod26(current10P))
                current10P = -1
                more = False
print((time.perf_counter() - start)/60, " minutes lapsed\t................End of line")
