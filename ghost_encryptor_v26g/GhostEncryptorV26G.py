# GhostEncryptorV26G.py
import time

from .ghost_compressor_g_symbolic import GhostCompressorG
from .ghost_operator_g import GhostOperatorG
from .ghost_mac_g import ghost_mac_g_verify, ghost_mac_g_generate
from .ghost_matrix_cipher_g import GhostMatrixCipherG
from .ghost_pq_hybrid import simulate_kyber_keypair, simulate_kyber_encapsulate

# GhostEncryptorV26G
# Classe para manipular criptografia e descriptografia usando a álgebra G.
# Ele usa um operador G, cifra de matriz, compressão simbólica e MAC-G.
# A implementação é baseada em conceitos modernos de criptografia e técnicas de segurança.
class GhostEncryptorV26G:
    def __init__(self, seed: bytes):
        self.seed = seed
        self.compressor = GhostCompressorG()
        self.operator_g = GhostOperatorG(seed)
        self.cipher = GhostMatrixCipherG(seed)

    def encrypt(self, plaintext: str) -> bytes:
        print("[🟢] Iniciando criptografia com V25G...")

        # Compressão G simbólica
        compressed = self.compressor.compress(plaintext.encode())
        print("[🟢] Compressão simbólica concluída.")

        # Transformações G
        transformed = self.operator_g.apply_operator_sequence(compressed)
        print("[🟢] Transformações G aplicadas.")

        # Chave híbrida PQ
        public_key, shared_secret = simulate_kyber_encapsulate(self.seed)

        # Cifra G com chave compartilhada
        encrypted = self.cipher.encrypt(transformed, shared_secret)

        # MAC-G para integridade
        mac = ghost_mac_g_generate(transformed, shared_secret)

        print("[🟢] Criptografia híbrida finalizada com sucesso.")
        return public_key + mac + encrypted

    def decrypt(self, ciphertext: bytes) -> str:
        print("[🔵] Iniciando descriptografia com V25G...")

        public_key = ciphertext[:32]
        mac = ciphertext[32:64]
        encrypted = ciphertext[64:]

        # Reconstituir chave compartilhada
        shared_secret = simulate_kyber_keypair(self.seed, public_key)

        # Decifra usando matriz G
        decrypted = self.cipher.decrypt(encrypted, shared_secret)

        # Verifica integridade MAC-G
        if not ghost_mac_g_verify(decrypted, shared_secret, mac):
            raise ValueError("[❌] Falha na verificação MAC-G.")
        print("[🔵] MAC-G validado com sucesso.")

        # Reverter transformações G
        restored = self.operator_g.apply_operator_sequence(decrypted, reverse=True)
        print("[🔵] Operador G revertido com sucesso.")

        # Descompressão simbólica
        decompressed = self.compressor.decompress(restored)
        print("[🔵] Descompressão simbólica concluída.")

        return decompressed.decode()
