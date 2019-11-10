from cryptography.fernet import Fernet
import os,sys

#Used to decrypt using the summetric "rsa.pt" key (not really rsa but whatever)
def decrypt(token_encrypted):
    #Reads key from file
    try:# Try to get absolute location of encryption key file for linux
        file = open(os.path.abspath(os.path.dirname(sys.argv[0]))+"//" +"rsa.pt","rb")
    except:
        try:# Try to get absolute location of encryption key file for windows
            file = open(os.path.abspath(os.path.dirname(sys.argv[0]))+"\\" +"rsa.pt","rb")
            
        except:# if it fails ask user to provide it instead
            print("Couldn't find encrytpion key location.")
            location = input("Please specify absolute location of your key: ")
            file = open(location )
    key = file.read()
    file.close
    #Decrypts input and encodes it properly
    encrypted = token_encrypted.encode()
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    decrypted = decrypted.decode()
    return (decrypted)

