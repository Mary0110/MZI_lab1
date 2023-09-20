import sys

from lib import *


def GOST_28147_89_GUM(text, key, keys, mode):
    result = []

    iv = 0x71EF0B1F3BE0394F
    iv = GOST_28147_89(iv, key, "e")

    C1 = 0x1010101
    C2 = 0x1010104

    N4 = iv >> 32 & 0xFFFFFFFF
    N3 = iv & 0xFFFFFFFF
    for t in text:
        N4 = (N4 + C2) & 0xFFFFFFFF
        N3 = ((N3 + C1 - 1) % 0xFFFFFFFF) + 1

        N1 = N3
        N2 = N4

        N = (N2 << 32) | N1
        gamma = GOST_28147_89(N, key, "e")
        result.append(t ^ gamma)
    return join_64bits(result)


def GOST_28147_89(text_int, key, mode):
    temp = 0
    print(((bin(text_int))))

    if len(hex(text_int)[2:]) % 16 > 0:
        temp = 1

    text_int = [(text_int >> (64 * i)) & 0xFFFFFFFFFFFFFFFF for i in range(len(hex(text_int)) // 16 + temp)]
    if temp == 1:

        text_int[len(text_int) - 1] = text_int[len(text_int) - 1] << (64 - len(hex(text_int[len(text_int) - 1]) * 4))
    if mode =="d":
        if text_int[-1] == 0:
            text_int = text_int[0:-2]
            print(text_int)
    for i in range(len(text_int)):
        print("la",  len(bin(text_int[i])), "temp", temp, bin(text_int[i]),mode)

    keys = gen_key(key, mode)

    final_result = []
    for i in range(len(text_int)):
        left_subblock = text_int[i] >> 32
        right_subblock = text_int[i] & 0xFFFFFFFF
        for i in range(32):
            if mode == "e":
                a =  function(right_subblock, keys[i])
                left_subblock, right_subblock = right_subblock,  function(right_subblock, keys[i]) ^ left_subblock
            else:
                left_subblock, right_subblock = right_subblock ^ function(left_subblock, keys[i]), left_subblock

        Tsh = ((left_subblock << 32) | right_subblock)
        final_result.append(Tsh)
    return join_64bits(final_result)


def encrypt_file(file_name, encrypted_file_name, key):
    with open(file_name, "r", encoding='utf-8') as read_file:
        lines = read_file.readlines()

    with open(encrypted_file_name, 'w', encoding='utf-8') as write_file:
        for line in lines:
            line_to_encrypt = int(utf8ToHexBytes(line), 16)
            crypted_line = str(GOST_28147_89(line_to_encrypt, key, "e"))
            write_file.write((crypted_line) + '\n')


def decrypt_file(encrypted_file_name, decrypted_file_name, key):
    with open(encrypted_file_name, "r",encoding='utf-8') as read_file:
        lines = read_file.readlines()

    with open(decrypted_file_name, "w",encoding='utf-8') as write_file:
        for line in lines:
            line_to_decrypt = int(line.removesuffix('\n'))
            # print("line", key)
            decrypted_line = (GOST_28147_89(line_to_decrypt, key, "d"))
            print("decrypt final", len(str(bin(int(decrypted_line)))), bin(int(decrypted_line)))

            decrypted_line = intToHex(decrypted_line)
            # print("bin", str(bin(int(decrypted_line))))
            write_file.write(hexToUtf8(decrypted_line))


def main():
    fileName = "Text.txt"
    encryptFileName = fileName + "_encrypt"
    decryptFileName = fileName + "_decrypt"
    key = 0x287fc759c1ad6b59ac8597159602217e9a03381dcd943c4719dcca000fb2b577
    encrypt_file(fileName, encryptFileName, key)
    decrypt_file(encryptFileName, decryptFileName, key)


if __name__ == '__main__':
    main()
