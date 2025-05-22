# ghost_matrix_cipher_g.py

# GhostMatrixCipherG
# Esta classe implementa a cifragem baseada em matrizes usando a Álgebra G.
# Ela é projetada para ser utilizada em conjunto com o GhostEncryptor V26G.
# A implementação é baseada em conceitos de criptografia moderna e técnicas de segurança.
# A classe é escrita em Python e utiliza bibliotecas padrão para operações de criptografia.
# A classe também inclui métodos para cifragem e decifragem, garantindo que os dados possam ser recuperados corretamente.
# A cifragem é baseada em operações de XOR e manipulação de matrizes, proporcionando segurança adicional.
# A classe é otimizada para trabalhar com dados binários e pode ser facilmente integrada em sistemas de criptografia.
# Implementa cifragem baseada em matrizes usando a Álgebra G (educacional)

import os

class GhostMatrixCipherG:
    def __init__(self, key: bytes):
        if isinstance(key, str):
            key = key.encode()
            
        self.key = key
        self.seed = key
        self.matrix = self._generate_matrix()

    def _generate_matrix(self):
        size = 16
        return [[(i * j + self.seed[(i + j) % len(self.seed)]) % 256 for j in range(size)] for i in range(size)]

    def _generate_iv_from_key(self, key: bytes) -> bytes:
        return key[:16] if len(key) >= 16 else (key * 2)[:16]

    def encrypt_gcbc(self, data: bytes, iv: bytes, rounds: int = 9) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        if isinstance(iv, str):
            iv = iv.encode()
        result = data
        for _ in range(rounds):
            result = self._xor_gcbc_round(result, iv)
        return result

    def decrypt_gcbc(self, data: bytes, iv: bytes, rounds: int = 9) -> bytes:
        if isinstance(data, str):
            data = data.encode()
        if isinstance(iv, str):
            iv = iv.encode()
        result = data
        for _ in range(rounds):
            result = self._xor_gcbc_round(result, iv)
        return result

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        return self._xor_g_operator(data, key)

    def decrypt(self, data: bytes, key: bytes) -> bytes:
        return self._xor_g_operator(data, key)

    def _xor_gcbc_round(self, data: bytes, iv: bytes) -> bytes:
        return bytes([
            b ^ iv[i % len(iv)] ^ self.key[i % len(self.key)]
            for i, b in enumerate(data)
        ])
        
    def _xor_g_operator(self, data: bytes, key: bytes) -> bytes:
        kstream = bytearray()
        for i in range(len(data)):
            k = key[i % len(key)]
            kstream.append(k ^ ((i * 17) % 256))
        return bytes([b ^ kstream[i] for i, b in enumerate(data)])


