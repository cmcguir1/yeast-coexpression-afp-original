import torch

# This import should fix the ssl import verificiation error
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

#This has to be run in a main thread otherwise you get an error
def main():
    pass

if __name__ == '__main__':
    main()
