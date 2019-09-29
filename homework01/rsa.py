from typing import Tuple
import random


def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True
    pass


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)

    while g != 1:
        e = random.randrange(1, phi)
    g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while a * b != 0:
        if a > b:
            a %= b
        else:
            b %= a
    return a + b
    pass


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    r0 = e % phi
    a0 = 1
    b0 = -(e // phi)

    r1 = phi % r0
    a1 = -(phi // r0)
    b1 = 1 + (e // phi) * (phi // r0)
    r2 = -1

    if r1 == 0:
        return r0

    while r2 != 0:
        a2 = a0 - a1 * (r0 // r1)
        b2 = b0 - b1 * (r0 // r1)
        r2 = a2 * e + b2 * phi
<<<<<<< HEAD
        
=======

>>>>>>> feature/rsa_new
        r0 = r1
        r1 = r2
        a0 = a1
        a1 = a2
        b0 = b1
        b1 = b2

    if a0 < 0:
        a0 += phi * (abs(a0) // phi + 1)
    return a0
    pass
