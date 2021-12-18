#!/bin/bash

echo 'yes' | python3 manage.py flush

./scripts/load_prod_fixtures.sh