from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

def generate_keys():
    """Generate a public-private key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    public_key = private_key.public_key()
    return private_key, public_key

def sign_vote_count(vote_count, private_key):
    """Sign the vote count using the private key."""
    vote_count_bytes = str(vote_count).encode()
    signature = private_key.sign(
        vote_count_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature

def verify_vote_count(vote_count, signature, public_key):
    if signature is None:
        return vote_count == 0
    vote_count_bytes = str(vote_count).encode()
    try:
        public_key.verify(
            signature,
            vote_count_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except InvalidSignature:
        return False