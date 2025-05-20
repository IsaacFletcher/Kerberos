#### Okay so lets implement Kerberos authentication

**We will need some applications and services**

## Client 

- Client application 

## Key Distribution Center (KDC)
- Authentication Service (AS)
- Ticket Granting Service

## Services

- Service Application to authenticate to

## Administrtion

- A database to store users and their secrets
- An application to add new users
------------------------------------------------------

Lets start with the administration part because we can't start Kerberos without users and a database

so let's start with createPrincipal.py which will take a few arguments to create a user and derive the secret key from the password and store it in a json file (as this is a prototype we'll replace a traditional kbx database with just a json file.)
we'll use argon2 for deriving the secret key by taking the user's password adding a salt which is the kdc realm.
After that we will write to a json file or create if non-existant the username, userID, secret, created timestamp and validity timestamp

