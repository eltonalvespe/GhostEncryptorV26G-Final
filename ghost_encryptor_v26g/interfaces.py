# interfaces.py

from abc import ABC, abstractmethod
# IGhostEncryptor
# A classe IGhostEncryptor define a interface para criptografia e descriptografia.
# Ela é uma classe abstrata que deve ser implementada por qualquer classe que
# deseje fornecer funcionalidades de criptografia e descriptografia.
# Ela define os métodos encrypt_text e decrypt_text, que devem ser implementados
# pelas subclasses.
# A implementação é baseada em conceitos de criptografia moderna e técnicas de segurança.
class IGhostEncryptor(ABC):
    @abstractmethod
    def encrypt_text(self, plaintext: str) -> bytes: pass

    @abstractmethod
    def decrypt_text(self, ciphertext: bytes) -> str: pass
