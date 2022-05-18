import numpy as np
import os
import json
import matplotlib.pyplot as plt
import torch
from torch_geometric.nn import Node2Vec

edgelist = [[], []]
with open(os.path.join("data", "wikilinks.edg"), "r") as f:
    lines = f.readlines()

    for line in lines:
        edge = line.split()

        edgelist[0].append(int(edge[0]))
        edgelist[1].append(int(edge[1]))

edge_index = torch.tensor(edgelist, dtype=torch.long)

device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = Node2Vec(edge_index, embedding_dim=128, walk_length=80,
                    context_size=10, walks_per_node=10, num_negative_samples=1, p=1, q=1).to(device)

loader = model.loader(batch_size=128, shuffle=True, num_workers=4)
optimizer = torch.optim.Adam(list(model.parameters()), lr=0.01)

losses = []
for epoch in range(10):
    model.train()
    total_loss = 0
    for pos_rw, neg_rw in loader:
        optimizer.zero_grad()
        loss = model.loss(pos_rw.to(device), neg_rw.to(device))
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    loss = total_loss / len(loader)
    losses.append(loss)
    print(f'Epoch: {epoch:02d}, Loss: {loss:.4f}')

with open("losses.txt", "w") as f:
    json.dump(losses, f)

z = model().detach().cpu().numpy()

np.savetxt("wikilinks.emb", z, delimiter=",")