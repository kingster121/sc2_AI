There would 2 main ML algo running to determine our final output action.

\
Macro: Decides the long-term strategy
- Inputs: []
- Ouputs: [optimal_army_comp, expand, attack, defend]
- Reward: [mineral_mining_lead mineral_fighting_lead, army_size, enemy_army_size]

\
Micro:
- Inputs: [minimap, ]
- Outputs: []
- Reward: Look into 5 mins of gametime