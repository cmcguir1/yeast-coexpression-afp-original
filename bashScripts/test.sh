#!/bin/bash
ncat -z -w5 janus24.cs.trinity.edu 22
    if [ $? -eq 0 ]; then
        echo "SSH is open"
        exit 0
    else
        echo "SSH is not open"
        exit 1
    fi