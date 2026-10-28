import base64, gzip, sys, os
# Simple Python packer/obfuscator

def main():
    if sys.platform == 'win32':
        os.system('cls')
    else:
        os.system('clear')
    
    if len(sys.argv) != 3:
        sys.exit(f"\r\n Syntax: python3 {sys.argv[0]} <input_path> <output_path>\r\n")
        
    #read file
    try:
        with open(sys.argv[1], 'r') as file:
            original_code = file.read()
    except Exception as e:
        sys.exit(e)
    
    #compress using g-zip
    compressed = gzip.compress(original_code.encode('utf-8'))
    
    #encode using base-64
    encoded = base64.b64encode(compressed).decode('utf-8')
    
    #build obfuscated script
    obfuscated = f"""import base64, gzip\r\nexec(gzip.decompress(base64.b64decode("{encoded}")))\r\n"""

    try:
        with open(sys.argv[2], 'w') as file:
            file.write(obfuscated)
    except Exception as e:
        sys.exit(e)
    
    sys.exit('\r\nOperation complete!\r\n')

if __name__ == "__main__":
    main()
