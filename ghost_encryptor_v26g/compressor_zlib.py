# compressor_zlib.py
import zlib
# GhostCompressor
# Classe para compressão e descompressão de dados usando zlib.
# Esta classe fornece métodos para comprimir e descomprimir dados.
class GhostCompressor:
    def compress(self, data: bytes) -> bytes:
        # Compressão com zlib
        return zlib.compress(data)

    def decompress(self, data: bytes) -> bytes:
        # Descompressão com zlib
        try:
            return zlib.decompress(data)
        except zlib.error as e:
            raise ValueError("Erro ao descomprimir os dados: " + str(e))
