# Project Documentation

## Project Overview
This project focuses on the analysis of actor collaboration networks, exploring the dynamics of collaborations in various film and media projects.

## Installation
To install this project, follow these steps:
1. Clone the repository: `git clone https://github.com/Shibakennn/actor-collaboration-network-analysis.git`
2. Navigate into the project directory: `cd actor-collaboration-network-analysis`
3. Install the required dependencies: `pip install -r requirements.txt`

## Usage
You can run the main analysis script using the following command:
```bash
python main.py
```
Adjust the input files as necessary based on your data.

## Output Description
The output of this project includes various visualizations of the collaboration networks, as well as metrics regarding actor centrality, connections, and assortativity.

## Key Functions
- `load_data(file_path)`: Loads data from the specified file.
- `create_network(data)`: Creates a network graph from the data.
- `calculate_assortativity(network)`: Computes the assortativity of the network.
- `visualize_network(network)`: Generates visual representations of the collaboration network.

## Interpretation of Assortativity
Assortativity measures the tendency of a network to connect similar or dissimilar nodes. A positive assortativity indicates that high-degree nodes tend to connect with other high-degree nodes, while a negative assortativity suggests that high-degree nodes connect with lower-degree nodes. This aspect is crucial in understanding the collaboration patterns within the network.

## Code Structure
- `/src`: Contains the main source code files.
- `/data`: Holds the dataset used for analysis.
- `/outputs`: Includes the generated plots and output data files.
- `/requirements.txt`: Lists the dependencies required to run the project.

## References
- Newman, M. E. J. (2010). Networks: An Introduction. Oxford Press.
- Barabási, A.-L. (2016). Network Science. Cambridge University Press.