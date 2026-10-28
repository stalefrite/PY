import random, sys

def randomize_escapes(text: str) -> str:
    escaped_string = ""
    
    for char in text:
        # get the ascii value of character
        ascii_val = ord(char)
        
        # randomly choose between hex (0) and octal (1)
        if random.choice([True, False]):
            escaped_string += f"\\x{ascii_val:02x}"
        else:
            # octal (padded to 3 digits for consistency)
            escaped_string += f"\\{ascii_val:03o}"
            
    return escaped_string

def main():
    # Credits: ChatGPT
    # Escape Sequence (Hex/Octal) String Confuser
    # Helps obfuscate code for PHP, Perl, Python, C, etc... 
    try:
        while True:
            input_text = input("Input:\r\n")
            result = randomize_escapes(input_text)
            print("\r\nOutput:")
            print(result)
            print("-" * 50)
    except KeyboardInterrupt:
        sys.exit("\r\n")

if __name__ == "__main__":
    main()
