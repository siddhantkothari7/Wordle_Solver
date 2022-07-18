# Wordle Solver

This project allows you to quickly use solver to get the correct guess for Wordle using SeleniumBase and pytest.

The solver uses a greedy approach that significantly reduces the word space in the first 3 tries.

Upon running, it also saves a log of the correct word and the number of attempts.

## Build and run

### To Run Locally:

```bash
$> pip install -r requirements.txt
$> pytest wordle_solver.py
```

### To Run in Headless Mode:

```bash
$> pip install -r requirements.txt
$> pytest --headless wordle_solver.py
```

## Scope

- I would like to dynamically pick the first 3 words such that the word space is reduced with regards to the current instance.
- Make improvements to the algorithm
- Create different algorithm benchmarks
- Run the solver script daily when the new Wordle releases