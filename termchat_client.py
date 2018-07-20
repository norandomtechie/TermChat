# !/usr/bin/python
from Crypto.Cipher import AES
import os, sys, getpass, Crypto.Random, hashlib

###########################################################################################
### https://stackoverflow.com/questions/6425131/encrypt-decrypt-data-in-python-with-salt

# salt size in bytes
SALT_SIZE = 16
# number of iterations in the key generation
NUMBER_OF_ITERATIONS = 25
# the size multiple required for AES
AES_MULTIPLE = 16

def generate_key(password, salt, iterations):
    assert iterations > 0
    key = password + salt
    for i in range(iterations):
        key = hashlib.sha256(key).digest()
    return key

def pad_text(text, multiple):
    extra_bytes = len(text) % multiple
    padding_size = multiple - extra_bytes
    padding = chr(padding_size) * padding_size
    padded_text = text + padding
    return padded_text

def unpad_text(padded_text):
    padding_size = ord(padded_text[-1])
    text = padded_text[:-padding_size]
    return text

def encrypt(plaintext, password):
    salt = Crypto.Random.get_random_bytes(SALT_SIZE)
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = pad_text(plaintext, AES_MULTIPLE)
    ciphertext = cipher.encrypt(padded_plaintext)
    ciphertext_with_salt = salt + ciphertext
    return ciphertext_with_salt

def decrypt(ciphertext, password):
    salt = ciphertext[0:SALT_SIZE]
    ciphertext_sans_salt = ciphertext[SALT_SIZE:]
    key = generate_key(password, salt, NUMBER_OF_ITERATIONS)
    cipher = AES.new(key, AES.MODE_ECB)
    padded_plaintext = cipher.decrypt(ciphertext_sans_salt)
    plaintext = unpad_text(padded_plaintext)
    return plaintext

###########################################################################################

def new_user ():
    # This function is called if the user wishes to create a new profile.

    passphrase = getpass.getpass ("Enter passphrase: ")
    while len (passphrase) < 5:
        print ("Your passphrase should be more than 4 characters long! ")
        passphrase = getpass.getpass ("Enter passphrase: ")
        pass

    return passphrase;

def existing_user ():
    # This function is called when a data file for the given username
    # is found.

    passphrase = getpass.getpass ("Enter passphrase: ")
    return passphrase;

def start_conversation (user_name, profile_data):
    # Start a conversation with a specified user.

    # Request which user the message should be sent to.
    recv_user = raw_input ("\nTo whom do you wish to send a message? ")
    search_string = '#### To ' + recv_user + ' ####'
    print ('\n')
    split_data = profile_data.split ("\n")
    # If the user exists, display past messages, otherwise
    # add an entry to the profile_data text string.

    if search_string in split_data:
        start_index = split_data.index (search_string)

        print (split_data[start_index])
        start_index += 1

        while split_data[start_index][0:4] != "####":
            print (split_data[start_index])
            start_index += 1
            try:
                char_c = split_data[start_index]
            except IndexError:      # Since the conversation length is unknown
                break               # we must wait for the index to go out of bounds.
            pass

        conversation_end_index = start_index - 1
    else:
        split_data.append ('#### To ' + recv_user + ' ####')
        start_index = len (split_data) + 1

    # Create a prompt that accepts messages until the
    # user enters '\q'

    print ('\nConversation with ' + recv_user + ': ')
    print ('Enter "\q" without quotes when you wish to exit. \n')
    line = raw_input (user_name + ">> ")

    if line != '\q':
        split_data.insert (start_index, user_name + ': ' + line)
        start_index += 1
    else:
        print ('Leaving conversation...\n')

    while line != '\q':
        line = raw_input (user_name + ">> ")
        if line != '\q':
            split_data.insert (start_index, user_name + ': ' + line)
            start_index += 1
        else:
            print ('Leaving conversation...\n')
        pass

    profile_data = "\n".join (split_data)
    print (profile_data)
    return profile_data;

def quit_app ():
    print ("Exiting...")
    print ('########################################################\n')
    exit()
    return;

############################# START OF SCRIPT #############################

print ('\n########################################################')
print ("Welcome to TermChat! Developed for a more secure world. \n")
user_name = raw_input ("Enter username: ")
ch = 'X'

if os.path.isfile (user_name + '.dat') == True:
    passphrase = existing_user ()
    file = open (user_name + '.dat', "r")
    profile_data = decrypt (file.read(), passphrase)
    # profile_data = file.read()
    file.close()
else:
    ch = raw_input ("This user does not exist! Create a new ID? (Y/N): ")
    if ch == 'Y':
        passphrase = new_user()
        file = open (user_name + '.dat', "w+")
        file.write ("Message data for %s: \n" % (user_name))
        profile_data = 'Message data for ' + user_name + ': \n'
        file.close()
    elif ch == 'N':
        print ("User ID not found.\n")
        quit_app()

login = raw_input ("Do you wish to send a message? (Y/N): ")
if login == 'Y':
    open (user_name + '.dat', "w").close()  ## Clears file

while login == 'Y':
    profile_data = start_conversation (user_name, profile_data)
    file = open (user_name + '.dat', 'w+')
    file.write (encrypt (profile_data, passphrase))
    # file.write (profile_data)
    login = raw_input ("Do you wish to send another message? (Y/N): ")
    pass

file.close()
quit_app()
