from pomegranate.bayesian_network import BayesianNetwork
from pomegranate.distributions import *

# Rain: (none, light, heavy)
rain = Categorical([[0.7, 0.2, 0.1]])

# Maintenance given rain: P(maintenance | rain)
maintenance = ConditionalCategorical([
    # Format: [P(no_maintenance), P(yes_maintenance)] for each rain state
    [[0.4, 0.6]],  # given no rain
    [[0.2, 0.8]],  # given light rain
    [[0.1, 0.9]]   # given heavy rain
])

# Train given both rain and maintenance
train = ConditionalCategorical([
    # Format: For each rain state, for each maintenance state
    [
        [[0.8, 0.2]],  # no rain, no maintenance
        [[0.9, 0.1]]   # no rain, yes maintenance
    ],
    [
        [[0.6, 0.4]],  # light rain, no maintenance
        [[0.7, 0.3]]   # light rain, yes maintenance
    ],
    [
        [[0.4, 0.6]],  # heavy rain, no maintenance
        [[0.5, 0.5]]   # heavy rain, yes maintenance
    ]
])

# Appointment given train
appointment = ConditionalCategorical([
    [[0.9, 0.1]],  # given train on time
    [[0.6, 0.4]]   # given train delayed
])

model = BayesianNetwork()
model.add_distributions([rain, maintenance, train, appointment])

model.add_edge(rain, maintenance)
model.add_edge(rain, train)
model.add_edge(maintenance, train)
model.add_edge(train, appointment)

evidence = {"train": 1}  # Use index 1 for "delayed" state
predictions = model.predict_proba(evidence)
print(predictions)