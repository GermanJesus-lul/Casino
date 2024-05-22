from flask import request, Blueprint
import git
import hmac
import hashlib

autodeployment = Blueprint('autodeployment', __name__)


# check signature of GitHub webhook call
def is_valid_signature(x_hub_signature, data, private_key):
    # x_hub_signature and data are from the webhook payload
    # private key is your webhook secret
    hash_algorithm, github_signature = x_hub_signature.split('=', 1)
    algorithm = hashlib.__dict__.get(hash_algorithm)
    encoded_key = bytes(private_key, 'latin-1')
    mac = hmac.new(encoded_key, msg=data, digestmod=algorithm)
    return hmac.compare_digest(mac.hexdigest(), github_signature)


@autodeployment.route('/update_server', methods=['POST'])
def update_server():
    if request.method == 'POST':
        x_hub_signature = request.headers.get('X-Hub-Signature')
        if x_hub_signature is None:
            return 'Invalid call', 400
        if not is_valid_signature(x_hub_signature, request.data, 'somewebhookpassword'):
            return 'Invalid signature', 400
        repo = git.Repo('/home/Betonblock/Casino')
        origin = repo.remotes.origin
        origin.pull()
        return 'Updated PythonAnywhere successfully', 200
    else:
        return 'Wrong event type', 400