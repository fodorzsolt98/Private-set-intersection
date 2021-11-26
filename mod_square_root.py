def power(x, y, p):
    res = 1
    x = x % p

    while (y > 0):

        if (y & 1):
            res = (res * x) % p

        y = y >> 1
        x = (x * x) % p

    return res

def square_root(n, p):
    if (p % 4 != 3):
        #print("Invalid Input")
        return -1

    n = n % p
    x = power(n, (p + 1) // 4, p)
    if ((x * x) % p == n):
        #print("Square root is ", x)
        return x

    x = p - x
    if ((x * x) % p == n):
        #print("Square root is ", x)
        return x

    #print("Square root doesn't exist ")
    return -1
