from flask import Flask, request, render_template
from main import generate_totp, generate_qrcode, save_key_from_file
import time

app = Flask(__name__)


@app.route("/")
def index():
    one_time_code = generate_totp("ft_otp.key")
    generate_qrcode("ft_otp.key")
    remaining_time = 30 - int(time.time() % 30)
    return render_template(
        "index.html",
        hotp_code=one_time_code,
        qrcode_exists=True,
        remaining_time=remaining_time,
    )

    # return render_template("index.html")


@app.route("/generate")
def generate():
    one_time_code = generate_totp("ft_otp.key")
    generate_qrcode("ft_otp.key")
    remaining_time = 30 - int(time.time() % 30)
    return render_template(
        "index.html",
        hotp_code=one_time_code,
        qrcode_exists=True,
        remaining_time=remaining_time,
    )


@app.route("/generate_key", methods=["POST"])
def generate_key():
    key_input = request.form.get("key_input")
    success = False
    message = "No key provided."

    hotp_code = None
    qrcode_exists = False
    remaining_time = None

    if key_input:
        with open("ft_otp.key", "w") as file:
            file.write(key_input)

        if save_key_from_file("ft_otp.key"):
            success = True
            message = "Key successfully saved and encrypted."

            # Generate OTP and QR Code immediately
            hotp_code = generate_totp("ft_otp.key")
            generate_qrcode("ft_otp.key")
            remaining_time = 30 - int(time.time() % 30)
            qrcode_exists = True
        else:
            success = False
            message = "Error: Key must be 64 hexadecimal characters."

    return render_template(
        "index.html",
        key_success=success,
        key_message=message,
        key_attempted=True,
        hotp_code=hotp_code,
        qrcode_exists=qrcode_exists,
        remaining_time=remaining_time,
    )


if __name__ == "__main__":
    app.run(debug=True)
