#!/bin/bash

python src/learn.py -i problems/MDP-test.txt -p plots/MDP-test.eps
python src/learn.py -i problems/parking-a.txt -p plots/parking-a.eps
python src/learn.py -i problems/parking-b.txt -p plots/parking-b.eps
