from ghost_encryptor_v26g.GhostEncryptorV26G_Final import GhostEncryptorV26G

# Inicialização do sistema com uma seed
encryptor = GhostEncryptorV26G(seed=b"seed_final_v26g")

mensagem = "GhostEncryptor V26G - Final Teste com compressão simbólica, MAC-G e cifragem GCBC!"
print("[ORIGINAL] →", mensagem)

# Criptografia
cifrado = encryptor.encrypt(mensagem)
print("[CRIPTOGRAFADO] →", cifrado[:60], "...")

# Descriptografia
decifrado = encryptor.decrypt(cifrado)
print("[DECIFRADO] →", decifrado.decode())