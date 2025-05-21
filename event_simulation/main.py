import copy
import random
import uuid
from pathlib import Path
from datetime import datetime
from event_simulation.node import Node
from event_simulation.simulation import simulate_case

# To get exactly the same results from a specific run,
# just use the same seed, same parameters, and same nodes.

# Simulation hours
T = 100000.0*0.1
seed = random.randint(1, 100000) # generate a random seed
random.seed(seed)
print(f"Semilla aleatoria: {seed}")

# External arrival parameters (patients/hour)
lambda1 = 4.0 # to reg1
lambda2 = 3.0 # to reg2

# Base model
nodes_base = {
    'reg1':    Node('reg1',     mu=8.0,  servers=1),
    'reg2':    Node('reg2',     mu=10.0, servers=1),
    'exam1':   Node('exam1',    mu=6.0,  servers=1),
    'exam2':   Node('exam2',    mu=6.0,  servers=1),
    'consult1':Node('consult1', mu=2.5,  servers=2),
    'consult2':Node('consult2', mu=3.0,  servers=2),
}

# Solution 3 model
nodes_solution3 = copy.deepcopy(nodes_base)

# Solution 4 model
nodes_solution4 = copy.deepcopy(nodes_solution3)

# Solution 5 model
nodes_solution5 = {
    'reg1':    Node('reg1',     mu=8.0,  servers=1),
    'reg2':    Node('reg2',     mu=10.0, servers=1),
    'exam':    Node('exam',     mu=6,    servers=2),
    'consult1':Node('consult1', mu=2.5,  servers=2),
    'consult2':Node('consult2', mu=3.0,  servers=2),
}

# Create a directory for the execution results inside "runs"
timestamp = datetime.now().strftime("%d-%m-%Y %H_%M_%S") # current date
unique_id = uuid.uuid4().hex[:6] # unique ID

# Create the common folder using timestamp and unique_id 'runs/{timestamp} {unique_id}'
run_dir = Path("runs") / f"{timestamp} {unique_id}"
run_dir.mkdir(parents=True, exist_ok=True)

# Base case
base_metrics = simulate_case(
    "base", T, lambda1, lambda2, copy.deepcopy(nodes_base),
    save_results=True, run_dir=run_dir, seed=seed,
)

# Solution case 3
# Use Lq from the base simulation to calculate the proportion of patients
# going to consult1
L_q1 = base_metrics['consult1']['Lq']
L_q2 = base_metrics['consult2']['Lq']
p_to_consult1 = L_q2 / (L_q1 + L_q2)
print(f"Proportion of patients going to consult1: {p_to_consult1:.4f}")
solution3_metrics = simulate_case(
    "solution3", T, lambda1, lambda2, copy.deepcopy(nodes_solution3),
    p_to_consult1=p_to_consult1,
    save_results=True, run_dir=run_dir, seed=seed,
)

# Solution case 4
# Use mu to calculate the proportion of patients going to consult1
mu1 = nodes_base['consult1'].mu
mu2 = nodes_base['consult2'].mu
p_to_consult1 = mu1 / (mu1 + mu2)
print(f"Proportion of patients going to consult1: {p_to_consult1:.4f}")
solution4_metrics = simulate_case(
    "solution4", T, lambda1, lambda2, copy.deepcopy(nodes_solution4),
    p_to_consult1=p_to_consult1,
    save_results=True, run_dir=run_dir, seed=seed,
)

# Solution case 5
# Use the same p_to_consult1 as solution 4
print(f"Proportion of patients going to consult1: {p_to_consult1:.4f}")
solution5_metrics = simulate_case(
    "solution5", T, lambda1, lambda2, copy.deepcopy(nodes_solution5),
    p_to_consult1=p_to_consult1,
    save_results=True, run_dir=run_dir, seed=seed,
)