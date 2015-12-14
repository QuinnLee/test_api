#!/bin/bash

# Post some data to the 'echo' endpoint. This should return the same data back in response.
curl -H "Content-Type: application/json" -X POST -d '{"foo":"bar"}' localhost:5000/api/v1.0/echo

# Get some data from the 'random' endpoint
curl -H "Content-Type: application/json" -X GET localhost:5000/api/v1.0/random
