# 2020 Daniel Duncan
# Provides the functionality for a web based blockchain application

import datetime
# from app import app
from flask import render_template, redirect, request
import time
import hashlib
import json

from flask import Flask


# instantiation of node
app = Flask(__name__)

# flask stuff
@app.route('/')
def init():
    return 'working!'

@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    post_content = request.form["content"]
    required_fields = ["content"]

    post_object = {
        'author': author,
        'content': post_content,
    }

    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)

    requests.post(new_tx_address,
                json=post_object,
                headers={'content_type': 'application/json'})

    # return to homepage
    return redirect(['/'])


def chrono():

    std_time = time.ctime()

    global time_of_genesis

    time_of_genesis = time.time()

    print("initialised " + std_time)

    global time_since_genesis

    time_since_genesis = time.time() - time_of_genesis

    print("it has been " + str(time_since_genesis) + " seconds since genesis")


class block:

    def __init__(self, index, hash, previous_hash, value, timestamp):
        print("\nblocks are initialising")
        self.index = index
        # calling it hash is going to backfire
        self.hash = hash
        self.previous_hash = previous_hash
        self.value = value
        self.timestamp = timestamp
        print("blocks are initialised")

    def block_hash(self):
        last_block = self.chain[-1]
        new_index = last_block.index + 1

        identifier_hash = json.dumps(new_index, sort_keys=True).encode()
        identifier_hash = hashlib.sha256(identifier_hash).hexdigest()

        return identifier_hash

    # crap
    def last_block(self):

        return self.chain[-1]


class blockchain:

    def __init__(self):
        print("\nblockchain is initialising")
        self.chain = []
        self.current_transactions = []
        print("blockchain is initialised")

    def create_genesis_block(self):
        genesis_block = block(0, '', 0, 0, time_since_genesis)
        self.chain.append(genesis_block)
        print("\ngenesis block initialised")

    # also crap
    def new_block(self):
        last_block = self.chain[-1]

        new_index = last_block.index + 1

        # could this be any less secure
        new_hash = block.block_hash(self)

        new_value = input('enter the value of the block\n')

        block_timestamp = time.time() - time_of_genesis

        new_block = block(new_index, new_hash, last_block.hash,
                          new_value, block_timestamp)

        self.chain.append(new_block)


def start_up():

    chrono()

    global blockchain

    # instantiation of blockchain
    blockchain = blockchain()

    blockchain.create_genesis_block()


def print_chain():

    chain = blockchain.chain

    length = len(chain)

    position = 0

    print('genesis block:')

    while(position <= length):

        if position <= length-1:

            block = chain[position]

            print(' index: ', block.index, '\n', 'hash: ', block.hash, '\n', 'previous hash: ',
                  block.previous_hash, '\n', 'value: ', block.value, '\n', 'timestamp: ', block.timestamp, '\n')

            position = position + 1

        else:

            break


def commands():

    while True:

        user_choice = input(
            '\nwhat do you wish to do?\nenter 1 to print the blockchain\nenter 2 to add a new block to the blockchain\nenter EXIT to exit the program\n')

        if user_choice == '1':

            print_chain()

        # very crap
        if user_choice == '2':

            blockchain.new_block()

        if user_choice == 'EXIT':

            return False


start_up()

commands()
