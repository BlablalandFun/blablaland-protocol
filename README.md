# Blablaland Protocol

Ces classes servent à encoder et à décoder les paquets communiqués entre le client (chat.swf) et le serveur.

Pour le moment, ces classes sont disponibles en:
- Python3

Utilisation
--

**PYTHON3**

    from Binary import Binary
    packet = Binary()
    packet.writeIdentity(20, 20)
    print(packet.bytes)

Ce code permet de générer les données pour le paquet (20, 20).

(c) 2019 - Yovach
