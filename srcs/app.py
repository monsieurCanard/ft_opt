from flask import Flask, request, render_template, send_file
from prog import generate_hotp, generate_qrcode, save_key_from_file

app = Flask(__name__)

@app.route("/")
def index():
		return render_template("index.html")

@app.route("/generate")
def generate():
		one_time_code = generate_hotp('ft_opt.key')
		generate_qrcode()
		return render_template("index.html", hotp_code=one_time_code, qrcode_exists=True)

@app.route("/generate_key", methods=['POST'])
def generate_key():
		key_input = request.form.get('key_input')
		if key_input:
			with open ('ft_opt.key', 'w') as file:
				file.write(key_input + '\n0\n')
				save_key_from_file('ft_opt.key')
			
		return render_template("index.html")

if __name__ == "__main__":
		app.run(debug=True)