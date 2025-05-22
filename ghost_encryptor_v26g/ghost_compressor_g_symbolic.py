# ghost_compressor_g.py

import zlib

# Class GhostCompressorG
# Esta classe implementa a compressão simbólica de dados usando o algoritmo zlib.
# Ela adiciona um prefixo para diferenciar entre dados vazios e dados comprimidos.
class GhostCompressorG:
    def __init__(self, seed: bytes):
        self.seed = seed

    def compress(self, data: bytes) -> bytes:
        if not data:
            return b'\x00G\x00'  # marcador para vazio

        compressed = zlib.compress(data)
        encoded = self._symbolic_encode(compressed)
        return b'\x00G\x01' + encoded  # marcador para dado simbólico comprimido

    def decompress(self, data: bytes) -> bytes:
        if not data.startswith(b'\x00G'):
            raise ValueError("Flag de compressão simbólica inválida.")

        flag = data[2]
        content = data[3:]

        if flag == 0x00:
            return b''  # dado original era vazio
        elif flag == 0x01:
            decoded = self._symbolic_decode(content)
            return zlib.decompress(decoded)
        else:
            raise ValueError("Flag de tipo de dado simbólico desconhecida.")

    def _symbolic_encode(self, data: bytes) -> bytes:
        return bytes([b ^ self.seed[i % len(self.seed)] for i, b in enumerate(data)])

    def _symbolic_decode(self, data: bytes) -> bytes:
        return bytes([b ^ self.seed[i % len(self.seed)] for i, b in enumerate(data)])


if __name__ == "__main__":
    s = "Teste de compressão G simbólica Ghost V25G Final!".encode('utf-8')
    g = GhostCompressorG(seed=b"g25final")

    c = g.compress(s)
    d = g.decompress(c)
    assert d == s, "Erro: compressão ou descompressão falhou!"
    print("[✔️] Compressão e descompressão simbólica funcionaram corretamente.")

