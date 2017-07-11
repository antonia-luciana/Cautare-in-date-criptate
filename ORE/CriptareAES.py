from Crypto.Cipher import AES

def XOR(string1, string2):
    """zip intoarce o lista de tuple (s1,s2)
    se itereaza prin lista si face xor (^) pe elementele fiecarei perechi
    functia intoarce stringul rezultat"""
    return "".join(chr(ord(s1) ^ ord(s2)) for s1, s2 in zip(string1, string2))

class CriptareAES:

    iv = "This is an iv456"

    def __init__(self, blocksize = 256, modValue="CBC", key="RandomKey1234567"):
        if blocksize in [128,192,256]:
            self.blocksize = blocksize/8
        elif blocksize in [16,24,32]:
            self.blocksize = blocksize
        else:
            raise ValueError("The blocksize is not correct!")
        if modValue=="ECB" or modValue=="ecb":
            self.mod = "ECB"
        elif modValue=="CBC" or modValue=="cbc":
            self.mod = "CBC"
        else:
            raise ValueError ("Mod de operare incorect! Va rugam introduceti ECB sau CBC!")
        self.aes = AES.new(key)

    def SetKey(self,key):
        self.aes = AES.new(key)

    def Pad(self,s):   # padding PKCS5
        return  s + (16 - len(s) % 16) * chr(16 - len(s) % 16)


    def Unpad(self,s):
        return s[0:-ord(s[-1])]

    def EncryptECB(self,text):
        blocks = CriptareAES.GetBlocks(self,text)
        cipher_text = ""
        for block in blocks:
            if (len(block)==16):
                cipher_text += self.aes.encrypt(block)
            else:
                padded_block = CriptareAES.Pad(self,block)
                cipher_text += self.aes.encrypt(padded_block)

        return cipher_text

    def DecryptECB(self,cipher_text):
        blocks = CriptareAES.GetBlocks(self,cipher_text)

        plain_text = ""
        for i in range(len(blocks)):
            plain_text += self.aes.decrypt(blocks[i])

        # depadare plaintext
        plain_text = CriptareAES.Unpad(self,plain_text)

        return plain_text

    def EncryptCBC(self,text):
        blocks = CriptareAES.GetBlocks(self,text)

        #primul bloc poate avea maxim 16 caractere
        if len(blocks[0])==16:
            cipher_block = self.aes.encrypt(XOR(blocks[0],self.iv));
            cipher_text = cipher_block
        else:
            padded_block = CriptareAES.Pad(self,blocks[0])
            cipher_block = self.aes.encrypt(XOR(padded_block,self.iv));
            cipher_text = cipher_block

        #daca avem mai mult de un bloc continuam decriptarea
        for i in  range(1,len(blocks)):
            if len(blocks[i]) == 16:
                cipher_block = self.aes.encrypt(XOR(cipher_block,blocks[i]))
            else:
                padded_block = CriptareAES.Pad(self,blocks[i])
                cipher_block = self.aes.encrypt(XOR(cipher_block,padded_block))
            cipher_text += cipher_block

        return cipher_text

    def DecryptCBC(self,cipher_text):
        #impartim in blocuri de criptotext
        blocks = CriptareAES.GetBlocks(self,cipher_text)

        #blocul initial de plaintext este obtinut prin decriptare si apoi XOR cu iv
        plain_text = XOR(self.aes.decrypt(blocks[0]),self.iv)

        # celelalte blocuri vor fi decriptate cu cheia data
        #apoi se face xor cu blocul de criptotext anterior
        for i in range(1,len(blocks)):
            plain_text += self.DecryptareBlockCBC(blocks[i-1],blocks[i])

        #depadare
        #if len(blocks) > 1:
        plain_text = CriptareAES.Unpad(self, plain_text)

        return plain_text

    def Encrypt(self,text):
        if self.mod == "ECB":
            return self.EncryptECB(text)
        if self.mod == "CBC":
            return self.EncryptCBC(text)

    def Decrypt(self, text):

        if self.mod == "ECB":
            return self.DecryptECB(text)
        if self.mod == "CBC":
            return self.DecryptCBC(text)

    def GetBlocks(self,text):
        return filter(None,[text[0 + i:16 + i] for i in range(0, len(text), 16)])

    def DecryptareBlockCBC(self,block1,block2):
        return XOR(self.aes.decrypt(block2),block1)


