from binascii import unhexlify

def _write_int(i, width=4):
    return unhexlify(hex(i)[2:].rjust(width, '0'))


def _write_indices(*indices):
    result = bytes()
    for index in indices:
        result += _write_int(index)
    return result


def write_CONSTANT_Utf8(s):
    return unhexlify("01") + _write_int(len(s)) + bytes(s.encode())


def write_CONSTANT_Class(index):
    return unhexlify("07") + _write_indices(index)


def write_CONSTANT_String(index):
    return unhexlify("08") + _write_indices(index)


def write_CONSTANT_Fieldref(index1, index2):
    return unhexlify("09") + _write_indices(index1, index2)


def write_CONSTANT_NameAndType(index1, index2):
    return unhexlify("0C") + _write_indices(index1, index2)


def write_CONSTANT_Methodref(index1, index2):
    return unhexlify("0A") + _write_indices(index1, index2)


def write_constant_pool(data):
    pool = {}
    # this_class
    pool[1] = write_CONSTANT_Class(2)
    pool[2] = write_CONSTANT_Utf8("PythonSample")
    # super_class
    pool[3] = write_CONSTANT_Class(4)
    pool[4] = write_CONSTANT_Utf8("java/lang/Object")
    # constructor from Object
    pool[5] = write_CONSTANT_Methodref(3, 6)
    pool[6] = write_CONSTANT_NameAndType(7, 8)
    pool[7] = write_CONSTANT_Utf8("<init>")
    pool[8] = write_CONSTANT_Utf8("()V")
    # Code attribute
    pool[9] = write_CONSTANT_Utf8("Code")
    return pool


def write_class_data(data, pool, f):
    pass


def generate_byte_code(data, filename):
    with open(filename, 'wb') as f:
        f.write(unhexlify("CAFEBABE"))
        f.write(unhexlify("0000"))
        f.write(unhexlify("0032")) # Java 6
        pool = write_constant_pool(data)
        f.write(_write_int(len(pool) + 1))
        for key in sorted(pool.keys()):
            f.write(pool[key])
        f.write(unhexlify("0021")) # access_flags
        f.write(unhexlify("0001")) # this_class
        f.write(unhexlify("0003")) # super_class
        f.write(unhexlify("0000")) # interfaces_count
        f.write(unhexlify("0000")) # fields_count
        f.write(unhexlify("0001")) # method_count
        # constructor from Object
        f.write(unhexlify("0001")) # method access_flags
        f.write(unhexlify("0007")) # method name_index
        f.write(unhexlify("0008")) # method descriptor_index
        f.write(unhexlify("0001")) # method attributes_count
        # Code attribute for constructor
        f.write(unhexlify("0009")) # attribute_name_index
        f.write(unhexlify("00000011")) # attribute_length
        f.write(unhexlify("0001")) # max_stack
        f.write(unhexlify("0001")) # max_locals
        f.write(unhexlify("00000005")) # code_length
        f.write(unhexlify("2AB70005B1")) # code
        f.write(unhexlify("0000")) # exception_table_length
        f.write(unhexlify("0000")) # attribute_count
        # attributes
        f.write(unhexlify("0000")) # attribute_count
