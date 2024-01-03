import numpy as np

class HammingCode:
    def __init__(self, m):
        self.m = m
        self.n = 2 ** m - 1
        self.r = m
        self.k = self.n - self.r
        self.gen_matrix = self.get_generate_matrix()
        self.check_matrix = self.get_check_matrix()

    def get_generate_matrix(self):
        I = np.identity(self.n - self.r, dtype=int)
        P = np.array([list(np.binary_repr(i, width=self.r)) for i in range(1, self.n - self.r + 1)], dtype=int)
        return np.concatenate((I, P), axis=1)

    def get_check_matrix(self):
        P = np.array([list(np.binary_repr(i, width=self.r)) for i in range(1, self.n - self.r + 1)], dtype=int)
        I = np.identity(self.r, dtype=int)
        return np.concatenate((P.T, I), axis=1)

    def encode(self, data):
        data = np.array(list(map(int, data)))
        encoded_data = np.dot(data, self.gen_matrix) % 2
        print(f"Encoded data: {encoded_data}")
        return encoded_data

    def decode(self, code):
        syndrome = np.dot(code, self.check_matrix.T) % 2
        if np.count_nonzero(syndrome) == 0:
            decoded_code = code[:self.n - self.r]
            print(f"Decoded code: {decoded_code}")
            return decoded_code
        else:
            error_pos = int(''.join(map(str, syndrome)), 2) - 1
            corrected_code = code.copy()
            corrected_code[error_pos] ^= 1
            print("Corrected code before removing parity bits:", corrected_code)
            print(f"Corrected code: {corrected_code[:self.n - self.r]}")
            return corrected_code[:self.n - self.r]

    def check(self, code):
        syndrome = np.dot(code, self.check_matrix.T) % 2
        is_valid = np.count_nonzero(syndrome) == 0
        print(f"Code '{code}' is {'valid' if is_valid else 'invalid'}")
        return is_valid

# example use case
hamming = HammingCode(3)  # m = 3

# Print the generator and parity check matrix
print("Generator Matrix:\n", hamming.get_generate_matrix())
print("")
print("Parity Check Matrix:\n", hamming.get_check_matrix())
print("")

# Define and print word
word = '1011'
print("Word not encoded: " + word)
print("")

# Encode and print word (encoded code is printed in method)
code = hamming.encode(word)

# Decode and print word (decoded code is printed in method)
decoded_code = hamming.decode(code)

# Check if the code is valid (print is in method)
hamming.check(code)

print("")

# Create an error in the code
print("Deliberately create an error in code:")
print("")
error_code = code.copy()
error_code[3] ^= 1  # Flip the fourth bit
print("Error code:", error_code)

# Check if the code is valid (print is in method)
print("")
print("Check if errorcode is valid:")
print("")
valid_error = hamming.check(error_code)
if not valid_error:
    # Decode and print the error code (print in method)
    print("")
    print("Correct the wrong code:")
    print("")
    corrected_code = hamming.decode(error_code)
