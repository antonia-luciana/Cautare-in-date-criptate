import random
from CriptareAES import CriptareAES
from hashlib import md5, sha256
from bitstring import BitArray
from hmac import hmac
import shutil
import os

class AdminSong:
    def __init__(self, nume):
        self.nume = nume
        if not os.path.exists(self.nume):
            os.makedirs(self.nume)
        self.F = hmac()

    def verify(self, C, X, k):

        k = self.toBin(k)
        if len(X) != len(C):
            return False
        SFk = C.__xor__(X).bin
        S = SFk[:-128]
        fk = self.F.calc(k, S).hex

        return ( SFk[-128:] == BitArray(hex = md5(fk).hexdigest()).bin)

    def getWords(self, filename):
        if "/" not in filename:
            filename = self.nume + "//" + file
        with open(filename) as f:
            words = f.read()
            words = words.split('\n')
            words = filter(None, words)

        return words

    def toBin(self, str):
        return bin(long(str))

    def toBites(self, word):
        b = bytearray()
        b.extend(word)
        binary_str = ""
        for i in range(len(b)):
            binary_repr = bin(b[i])[2:]
            binary_str += "0" * (8-len(binary_repr)) + binary_repr
        return binary_str

    def readWords(self, file):
        if "/" not in file:
            file = self.nume + "//" + file
        with open(file, 'r') as f:
            text = f.read()
            words = text.split('\n')
            words = filter(None, words)
            return words

    def verify_file(self, file, X, k):
        if "/" not in file:
            file = self.nume + "//" + file
        words = self.getWords(file)
        for C in words:
            if self.verify(BitArray(hex = C), X, k):
                return True
        return False

    def getFiles(self,client, X_and_k):
        for (dirpath, dirnames, filenames) in os.walk(self.nume):
            files = filenames
            break
        for file in files:
            if self.verify_file(file, X_and_k[0], X_and_k[1]):
                dot_index = file.index(".")
                file_out = file[:dot_index-1] + file[dot_index:]
                shutil.copy(self.nume + "//" + file, client)




