# Mdp

## Homework 4

### Part II-a

Simulate the random policy ```policies/MDP-test-random.csv``` on the simple MDP problem ```problems/MDP-test.txt```:
```
python src/simulate.py -i problems/MDP-test.txt -p policies/MDP-test-random.csv
```

Simulate the optimal policy ```policies/MDP-test-optimal.csv``` on the simple MDP problem ```problems/MDP-test.txt```:
```
python src/simulate.py -i problems/MDP-test.txt -p policies/MDP-test-optimal.csv
```

### Part II-b

#### Random Policy

Simulate the random policy ```policies/parking-random.csv``` on the parking MDP problem A ```problems/parking-a.txt```:
```
python src/simulate.py -i problems/parking-a.txt -p policies/parking-random.csv
```

Simulate the random policy ```policies/parking-random.csv``` on the parking MDP problem B ```problems/parking-b.txt```:
```
python src/simulate.py -i problems/parking-b.txt -p policies/parking-random.csv
```


#### Naive Policy

Simulate the naive policy ```policies/parking-naive.csv``` on the parking MDP problem A ```problems/parking-a.txt```:
```
python src/simulate.py -i problems/parking-a.txt -p policies/parking-naive.csv
```

Simulate the naive policy ```policies/parking-naive.csv``` on the parking MDP problem B ```problems/parking-b.txt```:
```
python src/simulate.py -i problems/parking-b.txt -p policies/parking-naive.csv
```


#### Simple Policy

Simulate the simple policy ```policies/parking-a-simple.csv``` on the parking MDP problem A ```problems/parking-a.txt```:
```
python src/simulate.py -i problems/parking-a.txt -p policies/parking-a-simple.csv
```

Simulate the simple policy ```policies/parking-b-simple.csv``` on the parking MDP problem B ```problems/parking-b.txt```:
```
python src/simulate.py -i problems/parking-b.txt -p policies/parking-b-simple.csv
```

### Part III

Run all learning methods with both epsilon values and generate a plot ```plots/MDP-test.eps``` for the simple MDP problem ```problems/MDP-test.txt```:
```
python src/learn.py -i problems/MDP-test.txt -p plots/MDP-test.eps
```

Run all learning methods with both epsilon values and generate a plot ```plots/MDP-test.eps``` for the parking MDP problem A ```plots/parking-a.eps```:
```
python src/learn.py -i problems/parking-a.txt -p plots/parking-a.eps
```

Run all learning methods with both epsilon values and generate a plot ```plots/MDP-test.eps``` for the parking MDP problem B ```plots/parking-b.eps```:
```
python src/learn.py -i problems/parking-b.txt -p plots/parking-b.eps
```

## Homework 3

Synthesize parking MDP problem using parameters in the ```problems/parking-a.yaml``` file into  ```problems/parking-a.txt```:
```
python src/generate_parking.py -i problems/parking-a.yaml -o problems/parking-a.txt
```

Solve the parking MDP problem ```problems/parking-a.txt``` with discount rate ```0.9```, and store policy to CSV file ```sols/parking-a.csv```:
```
python src/solve.py -i problems/parking-a.txt -d 0.9 -o sols/parking-a.csv
```

Analyse the results of the policy CSV file ```sols/parking-a.csv```:
```
python src/analyse_parking.py -i problems/parking-a.yaml -s sols/parking-a.csv
```
