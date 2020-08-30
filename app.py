# 2020 Daniel Duncan
# Provides the functionality for a web based blockchain application


# library imports
# date and time library
import datetime
# web serving library
from flask import render_template, redirect, request
# time library
import time
# hashing library
import hashlib
# json library to convert between datatypes required for effective hashing
import json
# imports Flask for serving
from flask import Flask


# instantiation of node
app = Flask(__name__)

# web serving with flask
# routes the serving to http://127.0.0.1:5000/
@app.route('/')
# simple function to initialise and return that the serving is working correctly
def init():
    return 'working!'

# function which rules time within the blockchain, hence the name chrono
def chrono():
    # current time since the epoch (formatted as DAY/MONTH/DATE/TIME/YEAR)
    std_time = time.ctime()
    # when the blockchain's genesis occurred, relative to the epoch (in seconds)
    global time_of_genesis
    time_of_genesis = time.time()
    # printouts are mostly for debugging but also to show off
    print("initialised " + std_time)
    # time since genesis occurred - if the program is running correctly it should be 0
    global time_since_genesis
    time_since_genesis = time.time() - time_of_genesis

    print("it has been " + str(time_since_genesis) + " seconds since genesis")

# makes variables and relevant functions to blocks modular
class block:

    def __init__(self, index, hash, previous_hash, value, timestamp):
        print("\nblocks are initialising")
        # index of the block relative to the genesis block
        self.index = index
        # unique hash of the block
        # needs to be renamed from hash in the future - due to potential interactions with the hash function
        self.hash = hash
        # hash of the previous block in the blockchain - this allows the linking of blocks
        self.previous_hash = previous_hash
        # value of the block attributed by the user
        self.value = value
        # time of the blocks creation, relative to when the blockchain's creation (genesis) occurred
        self.timestamp = timestamp
        print("blocks are initialised")

    # generates the hash for a block
    def block_hash(self):
        # block previous to the current block
        last_block = self.chain[-1]
        # index of the current block
        new_index = last_block.index + 1
        # current blocks index but converted into the right datatype
        identifier_hash = json.dumps(new_index, sort_keys=True).encode()
        # hashes the converted index
        identifier_hash = hashlib.sha256(identifier_hash).hexdigest()

        return identifier_hash


# makes variables and relevant functions to the blockchain modular
class blockchain:

    def __init__(self):
        print("\nblockchain is initialising")
        # array which represents the blockchain itself
        self.chain = []
        # array which holds all current transactions
        self.current_transactions = []
        print("blockchain is initialised")

    # creates the genesis block upon running the program
    def create_genesis_block(self):
        genesis_block = block(0, '', '', 'GENESIS BLOCK', time_since_genesis)
        # appends the new genesis block to the blockchain
        self.chain.append(genesis_block)
        print("\ngenesis block initialised")

    # creates new blocks
    def new_block(self):
        # last_block is the block previous to the current block
        last_block = self.chain[-1]
        # new_index is the index of the current block
        new_index = last_block.index + 1
        # new_hash is the generated hash for the new block
        # could this be any less secure
        new_hash = block.block_hash(self)
        # new_value takes a user input value for the blocks value
        new_value = input('enter the value of the block\n')
        # block_timestamp is the time of the blocks creation, relative to when the blockchain's creation (genesis) occurred
        block_timestamp = time.time() - time_of_genesis

        new_block = block(new_index, new_hash, last_block.hash,
                          new_value, block_timestamp)
        # appends the new block to the blockchain
        self.chain.append(new_block)

# startup function for the program
def start_up():

    chrono()

    global blockchain

    # instantiation of blockchain
    blockchain = blockchain()

    blockchain.create_genesis_block()

# prints the blockchains contents
def print_chain():

    chain = blockchain.chain

    # the length of the blockchain (how many blocks it has in it)
    length = len(chain)

    position = 0
    
    # iterates through the blockchain printing the contents of each block
    while(position <= length):

        if position <= length-1:

            block = chain[position]

            print('\nindex: ', block.index, '\nhash: ', block.hash, '\nprevious hash: ',
                  block.previous_hash, '\nvalue: ', block.value, '\ntimestamp: ', block.timestamp, '\n')

            position = position + 1

        else:

            break

# takes user input commands
def commands():

    while True:

        # prompts a user input
        user_choice = input(
            '\nwhat do you wish to do?\nenter 1 to print the blockchain\nenter 2 to add a new block to the blockchain\nenter EXIT to exit the program\n')

        # prints the blockchains contents
        if user_choice == '1':

            print_chain()

        # creates a new block
        if user_choice == '2':

            blockchain.new_block()
        
        # exits the program
        if user_choice == 'EXIT':

            return False


start_up()

commands()
