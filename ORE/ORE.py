from string import digits, ascii_lowercase, ascii_uppercase
import random
import bitstring as bit
from hmac import hmac
from Crypto.Cipher import AES
from CriptareAES import CriptareAES


class ORE:
    def __init__(self, parametru = 256):
        self.M = 10
        self.size = parametru
        self.sk = bin(random.getrandbits(parametru))
        self.aes_key = self.getRandomString( self.size / 8)
        self.aes = CriptareAES(blocksize = self.size, key = self.aes_key)

    def enc(self, m):
        b = str(bin(m)[2:])
        n = len(b)
        F = hmac()
        u = ""
        for i in range(1, n + 1):
            bi = bit.BitArray( bin = b[:i-1] + "0" * (n - i))
            u += str(((long(F.calc(self.sk, bin(int(bi.bin))).hex, 16) % self.M) + long(b[i-1], 2)) % self.M )

        criptare = self.aes.Encrypt( str( m ) )
        nr_biti = self.aes.Encrypt( str(n) )
        plus_criptare = u + str(criptare) + str(nr_biti)

        return plus_criptare

    def compare(self, u1, u2):
        nr_biti = int(self.aes.Decrypt(u1[-16:]))
        u1 = u1[0:nr_biti]
        nr_biti = int(self.aes.Decrypt(u2[-16:]))
        u2 = u2[:nr_biti]

        if len(u1) > len(u2):
            return False
        if len(u1) < len(u2):
            return True
        for i in range(min(len(u1), len(u2))):
            if u1[i] != u2[i]:
                #print long(u2[i]), (long(u1[i]))
                if long(u2[i]) == (long(u1[i]) + 1) % self.M:
                    return True
                else:
                    return False
        return False

    def decriptare(self, ct):
        nr_biti = self.aes.Decrypt( ct[ -16 :])
        m = self.aes.Decrypt( ct[ int(nr_biti) : -16] )

        return m

    def getRandomString(self, keysize):
        elemente = digits + ascii_lowercase + ascii_uppercase
        return "".join(random.choice(elemente) for x in range(keysize))


o = ORE()
print o.decriptare(o.enc(15088770550637226586391483680012202207942527896584155924087419357405971711661120801642161053882433265175346929267745470562535654906902609520756636224102531534435489415414600549033589898234938443649502165551917653954606409286711276419563442388678929371228660382365025298576616712390433753234979984887286072276243464665631528173659434952630993514465787750694464705049283061848394052622459987117801190068251225921385203440204810772999785006593528459711096086173364960827886155609740722417870283456585752522492656114693305899611334177550903637433789937380262755612228255475134965108778535164275996707628965202997754297580))

print o.compare(o.enc(1000), o.enc(2003))