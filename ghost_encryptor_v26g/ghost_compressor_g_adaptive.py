import zlib

# Class GhostCompressorGAdaptive
# Esta classe aplica compressão zlib com comportamento adaptativo simples.
class GhostCompressorGAdaptive:
    """
    GhostCompressorGAdaptive aplica compressão zlib com comportamento adaptativo simples.
    Suporta prefixos para diferenciar dados vazios e comprimidos.
    Opcionalmente usa uma seed (não usada nesta versão, mas reservada para versões futuras).
    """

    def __init__(self, seed: bytes = b''):
        self.seed = seed  # Mantido para compatibilidade com arquitetura GhostEncryptorV24G

    def compress(self, data: bytes) -> bytes:
        """
        Comprime os dados com zlib. Adiciona prefixo:
        \x00 para dados vazios, \x01 para dados comprimidos.
        """
        if not data:
            return b'\x00'  # Marcador para dados vazios
        level = 9 if len(data) > 1024 else 1  # Compressão adaptativa simples
        compressed = zlib.compress(data, level)
        return b'\x01' + compressed

    def decompress(self, data: bytes) -> bytes:
        """
        Descomprime os dados com base no prefixo.
        \x00: retorna vazio, \x01: descomprime com zlib.
        """
        if not data:
            raise ValueError("Dados vazios não podem ser descomprimidos.")
        flag = data[0]
        payload = data[1:]

        if flag == 0x00:
            return b''
        elif flag == 0x01:
            try:
                return zlib.decompress(payload)
            except Exception as e:
                raise ValueError("Erro ao descomprimir os dados adaptativos: " + str(e))
        else:
            raise ValueError(f"Flag de compressão desconhecida: {flag}")
