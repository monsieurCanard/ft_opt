import os
import time
from parser import init_parser
import hashlib
import hmac
import qrcode
import base64


def verify_key(key):
    if len(key) != 64 or not all(c in "0123456789abcdefABCDEF" for c in key):
        return False
    return True


def save_key_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            key = file.readline().strip()
    except Exception as e:
        print(f"error: could not read file: {e}")
        return False

    if not verify_key(key):
        print("error: key must be a 64 hexadecimal characters.")
        return False

    try:
        script_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(script_path, "..", "ft_otp.key")
        with open(path, "w") as key_file:
            key_file.write(key)
            print("Key was successfully saved in ft_otp.key")
            return True
    except Exception as e:
        print(f"error: could not write to ft_opt.key: {e}")
        return False


def generate_totp(key_file):
    if key_file != "ft_otp.key":
        print("error: key file must be named ft_otp.key")
        return None

    try:
        with open(key_file, "r") as file:
            key = file.readline().strip()
            key_bytes = bytes.fromhex(key)
            if not verify_key(key):
                print("error: key must be a 64 hexadecimal characters.")
                return None
    except Exception as e:
        print(f"error: could not read key file: {e}")
        return None

    period = 30
    time_bytes = int(time.time() // period).to_bytes(8, "big")

    encrypt_key = hmac.new(key_bytes, time_bytes, hashlib.sha1).digest()

    offset = encrypt_key[-1] & 0x0F
    p = encrypt_key[offset : offset + 4]
    bin_code = (int.from_bytes(p, "big") & 0x7FFFFFFF) % 1000000
    print(f"Temporary Password: {bin_code:06d}")
    return f"{bin_code:06d}"


def generate_qrcode(key_file):
    try:
        with open(key_file, "r") as file:
            key_hex = file.readline().strip()
            key_bytes = bytes.fromhex(key_hex)
    except Exception as e:
        print(f"error: could not read {key_file}: {e}")
        return

    period = 30
    time_bytes = int(time.time() // period).to_bytes(8, "big")

    key_base32 = base64.b32encode(key_bytes).decode("utf-8").replace("=", "")

    otp_uri = f"otpauth://totp/ft_opt?secret={key_base32}&time={time_bytes}&algorithm=SHA1&digits=6"

    try:
        img = qrcode.make(otp_uri)
        script_path = os.path.dirname(os.path.abspath(__file__))
        path = os.path.abspath(os.path.join(script_path, "static", "qrcode.png"))
        img.save(path)
        print("QR Code generated and saved as static/qrcode.png")
    except Exception as e:
        print(f"Error generating QR Code: {e}")


def main():
    parser = init_parser()
    args = parser.parse_args()

    if args.g:
        save_key_from_file(args.g)
    if args.k:
        ret = generate_totp(args.k)
        if ret:
            generate_qrcode(args.k)


if __name__ == "__main__":
    main()
