# ghost_core.py
from .utils import GhostEntropyAI
from .ghost_matrix_cipher_g import GhostMatrixCipherG
from .ghost_transformer_v26 import GhostTransformerV26
from .compressor_zlib import GhostCompressor
from .ghost_mac_g import GhostMACG
from .ghost_operator_g import GhostOperatorG
from .v26g_quantum import GhostSecurityAutotuner, kyber_encapsulate
from .v26g_benchmark import measure_entropy

# Class GhostCore
# Esta classe encapsula a lógica principal do GhostEncryptor V26G.
# Ela gerencia a criptografia, compressão, MAC e entropia.
class GhostCore:
    def __init__(self, seed: str):
        if isinstance(seed, bytes):
            self.seed = seed
        else:
            self.seed = seed.encode()

        # Encapsulamento real com Kyber para gerar segredo compartilhado
        _, shared_secret = kyber_encapsulate()
        self.shared_secret = shared_secret  # armazenar para depuração se necessário

        # Derivando chave principal a partir do segredo encapsulado
        self.main_key = shared_secret[:64]

        # Criando instância da IA de entropia com base na seed
        self.entropy_ai = GhostEntropyAI(seed)

        # Operador G e autotuner
        self.g_operator = GhostOperatorG(self.seed)
        self.autotuner = GhostSecurityAutotuner(self.g_operator)

        # Componentes internos com base na main_key
        self.matrix_cipher = GhostMatrixCipherG(self.main_key)
        self.transformer = GhostTransformerV26(self.main_key, self.entropy_ai)
        self.compressor = GhostCompressor()
        self.mac = GhostMACG(self.main_key)

    def encrypt(self, data: bytes) -> bytes:
        iv = self.main_key[:16]  # Derivado diretamente da main_key

        # Certificando-se de que os dados estão em formato bytes
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Compressão
        compressed = self.compressor.compress(data)

        # Avaliação da entropia e autotuning
        entropy = measure_entropy(compressed)
        tuning = self.autotuner.suggest_parameters(entropy, len(compressed))
        print(f"[AUTOTUNER] Nível: {tuning['level']}, Rodadas: {tuning['rounds']}")

        # Transformação + cifragem com rodadas adaptativas (se suportado)
        transformed = self.transformer.transform(compressed, rounds=tuning['rounds'])
        encrypted = self.matrix_cipher.encrypt_gcbc(transformed, iv, rounds=tuning['rounds'])

        # MAC
        mac = self.mac.compute_mac(encrypted, iv)

        return iv + mac + encrypted

    def decrypt(self, payload: bytes) -> bytes:
        iv = payload[:16]
        mac = payload[16:16+64]
        encrypted = payload[16+64:]
        self.mac.verify_mac(encrypted, iv, mac)
        decrypted = self.matrix_cipher.decrypt_gcbc(encrypted, iv)
        original = self.transformer.transform_decrypt(decrypted)
        return self.compressor.decompress(original)
