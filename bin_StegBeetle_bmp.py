from __future__ import absolute_import, unicode_literals
from steganography.steganography import Steganography
from random import *

def config_loader():
    global filepath, secret_message, output_filepath
    with open('StegBeetle_config.txt') as config_file:
        for i, line in enumerate(config_file):
            if i == 0:  # 1st line: filepath
                filepath = purify(line)
            elif i == 1:  # 2nd line: secret_message
                secret_message = purify(line)
            elif i == 2:  # 3rd line: output_path
                output_filepath = purify(line) + '/stegged-jpg-image-'+str(randint(0,100000))+'.bmp'

def purify(data):
    if "\n" in data:
        data = data[:-1]
    return data

filepath = ""
secret_message = ""
output_filepath = ""

config_loader()

#filepath = purify(filepath)
#secret_message = purify(secret_message)
#output = purify(output_filepath)

Steganography.encode(filepath, output_filepath, secret_message)