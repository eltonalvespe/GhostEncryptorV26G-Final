
# 🔐 GhostEncryptorV26G-Final

Versão final e estável do GhostEncryptor V26G — um sistema criptográfico avançado, pós-quântico e autossuficiente, baseado na Álgebra dos Números Fantasmas G.

## 📦 Visão Geral

O `GhostEncryptorV26G` é um framework de criptografia experimental e educacional que combina compressão simbólica, cifragem baseada em matrizes, operadores não comutativos, encapsulamento pós-quântico simulado (Kyber/NTRU/Frodo), e MAC-G (autenticação de integridade). Foi projetado para ser resistente a ataques clássicos e quânticos, além de funcionar de forma independente de bibliotecas criptográficas externas como `hashlib` ou `Crypto`.

## 🧬 Principais Componentes

- 🔣 **Compressão G Simbólica** (`ghost_compressor_g_symbolic.py`)  
  Compressão simbólica com prefixos de controle, segurança contra ruídos e codificação com seed.

- ⚙️ **Operadores G** (`ghost_operator_g.py`)  
  Transformações não lineares baseadas em álgebra G, incluindo operadores como `g_add`, `g_mul`, `g_inverse`.

- 🧪 **Cifragem com Matrizes G** (`ghost_matrix_cipher_g.py`)  
  Modo GCBC com rotação e difusão simbólica, utilizando estrutura matricial.

- 🔐 **MAC-G** (`ghost_mac_g.py`)  
  Autenticação de integridade baseada em GHash V6 com entropia dinâmica e operador θ.

- 🔒 **Encapsulamento Pós-Quântico** (`ghost_pq_hybrid.py`)  
  Simulação de KEMs híbridos com Kyber/NTRU/Frodo para geração de segredos seguros.

- 📈 **Autotuning Inteligente** (`v26g_quantum.py`)  
  Heurísticas de segurança com IA simbólica para ajuste dinâmico da criptografia.

- 🧠 **GhostCore** (`ghost_core.py`)  
  Núcleo modular que integra compressão, cifragem, operadores G, MAC e IA de entropia.

## 🗂️ Estrutura de Diretórios

```
GhostEncryptorV26G-Final/
├── examples/
│   └── demo_encrypt_decrypt.py
├── ghost_encryptor_v26g/
│   ├── GhostEncryptorV26G.py
│   ├── GhostEncryptorV26G_Final.py
│   ├── ghost_core.py
│   ├── ghost_mac_g.py
│   ├── ghost_matrix_cipher_g.py
│   ├── ghost_operator_g.py
│   ├── ghost_compressor_g_symbolic.py
│   ├── ghost_pq_hybrid.py
│   ├── ghost_transformer_v26.py
│   ├── ghash.py
│   ├── compressor_zlib.py
│   ├── interfaces.py
│   ├── utils.py
│   ├── v26g_quantum.py
│   ├── v26g_benchmark.py
│   └── __init__.py
├── tests/
│   └── test_core.py
├── .gitignore
├── LICENSE
└── README.md
```

## 🚀 Como Usar

### 1. Instalação
```bash
git clone https://github.com/eltonalvesp/GhostEncryptorV26G-Final.git
cd GhostEncryptorV26G-Final
```

> ⚠️ Requer Python 3.8+

### 2. Exemplo de Uso

```python
from ghost_encryptor_v26g.GhostEncryptorV26G_Final import GhostEncryptorV26G

encryptor = GhostEncryptorV26G(seed=b"minha_seed_segura")
mensagem = "Mensagem confidencial 🔒"
cifrado = encryptor.encrypt(mensagem)
decifrado = encryptor.decrypt(cifrado)
print(decifrado.decode())
```

### 3. Criptografar Arquivos

```python
encryptor.encryptFile("secreto.txt", "secreto.ghost", encryptor.encryptByte)
encryptor.decryptFile("secreto.ghost", "restaurado.txt", encryptor.decryptByte)
```

## ✅ Recursos

| Recurso                        | Implementado |
|-------------------------------|--------------|
| Compressão simbólica G        | ✅           |
| Operadores G (não comutativos)| ✅           |
| MAC-G com GHash               | ✅           |
| Cifragem Matricial GCBC       | ✅           |
| Suporte Pós-Quântico          | ✅ (simulado)|
| Autotuning com IA simbólica   | ✅           |
| Independente de hashlib/Crypto| ✅           |

## 🧪 Testes

```bash
python tests/test_core.py
```

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais detalhes.

## 🤝 Contribuições

Sinta-se à vontade para abrir *issues*, enviar *pull requests*, ou propor melhorias para fortalecer ainda mais este sistema.

## 👤 Autor

**Elton Alves P.**  
Criptógrafo experimental, pesquisador em álgebra simbólica e segurança da informação quântica.
