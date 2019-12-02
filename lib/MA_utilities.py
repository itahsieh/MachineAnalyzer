class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def bytes_xor(bytes_array):
    checksum = b'\x00'
    for i in range(len(bytes_array)):
        checksum = chr(ord(checksum) ^ ord(bytes_array[i]))
    return checksum

def floatbytes_xor(floatbytes_array):
    n_bytes = len(floatbytes_array)
    assert( n_bytes % 4 == 0 )

    checksum_list = list(str(b'\x00') * 4)
    for i in range(n_bytes/4):
        idx = 4 * i
        for j in range(4):
            checksum_list[j] = chr( ord(checksum_list[j]) ^ ord(floatbytes_array[idx+j]) )
    
    checksum = b''
    for j in range(4):
        checksum += checksum_list[j]
    return checksum
