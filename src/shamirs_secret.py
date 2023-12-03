from random import SystemRandom
from fractions import Fraction

rng = SystemRandom()

MAX_POLYNOMIAL_COEFFIECIENT = 2**256  # 2^256
MAX_X_VALUE = 2**256  # 2^256


class Shamirs_secret_sharing_setup():
    """ Shamirs secret sharing
    Split a secret value into as many shares as you want
    min_shares shares can be used to reconstruct said secret
    """

    def __init__(self, min_shares, secret):
        self.shares = 0
        self.min_shares = min_shares
        self.secret = secret
        # ordered x^0 , x^1, ...
        self.poly_coefficients = self.__create_polynomial(self.min_shares - 1)

    def __random_coefficient(self):
        return rng.randint(0, MAX_POLYNOMIAL_COEFFIECIENT)

    def __create_polynomial(self, degree):
        coefficients = []
        coefficients.append(self.secret)
        for i in range(degree):
            coefficients.append(self.__random_coefficient())
        return coefficients

    def __evaluate_poly(self, x):
        y = 0
        for i in range(len(self.poly_coefficients)):
            y += self.poly_coefficients[i] * x**i
        return y

    def create_share(self):
        """Creates a share
        share - a point (x,y) formatted as a tuple
        using min_shares shares the secret can be reconstructed
        Returns: 
            share : (x, y)
        """
        x = rng.randint(0, MAX_X_VALUE)
        y = self.__evaluate_poly(x)
        self.shares += 1
        return (x, y)


def lagrange_basis_poly(j, xeval, X):
    """ 
    https://en.wikipedia.org/wiki/Lagrange_polynomial
    Args:
        j (int): (index of x in X to be left out)
        xeval (number): x value to evaluate the lagrange polynomial (0 for shamirs secret sharing)
        X (List<number>) : x values to be interpolated
    Returns: 
        Fraction : returns the jth lagrange polynomial of X evaluated at x
    """
    basis_poly = 1
    for i in range(len(X)):
        if j != i:
            basis_poly *= Fraction(xeval - X[i], (X[j] - X[i]))
    return basis_poly


def reconstruct_shamirs_secret(shares):
    """ Reconstructs shamir's secret
    Uses lagrange interpolation to create a polynomial f() from shares
    evaluates shamirs secret at f(0)
    share - a point (x,y) formatted as a tuple
    # TODO potential speedup from another form of interpolation
    Args:
        shares (list<share>): list of shares (x,y) to be interpolated
    Returns:
        int: Shamir's secret
    """
    X = []
    for x, _ in shares:
        X.append(x)
    
    # lagrange interpolation
    shamirs_secret = 0
    for i in range(len(shares)):
        _, yi = shares[i]
        basis_poly_i = lagrange_basis_poly(i, 0, X)
        shamirs_secret += yi * basis_poly_i
    return shamirs_secret
