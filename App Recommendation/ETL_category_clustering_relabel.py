### ETL for categories clustering and relabel ###
### Tang Jiahui ###
### A0119415J ###


import csv
cat = dict()

# building a dict matrix of one categories and its corresponding apps
with open("app_labels.csv","rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if row[1] in cat: 
            cat[row[1]].append(row[0])
        else:
            cat[row[1]] = [row[0],]


category_labels = {}
with open("label_categories.csv", "rb") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        category_labels[row[0]] = row[1]

# ========================
import numpy as np
import sklearn.cluster
import distance

# sorting values 
# get a stable list of keys and values
# as python dict.keys() & values() return unstable results
keys = []
values = []
for key in cat.keys():
    cat[key] = sorted(cat[key])
    keys.append(key)
    values.append(cat[key])

keys = np.asarray(keys)


# distance/similarity matrix by testing union/similarity
values2 = [set(i) for i in values]
testdistance = lambda x, y: 1.0 * len(values2[x].intersection(values2[y])) / (len(values2[x].union(values2[y])))

distances = []
for i in range(len(keys)):
    distances.append({})
    for j in range(i, len(keys)):
        distances[i][j] = testdistance(i, j)
    print i

# fill in the similarity matrix. Symmetric.
lev_similarity = np.array([[distances[cat1][cat2] if cat1 <= cat2 else distances[cat2][cat1] 
    for cat1 in range(len(keys))] for cat2 in range(len(keys))])


# ==== clustering ========
# affprop = sklearn.cluster.AffinityPropagation(affinity="precomputed", damping=0.5)
affprop = sklearn.cluster.KMeans(n_clusters=40, random_state=1)
# affprop = sklearn.cluster.AgglomerativeClustering(n_clusters=20)
affprop.fit(lev_similarity)


for cluster_id in np.unique(affprop.labels_):
    # exemplar = keys[affprop.cluster_centers_indices_[cluster_id]]
    cluster = np.unique(keys[np.nonzero(affprop.labels_==cluster_id)])
    cluster_str = ", ".join([category_labels[i] for i in cluster]) + "\n"
    # print(" - *%s:* %s" % (exemplar, cluster_str))
    print cluster_str

 
# ====== Manually label each cluster =============
#         Business         Education     Entertainment           Finance 
#            Games  Health & Fitness         Lifestyle             Music 
#       Navigation              News     Photo & Video      Productivity 
#        Reference          Shopping Social Networking            Sports 
 #          Travel         Utilities           Weather          category 
# ========= relabel manually each group with references of categories from external data ==========

manual_label = ["Entertainment", "Game", "Finance", "Finance", "Utility", "Lifestyle", "Travel", "Finance","Travel","Entertainment", "Babycare", "Travel", "Finance", "Finance", "Babycare", "Finance", "Travel", "Sports", "Finance", "Travel", "Utility", "Finance", "Education", "Lifestyle", "Game", "Game", "Education", "Lifestyle", "Lifestyle", "Productivity", "Shopping", "Lifestyle", "Entertainment", "Finance", "Productivity", "Insurance", "Travel", "Beauty", "Music", "Finance"]

#==== write csv of app categories =====

with open("relabel_categories.csv",'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['label_id','new_category','clustering_group'])
    for i in range(len(keys)):
        writer.writerow([keys[i], manual_label[affprop.labels_[i]], affprop.labels_[i]])



#==== label each app with a definite categories ====
app = dict()

# building a dict matrix of one app and its corresponding categories
with open("app_labels.csv","rb") as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if row[0] in app: 
            app[row[0]].append(row[1])
        else:
            app[row[0]] = [row[1],]

# take the most common occurred category after relabeling
def most_common(lst):
    return max(set(lst), key=lst.count)

relabel = dict()
for i in range(len(keys)):
    relabel[keys[i]] = manual_label[affprop.labels_[i]]

app_relabel = dict()
for key in app.keys():
    for category in app[key]:
        if key not in app_relabel:
            app_relabel[key] = [relabel[category],]
        else:
            app_relabel[key].append(relabel[category])
    app_relabel[key] = most_common(app_relabel[key])

#=========write csv of apps and its corresponding categories =======

with open("relabel_apps.csv",'wb') as csvfile:
    writer = csv.writer(csvfile, delimiter=',')
    writer.writerow(['app_id','new_category'])
    for i in app_relabel:
        writer.writerow([i, app_relabel[i]])
