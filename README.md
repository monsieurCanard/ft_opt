<div align="center">
<img width="1460" height="337" alt="Image" src="https://github.com/user-attachments/assets/a72168c2-cdf1-4af8-89cb-20cc79eeaa05" />

<h1> 🔐 ft_opt - HOTP Generator </h1>
</div>

<div align="center">
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version">
  <img src="https://img.shields.io/badge/Status-Active-success.svg?style=for-the-badge" alt="Status">
</p>
<h2>Générateur de mots de passe à usage unique basé sur HOTP (RFC 4226)</h2>

[Features](#features) • [Installation](#installation) • [Usage](#usage) • [Web Interface](#web-interface)


</div>

---

## 📋 Table des matières

- [Qu'est-ce que HOTP ?](#quest-ce-que-hotp-)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [CLI Mode](#cli-mode)
  - [Web Interface](#web-interface)
- [Architecture](#architecture)
- [Algorithme](#algorithme)

---

## Qu'est-ce que HOTP ?

**HOTP** (HMAC-Based One-Time Password) est un algorithme standardisé ([RFC 4226](https://tools.ietf.org/html/rfc4226)) de génération de mots de passe à usage unique basé sur un compteur. Il utilise **HMAC-SHA1** pour créer des codes temporaires à 6 chiffres.

### Principe de fonctionnement

```
┌─────────────┐     ┌──────────┐     ┌──────────────┐
│ Secret Key  │────▶│ HMAC-SHA1│────▶│   Truncate   │
└─────────────┘     └──────────┘     └──────────────┘
       ▲                  ▲                   │
       │                  │                   ▼
┌─────────────┐          │           ┌──────────────┐
│  Counter    │──────────┘           │  6-digit OTP │
└─────────────┘                      └──────────────┘
```

1. **Clé secrète** : Une clé de 64 caractères hexadécimaux (256 bits)
2. **Compteur** : Un nombre qui s'incrémente à chaque génération
3. **HMAC-SHA1** : Hash cryptographique de la clé + compteur
4. **Dynamic Truncation** : Extraction de 4 octets depuis l'offset dynamique
5. **Modulo 1000000** : Génère un code à 6 chiffres (000000 - 999999)

---

### Features

- ✅ **CLI Mode** : Génération de clés et codes HOTP en ligne de commande
- ✅ **Web Interface** : Interface web moderne et animée
- ✅ **QR Code Generation** : Génération automatique de QR codes compatibles avec Google Authenticator
- ✅ **Auto-increment Counter** : Compteur auto-incrémenté à chaque génération
- ✅ **RFC 4226 Compliant** : Implémentation conforme au standard HOTP

---

## Installation

### Prérequis

- Python 3.8+
- pip

### Installation des dépendances

```bash
# Cloner le repository
git clone https://github.com/monsieurCanard/ft_opt.git
cd ft_opt

# Créer un environnement virtuel (recommandé)
python3 -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .venv\Scripts\activate   # Windows

# Installer les dépendances
pip install -r requirements.txt
```

---

## Usage

### CLI Mode

#### 1. Générer et sauvegarder une clé

```bash
python3 srcs/prog.py -g key.txt
```

**Exemple de fichier `key.txt` :**
```
0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
```

✅ **Résultat** : Crée un fichier `ft_opt.key` avec la clé et le compteur initialisé à 0

#### 2. Générer un code HOTP

```bash
python3 srcs/prog.py -k ft_opt.key
```

**Output :**
```
Generated HMAC-SHA1: f053922442311213163d796cfa1de9d3bcd7444b
Temporary Password: 027898
New Counter Value: 1
```

Le compteur s'incrémente automatiquement après chaque génération.

#### 3. Générer un QR Code

```bash
python3 srcs/prog.py -k ft_opt.key
```

✅ **Résultat** : Génère un QR code dans `srcs/static/qrcode.png` compatible avec :
- Google Authenticator
- Authy
- Microsoft Authenticator
- FreeOTP

### Web Interface

#### Lancer le serveur Flask

```bash
python3 srcs/app.py
```

Accédez à l'interface web : **https://code.duckiverse.com**

#### Fonctionnalités

1. **Generate New Key** : Entrez une clé hexadécimale de 64 caractères
2. **Generate HOTP & QR Code** : Génère un code OTP et un QR code scannable
3. **Modern UI** : Interface animée avec transitions fluides

<!-- Screenshot placeholder -->
<!-- ![Interface Screenshot](docs/screenshot.png) -->
*📸 Screenshot de l'interface à venir*

---

## Architecture

```
ft_opt/
├── srcs/
│   ├── app.py              # Flask web server
│   ├── prog.py             # Core HOTP logic
│   ├── parser.py           # CLI argument parser
│   ├── static/             # Static assets
│   │   ├── qrcode.png      # Generated QR codes
│   │   └── background.svg  # Background image
│   └── templates/
│       ├── index.html      # Web interface
│       └── style.css       # Custom styles
├── ft_opt.key              # Generated key file
├── key.txt                 # Input key file
└── README.md
```

---

## Algorithme

### Implémentation HOTP (RFC 4226)

```python
# 1. Générer HMAC-SHA1
HMAC = HMAC-SHA1(secret_key, counter)

# 2. Dynamic Truncation
offset = HMAC[19] & 0x0F
truncated = HMAC[offset:offset+4]

# 3. Générer le code
code = (int(truncated) & 0x7FFFFFFF) % 1_000_000
```

### Format du fichier `.key`

```
<64_caracteres_hexadecimaux>
<compteur>
```

**Exemple :**
```
0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef
0
```

### URI Format pour QR Code

```
otpauth://hotp/ft_opt?secret=<base32_key>&counter=<N>&algorithm=SHA1&digits=6
```

---

## 🛠️ Technologies

- **Python 3** : Core language
- **Flask** : Web framework
- **qrcode** : QR code generation
- **Pillow** : Image processing
- **HMAC-SHA1** : Cryptographic hashing
- **TailwindCSS** : Modern styling
 ---
<div align="center" style="display: flex; flex-direction: column; align-items: center; gap: 10px; margin-top: 20px;">
• Fait avec ❤️ par monsieurCanard •
⭐ N'oubliez pas de star le projet si vous l'aimez ! ⭐

</div>

