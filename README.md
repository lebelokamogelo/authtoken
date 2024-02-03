## authtoken

This library provides token-based authentication for Django REST Framework applications. It allows users to obtain authentication tokens and refresh them as needed.

### Obtaining a Token

To obtain an authentication token, send a POST request to the `/api/token/` endpoint with valid user credentials. If the credentials are correct, the endpoint will return a token.
    
    {
        "username": "user",
        "password": "password"
    }

Response:
    
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NDYwMjA1NjN9.MqCr6iGn7yqMw2uGwIsdz0C8PVTp4vH0Fam0EbgPEKo"
    }

### Refreshing a Token

To refresh an authentication token, send a POST request to the /api/token/refresh/ endpoint with the current token. If the token is valid, the endpoint will return a new token.

    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NDYwMjA1NjN9.MqCr6iGn7yqMw2uGwIsdz0C8PVTp4vH0Fam0EbgPEKo"
    }

Response:
    
    {
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2NDYwMjA1NjN9.MqCr6iGn7yqMw2uGwIsdz0C8PVTp4vH0Fam0EbgPEKo"
    }

### Routes

- `/api/token/`: endpoint for obtaining an authentication token.
- `/api/token/refresh/`: endpoint for refreshing an authentication token.


### License

This project is licensed under the MIT License.