import random
from CriptareAES import CriptareAES
from hashlib import md5, sha256
from bitstring import BitArray
from hmac import hmac
import re
import os

class ClientSong:
    def __init__(self, nume):
        self.nume = nume
        if not os.path.exists(self.nume):
            os.makedirs(self.nume)

        key_file = self.nume + "//" + "MasterKey.txt"
        if not os.path.isfile(key_file) :
            with open(key_file, "w") as f:
                self.__MasterKey = bin(random.getrandbits(256))
                f.write(self.__MasterKey)
                f.close()
        else:
            with open(key_file) as f:
                self.__MasterKey = self.toBin(f.read()[2:])
                f.close()

        self.E = CriptareAES()
        self.F = hmac()

    def simetric_enc(self, W):
        W = self.toBites(W)

        if len(W) > 16:
            cript = self.E.Encrypt(W)
            cript_bit = self.toBites(cript)
            res = BitArray(bin = cript_bit)
        else:
            res = BitArray(bin=self.toBites(self.E.Encrypt("0" * 128 + W)))

        return res

    def getKey(self, X):
        L = X.bin[:-128]
        k = self.F.calc(self.__MasterKey, self.toBin(L))

        return k

    def toStr(self, X):

        for x in X:
            if x != "1" and x != "0":
                X = X.replace(x, '')
        res = ""
        i = 0
        while i < len(X):
            res += chr(int(X[i : i+8], 2))
            i += 8
        res.replace(' ','')


        return res

    def curata_str(self, res):

        for i in range(len(res)):
            if ord(res[i]) > 126 or ord(res[i])<33:
                res = res.replace(res[i], '')

        return res


    def enc(self, W, seed):

        X = self.simetric_enc(W)

        L = X.bin[:-128]
        R = X.bin[-128:]

        len_S = len(X.bin[:-128])

        random.seed(seed)
        bin_S = bin(random.getrandbits(len_S))[2:]
        S = BitArray(bin = "0"*(len_S - len(bin_S)) + bin_S ).bin

        k = self.getKey(X)

        key = self.toBin(BitArray(k).bin)

        Fk = BitArray(hex = md5( self.F.calc(key, S).hex ).hexdigest())

        SFk  = BitArray(bin= str(S) + Fk.bin)
        c = SFk.__xor__(X)

        return C

    def toBites(self, word):

        b = bytearray()
        b.extend(word)
        binary_str = ""

        for i in range(len(b)):
            binary_repr = bin(b[i])[2:]
            binary_str += "0" * (8-len(binary_repr)) + binary_repr

        return binary_str

    def toBin(self, str):  #string to binary
        return bin(long(str))

    def sendFiles(self, admin, *files):

        for file in files:
            if "/" not in file:
                file = self.nume + "//" + file

            with open(file) as f:
                words = f.read()
                words = re.sub(r'[^\w\s]', '', words)
                words = words.split(" ")
                filter(None, words)


            #dot_index = file.index(".")
            #out_file = file[:dot_index]+ "_" + file[dot_index:]
            out_file = file.replace(self.nume, admin)
            isFirst = True
            with open(out_file, "w") as fout:
                for i in range(len(words)):
                    if isFirst:
                        isFirst = False
                        seed = file
                    else:
                        seed = words[i-1]
                        #seed = file
                    if len(words[i]) > 2:
                        fout.write(self.enc(words[i], seed).hex + "\n")
                    elif len(words[i])==2:
                        fout.write(self.enc(words[i] + " ", seed).hex + "\n")
                    else:
                        fout.write(" " + self.enc(words[i] + " ", seed).hex + "\n")
                fout.close()

            os.remove(file)


    def dec(self, C, seed):

        if type(C) is not BitArray("0"):
            C = BitArray(hex = C)

        random.seed(seed)
        len_S = len(C[:-128])
        #S = BitArray(bin = str(bin(random.getrandbits(len(C[:-128]))))[2:])
        bin_S = bin(random.getrandbits(len_S))[2:]
        S = BitArray(bin="0" * (len_S - len(bin_S)) + bin_S)

        CL = BitArray( bin = C.bin[:-128] )
        CR = BitArray( bin = C.bin[-128:] )


        L = (S.__xor__(CL)).bin

        k = self.F.calc(self.__MasterKey, self.toBin(L))

        key = self.toBin( BitArray( k ).bin )

        Fk = BitArray( hex = md5(self.F.calc(key, S.bin).hex).hexdigest() )

        R = (Fk.__xor__(CR)).bin

        X = L + R

        res = self.curata_str(self.toStr(self.E.Decrypt(self.toStr(X))))

        return res

    def Trapdoor(self, word):
        X = self.simetric_enc(word)
        k = self.getKey(self.simetric_enc(word)).bin

        return  (X, k)

    def getWords(self, filename):
        if "/" not in filename:
            filename = self.nume + "//" + file
        with open(filename) as f:
            words = f.read()
            words = words.split('\n')
            words = filter(None, words)

        return words

    def Dec_file(self, file):
        if "/" not in file:
            file = self.nume + "//" + file

        file_out = file.replace("_.",".")
        #os.rename(file, file_out)

        words = self.getWords(file)

        first = True
        with open(file,'w') as f:
            for word in words:
                if first:
                    seed = file
                    first = False
                else:
                    seed = last_word

                last_word = self.dec(word, seed)
                f.write(last_word + " ")



