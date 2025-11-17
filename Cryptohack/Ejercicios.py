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
#cnJzKptojwWrHvu7j4Sdyodgp4Poqz5Z5v5Jp97w=
