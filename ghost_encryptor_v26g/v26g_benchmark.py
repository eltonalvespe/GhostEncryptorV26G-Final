import time
import math
from collections import Counter

# Funções de benchmark para medir o desempenho e a entropia de funções criptográficas.
# Essas funções são projetadas para avaliar o desempenho de algoritmos de criptografia
def measure_entropy(data: bytes) -> float:
    """
    Calcula a entropia de Shannon dos dados.
    """
    if not data:
        return 0.0
    counter = Counter(data)
    total = len(data)
    entropy = -sum((count / total) * math.log2(count / total) for count in counter.values())
    return entropy

# Função de benchmark para medir o tempo e a entropia de uma operação
# de criptografia.
# Essa função mede o tempo de execução e a entropia da saída de uma função.
# Ela pode ser usada para avaliar o desempenho de algoritmos de criptografia
# e manipulação de dados.
# A função aceita uma função como argumento, juntamente com seus parâmetros,
# e retorna um dicionário com o tempo de execução, a entropia e o resultado.
# Ela é otimizada para trabalhar com dados binários e pode ser facilmente integrada em sistemas de criptografia.
def benchmark_operation(func, *args, **kwargs):
    """
    Mede o tempo e a entropia da saída de uma função.
    """
    start = time.perf_counter()
    result = func(*args, **kwargs)
    duration = time.perf_counter() - start
    entropy = measure_entropy(result) if isinstance(result, bytes) else None
    return {
        "duration_seconds": duration,
        "entropy_bits_per_byte": entropy,
        "result": result
    }
