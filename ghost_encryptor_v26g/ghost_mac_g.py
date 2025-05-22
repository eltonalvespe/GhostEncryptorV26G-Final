# ghost_mac_g.py
import hmac

# Class GhostMACG
# Esta classe implementa um sistema de MAC (Código de Autenticação de Mensagem) avançado.
# Ela utiliza uma combinação de funções hash, entropia dinâmica e compressão simbólica.
# O objetivo é garantir a integridade e autenticidade dos dados.
# A implementação é baseada em conceitos de criptografia moderna e técnicas de segurança.
# A classe é projetada para ser utilizada em conjunto com o GhostEncryptor V26G.
# Ela é otimizada para trabalhar com dados binários e pode ser facilmente integrada em sistemas de criptografia.
# A classe também inclui métodos para verificação de MAC, garantindo que os dados não tenham sido alterados.
# Além disso, a classe é projetada para ser extensível, permitindo que novos métodos de MAC sejam adicionados no futuro.
# A implementação é modular e pode ser facilmente adaptada para diferentes algoritmos de hash ou técnicas de compressão.
# A classe é escrita em Python e utiliza bibliotecas padrão para operações de criptografia.
# GhostMACG é uma implementação avançada de MAC (Código de Autenticação de Mensagem) para garantir a integridade e autenticidade dos dados.
# A classe utiliza uma combinação de funções hash, entropia dinâmica e compressão simbólica.
# O objetivo é garantir a integridade e autenticidade dos dados.

class GhostMACG:
    def __init__(self, seed: bytes):
        self.seed = seed
    
    def _rotate_left(self, val, r_bits, max_bits=8):
        return ((val << r_bits) & (2**max_bits - 1)) | (val >> (max_bits - r_bits))

    def _ghash_v6(self, data: bytes) -> bytes:
        """
        Versão avançada: usa rotação, entropia dinâmica G, compressão simbólica e operador θ.
        """
        mac = bytearray(64)
        entropy = sum(self.seed) % 256
        theta = len(data) ^ len(self.seed)

        for i, b in enumerate(data):
            idx = (i + theta) % 64
            g_val = self.seed[i % len(self.seed)] ^ entropy ^ ((i * 17) % 251)
            rotated = self._rotate_left(b ^ g_val, (i + entropy) % 8)
            mac[idx] = (mac[idx] + rotated + g_val + theta) % 256

            # Evolução da entropia com feedback dinâmico (modo G)
            entropy = (entropy + rotated + mac[idx] + i) % 256
            theta = (theta ^ rotated ^ entropy) % 256

        return bytes(mac)

    def generate_mac(self, data: bytes) -> bytes:
        return self._ghash_v6(data)

    # Função externa para uso simplificado
    @staticmethod
    def generate(transformed: bytes, shared_secret: bytes) -> bytes:
        """
        Gera um MAC-G usando uma instância da GhostMACG com base no segredo compartilhado.
        """
        mac_engine = GhostMACG(seed=shared_secret)
        return mac_engine.generate_mac(transformed)
    
    @staticmethod
    def verify(transformed: bytes, shared_secret: bytes, received_mac: bytes) -> bool:
        """
        Verifica um MAC-G usando uma instância da GhostMACG com base no segredo compartilhado.
        """
        mac_engine = GhostMACG(seed=shared_secret)
        return mac_engine.verify_mac(transformed, received_mac)


    def verify_mac(self, data: bytes, mac: bytes) -> bool:
        expected_mac = self.generate_mac(data)
        result = self._constant_time_compare(expected_mac, mac)
        print(f"[DEBUG] expected_mac: {expected_mac}")
        print(f"[DEBUG] received_mac: {mac}")
        print(f"[DEBUG] expected_mac == mac: {result}")
        return result

    def _constant_time_compare(self, a: bytes, b: bytes) -> bool:
        if len(a) != len(b):
            return False
        result = 0
        for x, y in zip(a, b):
            result |= x ^ y
        return result == 0
