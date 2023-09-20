import binascii


def join_64bits(text):
    crypted_text = 0
    for i in reversed(range(len(text))):
        crypted_text |= text[i]
        if i != 0:
            crypted_text = crypted_text << 64
    return crypted_text

def hexToUtf8(text):
    text = binascii.unhexlify(text).decode('utf8')
    text = text.replace('\x00', '')
    return text


def utf8ToHexBytes(text):
    text = binascii.hexlify(text.encode('utf8')).decode('utf8')
    return text


def intToHex(int):
    return hex(int)[2:]


def file_read(path):
    with open(path, "r") as f:
        text = f.read()
    return text


def file_write(path, text):
    with open(path, "w") as f:
        print(text, file=f)


def gen_key(key,type):

    if type=="e":
        keys = list()
        for i in range(8):
            keys.append((key >> (32 * i)) & 0xFFFFFFFF)
        finkeys=list()
        for i in range(24):
            finkeys.append(keys[i%8])
        for i in range(7,-1,-1):
            finkeys.append(keys[i%8])
        print("finkeys",finkeys)
        return finkeys
    elif type=="d":
        keys = list()
        for i in range(8):
            keys.append((key >> (32 * i)) & 0xFFFFFFFF)
        print("keys",keys)
        finkeys = list()
        for i in range(8):
            finkeys.append(keys[i % 8])
        for i in range(31, 7, -1):
            finkeys.append(keys[i % 8])
        print("fink",finkeys)
        return finkeys
# def encrypt_round(left_part, right_part, round_key):
#     return right_part, left_part ^ feistel_cipher_round(right_part, round_key)


def function(left_subblock, subkey):
    temp = left_subblock ^ subkey

    sbox = [
        [4, 10, 9, 2, 13, 8, 0, 14, 6, 11, 1, 12, 7, 15, 5, 3],
        [14, 11, 4, 12, 6, 13, 15, 10, 2, 3, 8, 1, 0, 7, 5, 9],
        [5, 8, 1, 13, 10, 3, 4, 2, 14, 15, 12, 7, 6, 0, 9, 11],
        [7, 13, 10, 1, 0, 8, 9, 15, 14, 4, 6, 12, 11, 2, 5, 3],
        [6, 12, 7, 1, 5, 15, 13, 8, 4, 10, 9, 14, 0, 3, 11, 2],
        [4, 11, 10, 0, 7, 2, 1, 13, 3, 6, 8, 5, 9, 12, 15, 14],
        [13, 11, 4, 1, 3, 15, 5, 9, 0, 10, 14, 7, 6, 8, 2, 12],
        [1, 15, 13, 0, 5, 7, 10, 4, 9, 2, 3, 14, 6, 11, 8, 12],
    ]


    ss = []
    result = 0
    for i in range(8):
        result |= ((sbox[i][(temp >> (4 * i)) & 0b1111]) << (4 * i))

    # TODO:check order

    mask = (1 << 32) - 1
    result = (((result >> 11) | (result << (32 - 11)))) & mask

    return result
