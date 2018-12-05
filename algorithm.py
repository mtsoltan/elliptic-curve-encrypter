"""
import ecdsa
import base64
import hashlib
"""

P_secp265k1 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F  # 256 bits field prime.
A_secp265k1 = 0
B_secp265k1 = 7
G_secp265k1_x = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798  # 256 bits base point x coord.
G_secp265k1_y = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8  # 256 bits base point y coord.
N_secp265k1 = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141  # 256 bits order of base point.
H_secp265k1 = 1  # The cofactor of base point.

"""
Rules:
Kpub = Kpriv x G
Private keys are randomly generated, usually iterative operation of a cryptographic hash function to a password.
Hash functions are designed in such a way to provide a bitstream of sufficient length to form a key.

G is used as the generator for public keys. Multiplication is straightforward through the double-and-add method.
Private keys cannot be recreated since multiplication is irreversible.


0- Randomly generate Kpriv (int), and generate Kpub = Kpriv x G (point).


For a fixed set of paramters T = (P, A, B, G, N, H), to sign a message, m (ECDSA):
1- Select a random integer k, 1 < k <= N - 1.
2- Compute r = (k * G).x mod N
   * where multiplication is over the elliptic curve (A, B, P)
   * where if r == 0 go to step 1.
3- Compute inv(k) using xgcd, and SHA1(m) as a 160-bit integer.
4- Compue s = inv(k) * (SHA1(m) + Kpriv * r) mod N
   * where if s == 0 go to step 1.
5- The signature is (r, s).

To verify the signature (r, s) given Kpub:
1- Verify that r, s are integers in the interval [1, n - 1]
2- Compute inv(s) using xgcd, and SHA1(m) as a 160-bit integer.
3- Compute u1 = inv(s) * SHA1(m) mod N and u2 = inv(s) * r mod N
4- Compute x = (u1 * G + u2 * Kpub).x mod N.
5- Accept if x == r.


For a fixed set of paramters T = (P, A, B, G, N, H), to encrypt a message, m given Kpub:
(https://onlinelibrary.wiley.com/doi/pdf/10.1002/sec.1702):
1- Select a random integer k, 1 < k <= N - 1.
2- Compute R = k * G
2- Convert the message to points on the elliptic curve, each Pi.
3- Encrypt each point in the message, Ci = Pi + k * Kpub
4- Send R and the set C.

To decrypt the message (R, C) using Kpriv:
1- Calculate Pi = Ci - Kpriv * R

"""