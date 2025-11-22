# ft_opt
HOTP (HMAC-Based One-Time Password) Generator

## Qu'est-ce que HOTP ?

HOTP est un algorithme de génération de mots de passe à usage unique basé sur un compteur (RFC 4226). Il utilise HMAC-SHA1 pour créer des codes temporaires à 6 chiffres.

### Principe de fonctionnement

1. **Clé secrète** : Une clé de 64 caractères hexadécimaux (256 bits)
2. **Compteur** : Un nombre qui s'incrémente à chaque génération
3. **HMAC-SHA1** : Hash de la clé + compteur
4. **Dynamic Truncation** : Extraction de 4 octets depuis l'offset
5. **Modulo 1000000** : Génère un code à 6 chiffres

### Algorithme

```
HMAC = HMAC-SHA1(key, counter)
offset = dernier_byte(HMAC) & 0x0F
code = (HMAC[offset:offset+4] & 0x7FFFFFFF) % 1000000
```

### Utilisation

**Sauvegarder une clé :**
```bash
python3 srcs/prog.py -g key.txt
```

**Générer un code HOTP :**
```bash
python3 srcs/prog.py -k ft_opt.key
```

### Format du fichier `.key`

```
<64_hex_chars>
<counter>
```

Le compteur s'incrémente automatiquement après chaque génération

