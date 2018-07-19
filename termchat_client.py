# !/usr/bin/python
import os, sys, getpass
from Crypto.Cipher import AES

def new_user (user_name):
    # This function is called if the user wishes to create a new profile.

    passphrase = getpass.getpass ("Enter passphrase: ")
    while len (passphrase) < 5:
        print ("Your passphrase should be more than 4 characters long! ")
        passphrase = getpass.getpass ("Enter passphrase: ")
        pass

    new_profile = open (user_name + '.dat', "w+")
    return passphrase, new_profile;

def existing_user (user_name):
    # This function is called when a data file for the given username
    # is found.

    passphrase = getpass.getpass ("Enter passphrase: ")

    profile = open (user_name + '.dat', "r")
    return passphrase, profile;

def start_conversation (user_name, profile_data):
    # Start a conversation with a specified user.

    # Request which user the message should be sent to.
    recv_user = raw_input ("\nTo whom do you wish to send a message? ")
    search_string = '#### To ' + recv_user + ' ####'
    split_data = profile_data.split ("\n")

    # If the user exists, display past messages, otherwise
    # add an entry to the profile_data text string.

    if search_string in split_data:
        start_index = split_data.index (search_string)
        conversation_begin_index = start_index

        print (split_data[start_index])
        start_index += 1

        while split_data[start_index][0:4] != "####":
            print (split_data[start_index])
            start_index += 1
            try:
                char_c = split_data[start_index]
            except IndexError:
                break
            pass

        conversation_end_index = start_index - 1
    else:
        # profile_data = profile_data + '\n#### To ' + recv_user + ' ####\n'
        split_data.append ('\n#### To ' + recv_user + ' ####')
        start_index = len (split_data) + 1

    # Create a prompt that accepts messages until the
    # user enters 'exit()'

    print ('Enter "exit()" without quotes when you wish to exit.')
    print ('Conversation with ' + recv_user + ': ')
    line = raw_input (user_name + ">> ")

    if line != 'exit()':
        # profile_data = profile_data + user_name + ': ' + line + '\n'
        split_data.insert (start_index, user_name + ': ' + line)
        start_index += 1
    else:
        print ('Leaving conversation...\n')

    while line != 'exit()':
        line = raw_input (user_name + ">> ")
        if line != 'exit()':
            # profile_data = profile_data + user_name + ': ' + line + '\n'
            split_data.insert (start_index, user_name + ': ' + line)
            start_index += 1
        else:
            print ('Leaving conversation...\n')
        pass

    profile_data = "\n".join (split_data)

    return profile_data;

def save_profile (passphrase, profile_data):
    # This function encrypts the final text buffer and saves it to the file

    file.write (profile_data)
    return;

############################# START OF SCRIPT #############################

print ('\n########################################################')
print ("Welcome to TermChat! Developed for a more secure world. \n")
user_name = raw_input ("Enter username: ")

if os.path.isfile (user_name + '.dat') == True:
    passphrase, file = existing_user (user_name)
    profile_data = file.read()
    file.close()
    file = open (user_name + '.dat', "w")
else:
    ch = raw_input ("This user does not exist! Create a new ID? (Y/N): ")
    if ch == 'Y':
        passphrase, file = new_user (user_name)
        print ('Here')
        file.write ("Message data for %s: \n" % (user_name))
        profile_data = ''
    elif ch == 'N':
        print ("User ID not found, exiting.\n")
        exit()

# if profile_data:
#     print ('\n' + profile_data)

while raw_input ("Do you wish to send a message? (Y/N): ") == 'Y':
    profile_data = start_conversation (user_name, profile_data)
    save_profile (passphrase, profile_data)
    pass

else:
    print ("Exiting...")
    print ('########################################################\n')
    exit()
