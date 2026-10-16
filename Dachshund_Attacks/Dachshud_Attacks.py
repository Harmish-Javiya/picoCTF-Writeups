from Crypto.Util.number import long_to_bytes
import math

e = 24117972953890808468080488544319919501796946197879731376477033404217655422744670279944382711189123782125482697700918853782814943329393006798541106135852403435755243105749267423333431406309768720178826598668470995399845213579354190577712846891934370108393663155046214233903385957394536917539375943723642657881
N=105215126605452031419034709177213584868039607539947635120148949717385546370738259041944431629257547120581861402965140300280399367843971871929869190362900409125202642062338085653604059392250344388797269121665400723783608381603416816311280739883603480065392118567078240120382465550840997547292771556483669682737
c=77567778307615250182341446878205200423717479613145014154832550441405764010481510352333691833673095778068731236429531677489261635836262990949548971595030301195079452196746750363251551223143337018752325618767188949239948247878691960620149208922785024005049489330949512694485528481599660875556775210334809383235


# -------- Continued Fraction --------
def continued_fraction(n, d):
    cf = []
    while d:
        q = n // d
        cf.append(q)
        n, d = d, n - q * d
    return cf


# -------- Convergents --------
def get_convergences(e, N):
    cf = continued_fraction(e, N)
    convergences = []

    for i in range(len(cf)):
        num, den = 1, 0
        for q in reversed(cf[:i+1]):
            num, den = den + num * q, num
        convergences.append((num, den))

    return convergences


# -------- Perfect square check --------
def is_perfect_square(n):
    if n < 0:
        return -1
    root = int(math.isqrt(n))
    if root * root == n:
        return root
    return -1


# -------- Factorisation --------
def factorises(N, e, k, d):
    if k == 0:
        return None

    if d % 2 == 0:
        return None

    if (e * d - 1) % k != 0:
        return None

    phi = (e * d - 1) // k

    # quadratic: x^2 - (N - phi + 1)x + N = 0
    b = N - phi + 1
    discr = b * b - 4 * N

    if discr >= 0:
        sq = is_perfect_square(discr)
        if sq != -1:
            p = (b + sq) // 2
            q = (b - sq) // 2
            return (p, q)

    return None


# -------- Main Attack --------
for k, d in get_convergences(e, N):
    factors = factorises(N, e, k, d)

    if factors:
        p, q = factors

        if p * q == N:
            phi = (p - 1) * (q - 1)

            # modular inverse
            d = pow(e, -1, phi)

            m = pow(c, d, N)
            print(long_to_bytes(m))
            break
