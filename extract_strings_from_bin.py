import os, sys, re

def main():
    if len(sys.argv) != 3:
        sys.exit('\r\nUsage: <file-path> <output.txt>\r\n')

    if not os.path.exists(sys.argv[1]):
        sys.exit('\r\nError! File not found!\r\n')
        
    # open/read file
    try:
        with open(sys.argv[1], 'rb') as file:
            # read binary content
            bin = file.read()
        
        # extract ascii (w/ 4+ printable chars)
        text = re.findall(b'[ -~]{4,}', bin)
        
        bin_decode = [t.decode('ascii', errors='ignore') for t in text]
        
        # if content, dump to .txt
        if not bin_decode:
            sys.exit('\r\nNothing found!\r\n')
        else:
            # create output file
            with open(sys.argv[2], 'w') as file2:
                for line in bin_decode:
                    file2.write(f"{line}\n")
        
    except Exception as e:
        sys.exit(f'\r\nError: {e}\r\n')
        
if __name__ == '__main__':
    main()
