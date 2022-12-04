import random


def rand_codeword(n):  # function to generate a random n length codeword

    word = ""
    for i in range(n):
        # give 0 or 1 as the ith bit in the codeword
        temp = str(random.randint(0, 1))
        word += temp
    return word                             # n length codeword


def BSC(x, p):                               # simulate the output of BSC channel
    y = ""
    for i in range(len(x)):
        # generate a float b/w 0 and 1; if it is <= P(bitflip) then bitflip occurs
        check = random.random()
        if check <= p:
            if x[i] == "1":                 # bitflip
                y += "0"
            else:
                y += "1"
        else:
            y += x[i]                       # no bitflip
    return y


# Driver code starts here

f = open("Results.txt", 'w')

for i in range(6):
    # parameters
    N = 2000

    n = int(input("n = "))
    f.write("n = ")
    f.write(str(n))
    f.write("\n")
    k = int(input("k = "))
    f.write("k = ")
    f.write(str(k))
    f.write("\n")
    p = float(input("p = "))
    f.write("p = ")
    f.write(str(p))
    f.write("\n")

    codeword_list = set()                       # set to store 2^k random codewords
    # set ensures that there is no duplication
    while len(codeword_list) < pow(2, k):
        word = rand_codeword(n)
    # generate 2^k random n length codewords and store them in the set
        codeword_list.add(word)

    Len = len(codeword_list)                    # cardinality of code C = 2^k
    pOfEmin = 1
    for c in  range (5):
        E = 0
        for i in range(N):
            # pick a random codeword from the set as input to BSC
            ip = random.choice(tuple(codeword_list))
            y = BSC(ip, p)                               # y is output of BSC

            j = 0
            min = n                                     # variable to track minimun Hamming distance
            word = ""                                   # codeword with minimum Hamming distance
            for j in codeword_list:
                dist = 0                                # initialising distance to be 0
                for k in range(n):
                    if y[k] != j[k]:
                        dist += 1                         # incrementing distance when flipped bit is found
                if dist < min:                            # updating min Hamming distance and estimate
                    min = dist
                    # word is the estimate; if it is not equal to the input, then E is incremented
                    word = j
            if word != ip:
                E += 1

        # No. of decoding errors
        f.write("E = ")
        f.write(str(E))
        f.write("\n")

        # P(error) for a random code C and BSC with parameters (n, k, p)
        pOfE = E/N
        if pOfE < pOfEmin:
            pOfEmin = pOfE

        f.write("P(Error) = ")
        f.write(str(pOfE))
        f.write("\n")

    f.write("Minimum P(Error) = ")
    f.write(str(pOfEmin))
    f.write("\n\n")
