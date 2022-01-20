#!/bin/bash

sleep 5
fastack db upgrade
uvicorn app.main:app --workers 2 --host "0.0.0.0" --port 6700
