#written by Severyn Kozak with the help of Andrew Xia, Ray Wang

NUM_CIPHERS = 10
cipher_msgs = []
with open("tenciphs.txt") as tenciphs_file:
	for ln in tenciphs_file:
		cipher_msg = [int(hex_str, 16) for hex_str in ln.strip().split()]
		cipher_msgs.append(cipher_msg)

g = [95, 243, 167, 123, 174, 143, 138, 252, 234, 67, 221, 53, 51, 12, 115, 14, 247, 196, 230, 11, 151, 80, 74, 39, 245, 24, 110, 10, 212, 69, 203, 66, 194, 127, 197, 206, 153, 60, 48, 228, 249, 56, 172, 31, 111, 9, 8, 1, 17, 164, 88, 150, 180, 103, 205, 132, 32, 46, 159, 91, 175, 144, 222, 118, 215, 250, 156, 6, 23, 109, 237, 99, 130, 105, 204, 147, 121, 236, 33, 41, 113, 141, 40, 216, 83, 152, 82, 47, 137, 44, 210, 161, 92, 68, 73, 19, 192, 134, 61, 136, 186, 165, 217, 89, 38, 50, 112, 154, 128, 160, 149, 176, 75, 43, 4, 133, 131, 218, 21, 35, 13, 169, 117, 25, 240, 190, 84, 201, 185, 49, 20, 241, 79, 214, 191, 106, 126, 37, 65, 78, 90, 125, 171, 85, 42, 81, 120, 142, 87, 251, 77, 96, 140, 104, 158, 36, 34, 232, 227, 7, 107, 187, 27, 168, 231, 155, 195, 54, 63, 52, 181, 253, 15, 116, 226, 193, 93, 229, 57, 244, 72, 139, 146, 124, 220, 26, 101, 129, 145, 58, 223, 173, 208, 114, 162, 122, 255, 102, 30, 213, 235, 100, 199, 239, 76, 5, 207, 224, 45, 248, 211, 188, 86, 182, 16, 184, 3, 179, 119, 183, 200, 59, 178, 209, 177, 166, 108, 97, 148, 70, 135, 238, 233, 219, 94, 55, 2, 29, 189, 0, 28, 246, 202, 18, 198, 98, 71, 62, 225, 64, 170, 163, 242, 254, 157, 22]
possible_pads_per_byte = []

print("Brute-forcing possible pad values.")
for byte_ind in range(1, len(cipher_msgs[0])):
	possible_pads = set()
	for p in range(256):
		possible_p = True

		for cipher_ind in range(NUM_CIPHERS):
			prev_cipher_byte = cipher_msgs[cipher_ind][byte_ind - 1]
			cipher_byte = cipher_msgs[cipher_ind][byte_ind]
			q = g[p ^ prev_cipher_byte]

			any_m = False
			for m in range(32, 127):
				if m ^ q == cipher_byte:
					any_m = True
					break

			if not any_m:
				possible_p = False

		if possible_p:
			possible_pads.add(p)

	possible_pads_per_byte.append(possible_pads)

print("Decrypting ciphertexts:")
for msg_ind in range(10):
	decoded_msg = ""
	for ind, possible_pads in enumerate(possible_pads_per_byte):
		real_ind = ind + 1
		if len(possible_pads) == 1:
			pad = list(possible_pads)[0]
			prev_c_byte = cipher_msgs[msg_ind][real_ind - 1]
			c_byte = cipher_msgs[msg_ind][real_ind]
			q = g[pad ^ prev_c_byte]
			decoded_msg += chr(c_byte ^ q)
		else:
			decoded_msg += "_"

	print("Msg {}: {}".format(msg_ind + 1, decoded_msg))
