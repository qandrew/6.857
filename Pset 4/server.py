from flask import abort, Flask, jsonify, request
from os import urandom
from struct import unpack
from speck import leak
from speck import ones

def randomUint64():
    return unpack("<Q", urandom(8))[0]

r = 32              # num of rounds
a = randomUint64()  # high 64 bits of secret key
b = randomUint64()  # low 64 bits of secret key
print 'HIGH a={0:064b}'.format(a)
print 'LOW  b={0:064b}'.format(b)

app = Flask(__name__)

@app.route('/')
def index():
    num = request.args.get('num', '')
    try:
        num = int(num)
    except ValueError:
        abort(400)
    if (num > 10000):
        abort(400)

    samples = []
    for i in range(num):
        x = randomUint64()      # high 64 bits of plaintext
        y = randomUint64()      # low 64 bits of plaintext
        o = leak(a, b, x, y, r) # num of ones in the XOR outputs
        samples.append((x, ones(x), y, ones(y), o))
    return jsonify(samples)

if __name__ == '__main__':
    app.run(port=4000)