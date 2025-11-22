from parser import init_parser
import hashlib
import hmac
import qrcode
import base64

def save_key_from_file(file_path):
	
	with open(file_path, 'r') as file:
		key = file.readline().strip()
		
	if len(key) != 64 or not all(c in '0123456789abcdefABCDEF' for c in key):
		print("error: key must be 64 hexadecimal characters.")
	else:
		with open('ft_opt.key', 'w') as key_file:
			key_file.write(key + '\n0\n')
		print("Key saved successfully.")

def generate_hotp(key_file):
		
		with open(key_file, 'r') as file:
			key = file.readline().strip()
			counter = int(file.readline().strip())
			
		key_bytes = bytes.fromhex(key)
		counter_bytes = counter.to_bytes(8, 'big')
		
		encrypt_key = hmac.new(key_bytes, counter_bytes, hashlib.sha1).digest()

		offset = encrypt_key[-1] & 0x0F
		p = encrypt_key[offset:offset+4] 
		bin_code = (int.from_bytes(p, 'big') & 0x7FFFFFFF) % 1000000
		print(f"Temporary Password: {bin_code:06d}")

		new_counter = counter + 1
		with open(key_file, 'w') as file:
			file.write(str(key) + '\n' + str(new_counter) + '\n')
		
		return f"{bin_code:06d}"

def generate_qrcode():
	with open('ft_opt.key', 'r') as file:
		key_hex = file.readline().strip()
		counter = file.readline().strip()
	
	counter = int(counter)

	key_bytes = bytes.fromhex(key_hex)
	key_base32 = base64.b32encode(key_bytes).decode('utf-8').replace('=', '')

	
	otp_uri = f"otpauth://hotp/ft_opt?secret={key_base32}&counter={counter}&algorithm=SHA1&digits=6"
	
	try:
		img = qrcode.make(otp_uri)
		img.save('srcs/static/qrcode.png')
		print("QR Code generated and saved as qrcode.png")
	except Exception as e:
		print(f"Error generating QR Code: {e}")



def main():
	parser = init_parser()
	args = parser.parse_args()

	generate_qrcode()
	if args.g:
		save_key_from_file(args.g)
	if args.k:
		generate_hotp(args.k)


if __name__ == "__main__":
		main()