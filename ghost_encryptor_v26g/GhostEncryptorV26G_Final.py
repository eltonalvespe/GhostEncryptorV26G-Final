# GhostEncryptorV26G_Final.py

import os
from .ghash import GHash
from .ghost_operator_g import GhostOperatorG
from .ghost_matrix_cipher_g import GhostMatrixCipherG
from .ghost_compressor_g_symbolic import GhostCompressorG
from .ghost_mac_g import GhostMACG
from .ghost_pq_hybrid import simulate_kyber_encapsulate, simulate_kyber_decapsulate  # Suporte pós-quântico real
from .ghost_pq_hybrid import GhostPQHybrid  # Simulação de integração com criptografia pós-quântica (PQ)

# class GhostEncryptorV26G
# Esta classe implementa a criptografia e descriptografia usando a Álgebra G.
# Ela utiliza um operador G, cifragem de matriz, compressão simbólica e MAC-G.
# A implementação é baseada em conceitos de criptografia moderna e técnicas de segurança.
# A classe é escrita em Python e utiliza bibliotecas padrão para operações de criptografia.
# A classe também inclui métodos para criptografar e descriptografar arquivos, garantindo que os dados possam ser recuperados corretamente.

class GhostEncryptorV26G:
    def __init__(self, seed: bytes = b"default_seed"):
        # Garante que seed é bytes
        if isinstance(seed, str):
            seed = seed.encode('utf-8')

        self.seed = seed
        self.operator_g = GhostOperatorG(self.seed)
        self.cipher = GhostMatrixCipherG(self.seed)
        self.compressor = GhostCompressorG(seed=self.seed)
        self.mac = GhostMACG(self.seed)
        self.last_recovered_extension = None
        self.last_recovered_data = None

    def encrypt(self, plaintext: str) -> bytes:
        # Entrada pode ser string, convertemos para bytes
        if isinstance(plaintext, str):
            plaintext = plaintext.encode('utf-8')

        print("[🔵] Iniciando criptografia com V26G...")

        # Compressão simbólica
        compressed = self.compressor.compress(plaintext)
        print("[🔵] Compressão simbólica concluída.")
        assert compressed.startswith(b'\x00G'), "[DEBUG] Compressão simbólica não gerou flag esperada"

        # Aplicar operador G
        print(f"[DEBUG] Compressed antes do operador G: {compressed[:40]}...")
        transformed = self.operator_g.apply_operator_sequence(compressed)
        print("[🔵] Transformações G aplicadas.")

        # Gerar chave pública e segredo compartilhado determinístico (Kyber real/simulado)
        pubkey, shared_secret = simulate_kyber_encapsulate(self.seed)
        print("[🔵] Chave pública e segredo compartilhado gerados com sucesso.")

        # Derivação da chave de sessão
        final_key = shared_secret[:32]
        iv = final_key[:16]  # derivação simples de IV
        encrypted = self.cipher.encrypt_gcbc(transformed, iv, rounds=9)

        # MAC-G para integridade
        mac = self.mac.generate_mac(encrypted)
        print("[🔵] Criptografia híbrida finalizada com sucesso.")

        # Estrutura: pubkey (32) + mac (64) + ciphertext
        return pubkey + mac + encrypted

    def decrypt(self, ciphertext: bytes) -> str:
        print("[🔹] Iniciando descriptografia com V26G...")

        if not isinstance(ciphertext, bytes):
            raise TypeError("O ciphertext deve estar em formato bytes!")

        pubkey = ciphertext[:32]
        mac = ciphertext[32:96]
        encrypted = ciphertext[96:]

        # Verificação do MAC-G
        if not self.mac.verify_mac(encrypted, mac):
            raise ValueError("MAC-G falhou! Dados comprometidos.")
        print("[🔹] MAC-G validado com sucesso.")

        # Simula a recuperação do segredo compartilhado
        _, shared_secret = simulate_kyber_encapsulate(self.seed)
        final_key = shared_secret[:32]

        # Decifra os dados
        iv = final_key[:16]  # derivação simples de IV
        decrypted = self.cipher.decrypt_gcbc(encrypted, iv, rounds=9)

        # Reverter transformações G
        restored = self.operator_g.apply_operator_sequence(decrypted, reverse=True)
        print("[🔹] Operador G revertido com sucesso.")
        assert restored.startswith(b'\x00G'), "[DEBUG] Flag de compressão simbólica corrompida após restauração"

        # Descompressão simbólica
        decompressed = self.compressor.decompress(restored)
        print("[🔹] Descompressão simbólica concluída.")

        try:
            # Garante que o retorno seja sempre bytes
            if isinstance(decompressed, str):
                return decompressed.encode("utf-8")
            elif isinstance(decompressed, bytes):
                return decompressed
            else:
                raise TypeError("Tipo inesperado após descompressão.")
    
        except UnicodeDecodeError as e:
            print("[ERRO DE DECODIFICAÇÃO UTF-8]", e)
            print("[DADOS BRUTOS]:", decompressed)
            raise
    
###----------------------------------------------------------------------------------###
    def encryptFile(input_path: str, output_path: str, encrypt_fn) -> None:
        """
        Lê um arquivo, criptografa seu conteúdo e salva em outro arquivo.

        Args:
            input_path (str): Caminho do arquivo de entrada.
            output_path (str): Caminho do arquivo criptografado.
            encrypt_fn (Callable[[bytes], bytes]): Função de criptografia que recebe e retorna bytes.
        """
        with open(input_path, 'rb') as f:
            raw_data = f.read()

        encrypted_data = encrypt_fn(raw_data)

        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

        print(f"[🔐] Arquivo '{input_path}' criptografado e salvo como '{output_path}'.")


    def decryptFile(input_path: str, output_path: str, decrypt_fn) -> None:
        """
        Lê um arquivo criptografado, descriptografa seu conteúdo e salva no destino.

        Args:
            input_path (str): Caminho do arquivo criptografado.
            output_path (str): Caminho do arquivo de saída descriptografado.
            decrypt_fn (Callable[[bytes], bytes]): Função de descriptografia que recebe e retorna bytes.
        """
        with open(input_path, 'rb') as f:
            encrypted_data = f.read()

        decrypted_data = decrypt_fn(encrypted_data)

        with open(output_path, 'wb') as f:
            f.write(decrypted_data)

        print(f"[🔓] Arquivo '{input_path}' descriptografado e salvo como '{output_path}'.")
    ###----------------------------------------------------------------------------------###
    
    def encryptByte(self, plaintext: bytes) -> bytes:
        print("[🟢] Iniciando criptografia com V26G...")

        if not isinstance(plaintext, bytes):
            raise TypeError("O plaintext deve estar em formato bytes!")

        # Compressão simbólica
        compressed = self.compressor.compress(plaintext)
        print("[🟢] Compressão simbólica concluída.")

        # Aplicar transformações G
        transformed = self.operator_g.apply_operator_sequence(compressed)
        print("[🟢] Transformações G aplicadas.")

        # Simula a geração de chave pública e segredo compartilhado determinístico
        pubkey, shared_secret = simulate_kyber_encapsulate(self.seed)
        final_key = shared_secret[:32]
        print("[🟢] Chave pública e segredo compartilhado gerados.")

        # Cifra os dados com GCBC (baseado na Álgebra G)
        iv = final_key[:16]
        ciphertext = self.cipher.encrypt_gcbc(transformed, iv, rounds=9)
        print("[🟢] Cifra GCBC concluída.")

        # Gera o MAC-G para integridade
        mac = self.mac.generate_mac(ciphertext)
        print(f"[🟢] MAC-G gerado: {mac}")

        # Monta o resultado final: pubkey (32) + mac (64) + ciphertext
        final_output = pubkey + mac + ciphertext
        print("[🟢] Criptografia finalizada com sucesso.")

        return final_output

    def decryptByte(self, ciphertext: bytes) -> bytes:
        print("[🔹] Iniciando descriptografia de arquivo com V26G...")

        if not isinstance(ciphertext, bytes):
            raise TypeError("O ciphertext deve estar em formato bytes!")

        pubkey = ciphertext[:32]
        mac = ciphertext[32:96]
        encrypted = ciphertext[96:]

        # Verificação do MAC-G
        if not self.mac.verify_mac(encrypted, mac):
            raise ValueError("MAC-G falhou! Dados comprometidos.")
        print("[🔹] MAC-G validado com sucesso.")

        # Recupera o segredo compartilhado determinístico
        _, shared_secret = simulate_kyber_encapsulate(self.seed)
        final_key = shared_secret[:32]

        # Decifra os dados
        iv = final_key[:16]
        decrypted = self.cipher.decrypt_gcbc(encrypted, iv, rounds=9)

        # Reverte transformações G
        restored = self.operator_g.apply_operator_sequence(decrypted, reverse=True)
        print("[🔹] Operador G revertido com sucesso.")
        assert restored.startswith(b'\x00G'), "[DEBUG] Flag de compressão simbólica corrompida após restauração"

        # Descompressão simbólica
        decompressed = self.compressor.decompress(restored)
        print("[🔹] Descompressão simbólica concluída.")

        # Retorna sempre como bytes
        if isinstance(decompressed, str):
            return decompressed.encode("utf-8")
        elif isinstance(decompressed, bytes):
            return decompressed
        else:
            raise TypeError("Tipo inesperado após descompressão.")
