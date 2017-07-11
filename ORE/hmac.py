from hashlib import sha256
import bitstring as bit

class hmac:
    def __init__(self, size=256):
        self.block_size = size
        self.ipad = bit.BitArray( hex = "0x5c" * (self.block_size / 8) )
        self.opad = bit.BitArray( hex = "0x36" * (self.block_size / 8) )
        #print len(self.ipad.hex), self.ipad.hex

    def calc(self, K, m):
        lungime_k = len(K) - 2

        if lungime_k > self.block_size:
            K_prim = bit.BitArray(hex = sha256(K).hexdigest())
        else:
            K_prim = bit.BitArray(bin = str(K[2:]) + "0"*(self.block_size - lungime_k))

        o_key_pad = K_prim.__ixor__(self.opad)
        i_key_pad = K_prim.__ixor__(self.ipad)

        i_key_pad_mesage = bin(int(i_key_pad.bin + str(m[2:]), 2))

        hash_i_key_pad_message = bit.BitArray ( hex = sha256(i_key_pad_mesage).hexdigest())

        h = bit.BitArray( hex = sha256( bin(int( o_key_pad.bin + hash_i_key_pad_message.bin, 2))).hexdigest() )

        return h

