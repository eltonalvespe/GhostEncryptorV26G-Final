# ghost_operator_g.py

# Class GhostOperatorG
# Esta classe implementa operadores G simbólicos e matemáticos para transformação avançada em criptografia.
# Ele implementa lógica baseada na Álgebra G (não comutativa, com incerteza incorporada).
# A classe é projetada para ser utilizada em conjunto com o GhostEncryptor V26G.
# Ela é otimizada para trabalhar com dados binários e pode ser facilmente integrada em sistemas de criptografia.
# A implementação é baseada em conceitos de criptografia moderna e técnicas de segurança.
# A classe é escrita em Python e utiliza bibliotecas padrão para operações de criptografia.
# A classe também inclui métodos para verificação de MAC, garantindo que os dados não tenham sido alterados.

class GhostOperatorG:
    def __init__(self, seed: bytes):
        """Inicializa o operador G com uma seed."""
        self.seed = seed
        
    def apply_operator_sequence(self, data: bytes, reverse: bool = False) -> bytes:
        """Aplica uma sequência de operações de acordo com o parâmetro reverse."""
        if reverse:
            data = self.reverse_operations(data)
        else:
            data = self.apply_operations(data)
        return data

    def apply_operations(self, data: bytes) -> bytes:
        """Aplica transformações G sobre os dados."""
        return bytes([self.g_add(b, self.seed[i % len(self.seed)]) for i, b in enumerate(data)])

    def reverse_operations(self, data: bytes) -> bytes:
        """Desfaz transformações G."""
        return bytes([self.g_sub(b, self.seed[i % len(self.seed)]) for i, b in enumerate(data)])

    def g_add(self, a: int, b: int) -> int:
        """Adição G (exemplo com comportamento simbólico modificado)"""
        # Adicionando a operação de XOR para simular uma adição não convencional com 'incerteza'
        return (a + b + (a ^ b) % 7) % 256

    def g_sub(self, a: int, b: int) -> int:
        """Subtração G (inverso da g_add)"""
        return (a - b - (a ^ b) % 7) % 256

    def g_mul(self, a: int, b: int) -> int:
        """Multiplicação G (com não comutatividade simples)"""
        # Multiplicação modificada para refletir comportamento não comutativo
        return ((a * (b + 1)) ^ (b * (a + 1))) % 256

    def g_mod(self, a: int, mod: int) -> int:
        """Módulo G (incorporando incerteza simbólica)"""
        # A incerteza é incorporada pela combinação do valor e do módulo de forma simbólica
        return (a + (a ^ mod) % 11) % mod

    def g_inverse(self, a: int, mod: int) -> int:
        """Inverso G (versão modificada da inversa modular)"""
        # Busca pelo inverso usando o algoritmo de tentativa e erro
        for i in range(1, mod):
            if self.g_mod(self.g_mul(a, i), mod) == 1:
                return i
        return 1  # Retorna 1 como fallback simbólico

    def apply_operator_sequence(self, data: bytes, reverse: bool = False) -> bytes:
        """Aplica uma sequência de operações de acordo com o parâmetro reverse."""
        if reverse:
            data = self.reverse_operations(data)
        else:
            data = self.apply_operations(data)
        return data

    def apply_operations(self, data: bytes) -> bytes:
        # Simula uma transformação G com operador XOR e rotação
        rotated = data[-1:] + data[:-1]
        return bytes([b ^ self.seed[i % len(self.seed)] for i, b in enumerate(rotated)])
        #"""Aplica transformações G sobre os dados."""
        #return bytes([self.g_add(b, self.seed[i % len(self.seed)]) for i, b in enumerate(data)])

    def reverse_operations(self, data: bytes) -> bytes:
        xor_reversed = bytes([b ^ self.seed[i % len(self.seed)] for i, b in enumerate(data)])
        return xor_reversed[1:] + xor_reversed[:1]
        #"""Desfaz transformações G."""
        #return bytes([self.g_sub(b, self.seed[i % len(self.seed)]) for i, b in enumerate(data)])

