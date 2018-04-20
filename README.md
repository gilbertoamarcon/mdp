# Mdp

Synthesize parking MDP problem using parameters in the ```problems/parking.yaml``` file into  ```problems/parking.txt```:
```
python src/generate_parking.py -i problems/parking.yaml -o problems/parking.txt
```

Solve the parking MDP problem ```problems/parking.txt``` with discount rate ```0.9```, and store policy to CSV file ```sols/parking_policy.csv```:
```
python src/solve.py -i problems/parking.txt -d 0.9 -o sols/parking_policy.csv
```

Analyse the results of the policy CSV file ```sols/parking_policy.csv```:
```
python src/analyse_parking.py -i problems/parking.yaml -s sols/parking_policy.csv
```
