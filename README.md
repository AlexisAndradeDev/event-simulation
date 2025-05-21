# Event Simulation

A Python framework for discrete event simulations designed to model and analyze complex queuing systems.

**Currently WIP.**

## Overview

This framework allows you to define nodes representing service stations with configurable parameters such as service rates and number of servers. It simulates discrete events over a specified time horizon, tracking queue lengths, waiting times, and other performance metrics.

You can run multiple scenarios modifying parameters like arrival rates, service rates, routing probabilities, and server capacities, and compare their outcomes to optimize system performance or just create a dataset from simulated data.

## Features

- **Discrete Event Simulation** of multi-node queuing systems
- **Flexible Node Configuration** including service rate (`mu`), and number of servers (`servers`)
- **Support for Multiple Solutions / Models** to test different configurations
- **Probabilistic Routing** between nodes based on queue lengths or service rates
- **Automatic Result Saving** including performance metrics for each run
- **Run Management** organizing output into timestamped folders, uniquely identified by UUID
- **Extensible Framework** allowing easy addition of nodes or modifications to routing logic

## Usage

1. **Define node configurations:**
   - Create a model with your own external arrival rates (lambdas), service rates, servers, routing probabilities.

2. **Run simulations for your models:**
   - Use `simulate_case` function to execute and store results

3. **Analyze outputs:**
   - Metrics such as queue lengths (`Lq`), waiting times, utilizations, etc.
   - Printed summary and saved CSV files inside organized run directories

---

## Example

The `main.py` script demonstrates:

- Setting up multiple service nodes
- Running a base simulation
- Calculating routing proportions from base results or node parameters
- Running alternative solutions adjusting routing or node configurations
- Storing results in organized folders for later analysis

## Installation

This package was developed using Python 3.10.

Clone this repository and install dependencies by using:

pip install -r requirements.txt

## Running a Simulation

`python main.py`

This will run the base case and three solution scenarios, printing routing probabilities and saving results with detailed metrics in a timestamped folder within `runs/`.

## Notes

- Use a fixed random seed if you require reproducibility.
- Modify service rates, servers, and routing logic in node definitions and simulation calls to reflect new scenarios.
- Results are saved as CSV files inside uniquely named folders combining datetime and randomized UUID.

## License

BSD-3-Clause — see the `LICENSE` file for details.

## Contact / Support

For questions, bug reports, or feature requests please open an issue on GitHub or contact the maintainer.
