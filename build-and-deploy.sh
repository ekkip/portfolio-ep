#!/bin/bash
# Build and deploy script - uses Python for reliable cache-busting
cd "$(dirname "$0")"
python3 build-and-deploy.py
