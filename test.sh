#!/bin/bash

curl -H "Content-Type: application/json" -X POST -d '{"foo":"bar"}' localhost:5000/api/v1.0/echo

curl -H "Content-Type: application/json" -X GET localhost:5000/api/v1.0/random
