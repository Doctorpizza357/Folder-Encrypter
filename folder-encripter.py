import time

import pyAesCrypt
from os import stat, remove
import sys
import os
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()

root.attributes('-topmost', True)
path = filedialog.askdirectory()

bufferSize = 64 * 3 * 1024
ACTION_ENCRYPT = 'encrypt'
ACTION_DECRYPT = 'decrypt'
encrypted_file_extenstion = ".PIZZA"

def get_normal_file_name(encrypted_filename):
    return encrypted_filename.replace(encrypted_file_extenstion, '')


def get_encrypted_file_name(normal_filename):
    return normal_filename + encrypted_file_extenstion


def encrypt_files_in_folder(action=ACTION_DECRYPT):
    for root, d_names, f_names in os.walk(path):
        for f in f_names:
            real_file_path = os.path.join(root, f)
            print("Processing " + str(real_file_path))
            if action == ACTION_ENCRYPT:
                encrypt(real_file_path)
            else:
                decrypt(real_file_path)


def check_if_encrypted(filename):
    if encrypted_file_extenstion in filename:
        return True
    else:
        return False


def encrypt(normal_filename):
    if check_if_encrypted(normal_filename):
        print("File is already encrypted")
        return
    with open(normal_filename, "rb") as fIn:
        with open(get_encrypted_file_name(normal_filename), "wb") as fOut:
            pyAesCrypt.encryptStream(fIn, fOut, password, bufferSize)
    remove(normal_filename)


def decrypt(encrypted_filename):
    if not check_if_encrypted(encrypted_filename):
        print("File is not Encrypted")
        return
    encFileSize = stat(encrypted_filename).st_size
    error = False
    with open(encrypted_filename, "rb") as fIn:
        try:
            with open(get_normal_file_name(encrypted_filename), "wb") as fOut:
                pyAesCrypt.decryptStream(fIn, fOut, password, bufferSize, encFileSize)
        except ValueError as e:
            print(e)
            error = True
    if not error:
        os.remove(encrypted_filename)
    else:
        remove(get_normal_file_name(encrypted_filename))


if __name__ == '__main__':
    start_time = time.time()
    action = input("Enter Action, 1 to encrypt 2 to decrypt\n")
    if int(action) == 1:
        ACTION = ACTION_ENCRYPT
    elif int(action) == 2:
        ACTION = ACTION_DECRYPT
    else:
        ACTION = None
        print("Invalid Action")
        sys.exit()
    print("Action Accepted")
    password = input("Enter new password for encryption and old password for decryption\n")
    encrypt_files_in_folder(ACTION)
    print(str(time.time() - start_time) + " Seconds elapsed")