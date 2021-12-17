#!/usr/bin/env python3

from getpass import getpass

from aws_lambda.credentials_store import CredentialsStore


def main():
    store = CredentialsStore(credentials_file="aws_lambda/.passwd")

    print("Welcome to the basic password manager.")
    print("Please enter your username:")
    username = input()
    print("Please enter your password:")
    password = getpass()

    store.add(username, password)
    store.save()


if __name__ == "__main__":
    main()
