# delonghi-comfort-client

Delonghi Tasciugo AriaDry Multi DDSX220WF API Client

## Description

Simple script to interact with the Delonghi `aylanetworks` APIs.
This script focuses on the DDSX220WF model, but it is very similar and can work with other Delonghi products like coffee machines.

The script receives your credentials as input and authenticates with the API,
storing locally a refresh token (under `refresh_token.txt`) that is reused if present in subsequent calls.

In case you don't have an account it also automates the creation process,
but to add your devices to the account you need to use the mobile app before being able to use the client.

## Usage

```
python3 cli.py
```

## References

- [duckwc/ECAMpy](https://github.com/duckwc/ECAMpy), used to bootstrap the initial code to convert auth code to the API token
- [aylanetworks API Reference](https://docs.aylanetworks.com/reference)
