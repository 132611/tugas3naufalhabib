# Import Library
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import numpy as np

# Vigenere Cipher
# Fungsi Enkripsi Vigenere
def encrypt_vigenere(plaintext, key):
    key = key.lower()
    ciphertext = ""
    for i in range(len(plaintext)):
        letter = plaintext[i]
        if letter.isalpha():
            shift = ord(key[i % len(key)]) - ord('a')
            if letter.islower():
                ciphertext += chr((ord(letter) - ord('a') + shift) % 26 + ord('a'))
            else:
                ciphertext += chr((ord(letter) - ord('A') + shift) % 26 + ord('A'))
        else:
            ciphertext += letter
    return ciphertext

# Fungsi Dekripsi Vigenere
def decrypt_vigenere(ciphertext, key):
    key = key.lower()
    plaintext = ""
    for i in range(len(ciphertext)):
        letter = ciphertext[i]
        if letter.isalpha():
            shift = ord(key[i % len(key)]) - ord('a')
            if letter.islower():
                plaintext += chr((ord(letter) - ord('a') - shift) % 26 + ord('a'))
            else:
                plaintext += chr((ord(letter) - ord('A') - shift) % 26 + ord('A'))
        else:
            plaintext += letter
    return plaintext

# Hill Cipher
# Fungsi Matriks Invers Modulo 26 (Jumlah Alfabet)
def matrix_mod_inverse(matrix, modulus):
    det = int(np.round(np.linalg.det(matrix)))  # Determinan matriks
    det_inv = pow(det % modulus, -1, modulus)  # Invers dari determinan modulo 26
    matrix_inv = det_inv * np.round(np.linalg.inv(matrix) * det) % modulus
    return matrix_inv.astype(int)

# Fungsi Enkripsi Hill
def encrypt_hill(plaintext, key):
    key_matrix = np.array(key).reshape(2, 2)
    ciphertext = ""
    plaintext = plaintext.lower().replace(" ", "")
    
    # Pastikan panjang plaintext genap
    if len(plaintext) % 2 != 0:
        plaintext += 'x'  # Menambahkan 'x' jika panjangnya ganjil
    
    for i in range(0, len(plaintext), 2):
        pair = plaintext[i:i+2]
        vector = np.array([ord(pair[0]) - ord('a'), ord(pair[1]) - ord('a')])
        encrypted_vector = (np.dot(key_matrix, vector) % 26)
        ciphertext += chr(encrypted_vector[0] + ord('a'))
        ciphertext += chr(encrypted_vector[1] + ord('a'))
    
    return ciphertext

# Fungsi Dekripsi Hill
def decrypt_hill(ciphertext, key):
    key_matrix = np.array(key).reshape(2, 2)
    key_matrix_inv = matrix_mod_inverse(key_matrix, 26)
    plaintext = ""
    ciphertext = ciphertext.lower().replace(" ", "")
    
    for i in range(0, len(ciphertext), 2):
        pair = ciphertext[i:i+2]
        vector = np.array([ord(pair[0]) - ord('a'), ord(pair[1]) - ord('a')])
        decrypted_vector = (np.dot(key_matrix_inv, vector) % 26)
        plaintext += chr(decrypted_vector[0] + ord('a'))
        plaintext += chr(decrypted_vector[1] + ord('a'))
    
    return plaintext

# Playfair Cipher
def generate_playfair_matrix(key):
    key = key.upper().replace("J", "I")
    matrix = []
    for char in key + "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if char not in matrix:
            matrix.append(char)
    return np.array(matrix).reshape(5, 5)

def find_position(matrix, char):
    char = char.upper().replace("J", "I")
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == char:
                return i, j

# Fungsi Enkripsi Playfair
def encrypt_playfair(plaintext, key):
    key_matrix = generate_playfair_matrix(key)
    plaintext = plaintext.upper().replace("J", "I").replace(" ", "")
    ciphertext = ""
    
    i = 0
    while i < len(plaintext):
        a = plaintext[i]
        b = plaintext[i + 1] if (i + 1 < len(plaintext)) else 'X'
        
        if a == b:
            b = 'X'
        
        row1, col1 = find_position(key_matrix, a)
        row2, col2 = find_position(key_matrix, b)
        
        if row1 == row2:
            ciphertext += key_matrix[row1][(col1 + 1) % 5]
            ciphertext += key_matrix[row2][(col2 + 1) % 5]
        elif col1 == col2:
            ciphertext += key_matrix[(row1 + 1) % 5][col1]
            ciphertext += key_matrix[(row2 + 1) % 5][col2]
        else:
            ciphertext += key_matrix[row1][col2]
            ciphertext += key_matrix[row2][col1]
        
        i += 2
    
    return ciphertext

def decrypt_playfair(ciphertext, key):
    key_matrix = generate_playfair_matrix(key)
    plaintext = ""
    
    i = 0
    while i < len(ciphertext):
        a, b = ciphertext[i], ciphertext[i + 1]
        row1, col1 = find_position(key_matrix, a)
        row2, col2 = find_position(key_matrix, b)
        
        if row1 == row2:
            plaintext += key_matrix[row1][(col1 - 1) % 5] + key_matrix[row2][(col2 - 1) % 5]
        elif col1 == col2:
            plaintext += key_matrix[(row1 - 1) % 5][col1] + key_matrix[(row2 - 1) % 5][col2]
        else:
            plaintext += key_matrix[row1][col2] + key_matrix[row2][col1]
        
        i += 2
    
    return plaintext

# GUI using tkinter library
class CipherApp:
    
    # Inisiasi Awal
    def __init__(self, root):
        self.root = root
        self.root.title("App Naufal Habib Muzakki - 4611422156")
        self.create_widgets()

    # Fungsi Background App
    def create_widgets(self):
        # Input Plaintext (Text Box)
        self.input_label = tk.Label(self.root, text="Masukkan Teks Dibawah / Upload File(.txt)")
        self.input_label.pack()
        self.input_text = ScrolledText(self.root, height=10)
        self.input_text.pack()

        # Tombol Unggah Berkas .txt (Button)
        self.load_button = tk.Button(self.root, text="Unggah dari File(.txt)", command=self.load_file)
        self.load_button.pack()

        # Input Kunci Enkripsi (key)
        self.key_label = tk.Label(self.root, text="Masukkan Kunci(min. 12 Karakter):")
        self.key_label.pack()
        self.key_entry = tk.Entry(self.root, width=40)
        self.key_entry.pack()

        # Pilihan Metode Cipher (Dropdown)
        self.method_label = tk.Label(self.root, text="Pilih Metode Cipher")
        self.method_label.pack()
        self.method_var = tk.StringVar(self.root)
        self.method_var.set("Vigenere")
        self.method_menu = tk.OptionMenu(self.root, self.method_var, "Vigenere", "Hill", "Playfair")
        self.method_menu.pack()

        # Tombol Enkripsi (Button)
        self.encrypt_button = tk.Button(self.root, text="Enkripsi", command=self.encrypt)
        self.encrypt_button.pack()

        # Tombol Dekripsi (Button)
        self.decrypt_button = tk.Button(self.root, text="Dekripsi", command=self.decrypt)
        self.decrypt_button.pack()

        # Output Ciphertext (Text Box)
        self.output_label = tk.Label(self.root, text="Cipher Text:")
        self.output_label.pack()
        self.output_text = ScrolledText(self.root, height=8)
        self.output_text.pack()

    # Fungsi Unggah Berkas
    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
            self.input_text.insert(tk.END, content)

    # Fungsi Enkripsi
    def encrypt(self):
        plaintext = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        if len(key) < 12:
            messagebox.showerror("Error", "Kunci harus minimal 12 karakter")
            return
        cipher_type = self.method_var.get()
        ciphertext = ""
        if cipher_type == "Vigenere":
            ciphertext = encrypt_vigenere(plaintext, key)
        elif cipher_type == "Hill":
            ciphertext = encrypt_hill(plaintext, key)
        elif cipher_type == "Playfair":
            cipher_type = encrypt_playfair(plaintext, key)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, ciphertext)

    # Fungsi Dekripsi
    def decrypt(self):
        ciphertext = self.input_text.get("1.0", tk.END).strip()
        key = self.key_entry.get().strip()
        if len(key) < 12:
            messagebox.showerror("Error", "Kunci harus minimal 12 karakter")
            return
        cipher_type = self.method_var.get()
        plaintext = ""
        if cipher_type == "Vigenere":
            plaintext = decrypt_vigenere(ciphertext, key)
        elif cipher_type == "Hill":
            plaintext = decrypt_hill(ciphertext, key)
        elif cipher_type == "Playfair":
            plaintext = decrypt_playfair(ciphertext, key)
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, plaintext)

# Fungsi Utama
if __name__ == "__main__":
    root = tk.Tk()
    app = CipherApp(root)
    root.mainloop()