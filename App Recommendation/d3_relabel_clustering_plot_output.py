##########
# output json files for d3 visualisation of clustering & distances

# Tang Jiahui
# A0119415J

##########
## run the following codes in shell after running ETL_category_clustering_relabel.py
## some variables are from that file


dist_matrix = lambda cat1, cat2: distances[cat1][cat2] if cat1 <= cat2 else distances[cat2][cat1]

links = [{"source": str(cat1), "target": str(cat2), "value": dist_matrix(cat1, cat2)} for cat2 in range(len(keys)) for cat1 in range(len(keys)) if cat1 != cat2 and dist_matrix(cat1, cat2) > 0]

nodes = []

for cluster_id in np.unique(affprop.labels_):
    # exemplar = keys[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(np.nonzero(affprop.labels_==cluster_id))
    for i in cluster:
        nodes.append({"id": str(i), "group": str(cluster_id)})
    # cluster_str = ", ".join([category_labels[i] for i in cluster]) + "\n"

with open('miserables.json', 'w') as f:
    json.dump({'nodes': nodes, 'links': links}, f)