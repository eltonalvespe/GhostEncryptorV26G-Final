# demo_encrypt_decrypt.py

# Teste de Criptografia e Descriptografia com GhostEncryptorV25G_Final
# Este script demonstra a criptografia e descriptografia usando a classe GhostEncryptorV25G_Final.
# Ele utiliza uma string de exemplo e imprime os resultados no console.
# Importando a classe GhostEncryptorV25G_Final
# do módulo ghost_encryptor_v26g
from ghost_encryptor_v26g.GhostEncryptorV26G_Final import GhostEncryptorV25G

texto_original = "Criptografia GhostEncryptorV25G com compressão simbólica, operadores G e suporte pós-quântico com NTRU/FrodoKEM adaptados!"
print(f"🔐 Texto original: {texto_original}")

ge = GhostEncryptorV25G(seed=b'minha-semente-secreta-25g-final')

print("[🟢] Iniciando criptografia com V25G_Final...")
criptografado = ge.encrypt(texto_original.encode('utf-8'))
print(f"🔒 Criptografado: {criptografado.hex()}")

print("[🔵] Iniciando descriptografia com V25G_Final...")
texto_recuperado = ge.decrypt(criptografado)
print(f"🔓 Texto recuperado: {texto_recuperado}")

if texto_original == texto_recuperado:
    print("✅ Sucesso: Texto original e recuperado são idênticos!")
else:
    print("❌ Falha: Texto original e recuperado são diferentes!")
    
print("🔒 Criptografia e descriptografia concluídas com sucesso.")
