def file_to_array(filename):
    with open(filename, 'rb') as file:
        byte_array = file.read()
    return byte_array

def generate_cpp_array(filename, var_name):
    byte_array = file_to_array(filename)
    array_str = ', '.join(f'0x{byte:02X}' for byte in byte_array)
    return f'#define {var_name}_len {len(byte_array)}\n' \
           f'const uint8_t {var_name}[] = {{\n  {array_str}\n}};'

filename = 'index_ov2640.html.gz'
var_name = 'index_ov2640_html_gz'
cpp_array = generate_cpp_array(filename, var_name)

with open(f'{var_name}.h', 'w') as header_file:
    header_file.write(cpp_array)

print(f'Arquivo {var_name}.h gerado com sucesso!')