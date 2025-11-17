#Ejercicio1
print("crypto{y0ur_f1rst_fl4g}")

#Ejercicio2

import sys
# import this

if sys.version_info.major == 2:
    print("You are running Python 2, which is no longer supported. Please update to Python 3.")

ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]

print("Here is your flag:")
print("".join(chr(o ^ 0x32) for o in ords))

#crypto{z3n_0f_pyth0n}

#Ejercicio3
nums = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95, 112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

flag = "".join(chr(n) for n in nums)

print(flag)
#crypto{ASCII_pr1nt4bl3}


#Ejercicio4
hex_string = "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"

flag = bytes.fromhex(hex_string).decode()

print(flag)
#crypto{You_will_be_working_with_hex_strings_a_lot}


#Ejercicio5
import base64

hex_string = "72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf"

b = bytes.fromhex(hex_string)
encoded = base64.b64encode(b)

print(encoded.decode())
#crypto/Base+64+Encoding+is+Web+Safe/

#Ejercicio6
# opción sin dependencias externas
n = 11515195063862318899931685488813747395775516287289682636499965282714637259206269

# calcular el número mínimo de bytes necesarios
length = (n.bit_length() + 7) // 8

# convertir a bytes (big-endian) y decodificar a string
msg_bytes = n.to_bytes(length, 'big')
flag = msg_bytes.decode()

print(flag)
#crypto{3nc0d1n6_4ll_7h3_w4y_d0wn}

#Ejercicio7

s = "label"
new = "".join(chr(ord(c) ^ 13) for c in s)
print("crypto{" + new + "}")

#crypto{aloha}

#Ejercicio8
KEY1 = bytes.fromhex("a6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313")
K2_xor_K1 = bytes.fromhex("37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e")
K2_xor_K3 = bytes.fromhex("c1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1")
FLAG_xor_all = bytes.fromhex("04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf")

# Recover KEY2  => KEY2 = (KEY2 ^ KEY1) ^ KEY1
KEY2 = bytes(a ^ b for a, b in zip(K2_xor_K1, KEY1))

# Recover KEY3  => KEY3 = KEY2 ^ (KEY2 ^ KEY3)
KEY3 = bytes(a ^ b for a, b in zip(KEY2, K2_xor_K3))

# Recover FLAG  => FLAG = FLAG ^ KEY1 ^ KEY2 ^ KEY3
FLAG = bytes(f ^ k1 ^ k2 ^ k3 for f, k1, k2, k3 in zip(FLAG_xor_all, KEY1, KEY2, KEY3))

print(FLAG.decode())
#crypto{x0r_i5_ass0c1at1v3}

#Ejercicio9
hex_data = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

data = bytes.fromhex(hex_data)

for key in range(256):
    decoded = bytes(b ^ key for b in data)
    try:
        text = decoded.decode()
        if "crypto" in text:  # buscar la flag
            print(f"Key: {key} -> {text}")
    except UnicodeDecodeError:
        continue

#crypto{0x10_15_my_f4v0ur173_by7e}


#Ejercicio10

cipher_hex = "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
cipher = bytes.fromhex(cipher_hex)

known = b"crypto{"

key = bytes([c ^ k for c, k in zip(cipher, known)])

full_key = (key * (len(cipher) // len(key) + 1))[:len(cipher)]

flag = bytes([c ^ k for c, k in zip(cipher, full_key)])

print(flag.decode())
#crypto{1f_y0u_Kn0w_En0uGH_y0u_Kn0w_1t_4ll}
