from __future__ import absolute_import, unicode_literals
from steganography.steganography import Steganography

def config_loader():
    global filepath, secret_message, output_filepath
    with open('StegBeetle_config.txt') as config_file:
        for i, line in enumerate(config_file):
            if i == 0:  # 1st line: filepath
                filepath = purify(line)
            elif i == 1:  # 2nd line: secret_message
                secret_message = purify(line)
            elif i == 2:  # 3rd line: output_path
                output_filepath = purify(line)
def purify(data):
    if "\n" in data:
        data = data[:-1]

    return data


filepath = ""
secret_message = ""
output_filepath = ""

config_loader()

write_data = Steganography.decode(filepath)

with open(output_filepath + '/StegBeetle_Discovered_Informaton.txt', 'w') as discover_info:
    discover_info.write(write_data)