# Event Simulation

A Python framework for discrete event simulations designed to model and analyze complex queuing systems.

**Currently WIP.**

## Overview

This framework allows you to define nodes representing service stations with configurable parameters such as service rates, number of servers, external arrival rates, and customizable routing probabilities. It simulates discrete events over a specified time horizon, tracking queue lengths, waiting times, and other performance metrics.

You can run multiple scenarios modifying parameters like external arrival rates (`external_lambda`), service rates (`mu`), routing probabilities (`routing_probabilities`), and server capacities, and compare their outcomes to optimize system performance or just create a dataset from simulated data.

## Features

- **Discrete Event Simulation** of multi-node queuing systems
- **Flexible Node Configuration** including service rate (`mu`), number of servers (`servers`), external arrival rate (`external_lambda`), and routing probabilities (`routing_probabilities`)
- **Customizable Routing Logic** directly via the `routing_probabilities` attribute in each `Node` instance
- **Support for Multiple Solutions / Models** to test different configurations
- **Automatic Result Saving** including performance metrics for each run
- **Run Management** organizing output into timestamped folders, uniquely identified by UUID
- **Extensible Framework** allowing easy addition of nodes or modifications to routing logic

## Usage

1. **Define node configurations:**
   - Create a model by instantiating `Node` objects with your desired parameters including external arrival rates (`external_lambda`) and routing probabilities (`routing_probabilities`).

2. **Run simulations for your models:**
   - Use the `simulate_case` function to execute and store results, passing your configured nodes.

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

`python main.py`

This will run the base case and multiple optimized scenarios, showing and saving results with detailed metrics in a timestamped folder inside `runs/`.

## Installation

This package was developed using Python 3.10.

Clone this repository and install dependencies by using:

pip install -r requirements.txt

## Notes

- Set the `external_lambda` attribute in each node to specify external arrival rates.
- Customize routing logic directly per node through `routing_probabilities` dictionaries.
- Use a fixed random seed for reproducibility.
- Modify service rates, servers, and routing logic in node definitions to reflect new scenarios.
- Results are saved as CSV files inside uniquely named folders.

## License

BSD-3-Clause — see the `LICENSE` file for details.

## Contact / Support

For questions, bug reports, or feature requests please open an issue on GitHub or contact the maintainer at alexis.martinez.contacto@gmail.com.