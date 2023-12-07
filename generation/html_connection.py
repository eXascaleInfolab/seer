from flask import Flask, request
import subprocess
from run_pretrained import run_pretrained_
app = Flask(__name__)
import toml

config = toml.load('./config.toml')['generation']
num_hashtables_default = int(config['num_hashtables'])
nb_top_default = int(config['n_top'])
hash_length_percentage_default = int(config['hash_length_percentage'])


@app.route('/run-pretrained')
def run_pretrained():
    # Capture arguments from URL query parameters
    seed = request.args.get('seed', 'bafu')
    len_ts = int(request.args.get('len_ts', '200'))
    nb_ts = int(request.args.get('nb_ts', '1'))
    num_hashtables_ = int(request.args.get('num_hashtables', num_hashtables_default))
    nb_top_ =   int(request.args.get('nb_top', nb_top_default))
    hash_length_percentage_ =  int(request.args.get('hash_length_percentage', hash_length_percentage_default))
    # Add more arguments as needed


    run_pretrained_(seed,len_ts=len_ts,nb_ts=nb_ts,
                    num_hashtables_ = num_hashtables_, nb_top_=nb_top_ ,hash_length_percentage_=hash_length_percentage_)
    # Run the subprocess and capture output

    # Return the captured output


    return "STATUS : OK"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
