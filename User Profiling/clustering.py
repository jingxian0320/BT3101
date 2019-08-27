############################################################################
#                                                                          #
#                               Clustering                                 #
#                                                                          #
############################################################################

######################################################
#                     k-prototype                    #
######################################################

import numpy as np
from kmodes import kprototypes
import csv
from sklearn import metrics
import scipy
import matplotlib.pyplot as plt

device = np.genfromtxt('../ETL output/device_cat_rate.csv', skip_header=1, dtype=str, delimiter=',')[:,0]
data = np.genfromtxt('../ETL output/device_cat_rate.csv', skip_header=1, dtype=object, delimiter=',')[:,1:]

result = {}
for i in range(1,20):
    kproto = kprototypes.KPrototypes(n_clusters=i, init='Cao', verbose=1)
    clusters = kproto.fit_predict(data, categorical=[1])
    result[i]=kproto.cost_

result = {1:15580872772.4,
          2:9217716551.15,
          3:7421943930.64,
          4:4475015523.67,
          5:3799081575.35,
          6:2708956750.61,
          7:2760721463.46,
          8:2086271054.92,
          9:1871896453.23,
          10:1517243835.98,
          11:1323094477.24,
          12:1421728184.4,
          13:1146600159.44,
          14:1246635996.99,
          15:1069447879.77,
          16:972306941.189,
          17:942744004.492,
          18:833685461.617,
          19:850678175.454}

X = list(result.keys())
Y = list(result.values())

plt.figure()
plt.plot(X,Y)
plt.xticks(X)
plt.show()

######################################################
#                   sklearn KMeans                   #
######################################################

from scipy.spatial.distance import cdist, pdist
from sklearn.cluster import KMeans
import csv
from sklearn import metrics
import scipy
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import tree
import pydotplus
import math
from sklearn import preprocessing
from scipy.stats import ttest_ind

def kmeans_elbow(dataset):
    # build KMeans models
    K = range(1,15)
    KM = [KMeans(n_clusters=k).fit(dataset) for k in K]
    centroids = [k.cluster_centers_ for k in KM]

    # calculate distance
    D_k = [cdist(dataset, cent, 'euclidean') for cent in centroids]
    dist = [np.min(D,axis=1) for D in D_k]
    avgWithinSS = [sum(d)/dataset.shape[0] for d in dist]

    wcss = [sum(d**2) for d in dist]                # Total within-cluster sum of squares
    tss = sum(pdist(dataset)**2)/dataset.shape[0]   # The total sum of squares
    bss = tss-wcss                                  # The between-cluster sum of squares

    # elbow curve
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(K, avgWithinSS, 'b*-')
    plt.grid(True)
    plt.xlabel('Number of clusters')
    plt.ylabel('Average within-cluster sum of squares')
    plt.title('Elbow for KMeans clustering')
    plt.show()

data = pd.read_csv('../ETL output/device_cat_rate.csv')
col = data.columns.values[1:]
X = data[col]
X['gender'] = X['gender'].map({'F': 1, 'M': 0})

##########################################
#            original dataset            #
##########################################
X_unscaled = X.as_matrix()

kmeans_elbow(X_unscaled)


##########################################
#             scaled dataset             #
##########################################
import numpy as np

col = X.columns.values
X_ratio = []
for i in range(len(X)):
    X_ratio.append([0 for i in range(len(col))])

for i in range(0,len(col)):
    i_col = X.columns.values[i]
    i_max=X[i_col].max()
    i_min=X[i_col].min()
    for j in range(0,len(X)):
        X_ratio[j][i]=float(X[i_col][j]-i_min)/float(i_max-i_min)*100

X_ratio = np.array(X_ratio)

kmeans_elbow(X_ratio)


##########################################
#           noramlized dataset           #
##########################################
X_normalize = preprocessing.normalize(X)

kmeans_elbow(X_normalize)  # k = 4

k4 = KMeans(n_clusters=4).fit(X_normalize)
label_4 = k4.labels_
Y = label_4.astype(str)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X, Y)
dot_data = tree.export_graphviz(clf, out_file=None, 
                         feature_names=X.columns.values,
                               class_names=clf.classes_)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("k4_normalize.pdf")

############## analysis #############

# scatter plot
X_np = X.as_matrix()
fig = plt.figure()
ax = fig.add_subplot(111)
clr = ['b','g','r','c','m','y','k']
centroids = k4.cluster_centers_
D_k = cdist(X_np, centroids, 'euclidean')
cIdx = np.argmin(D_k,axis=1)

for i in range(4):
    ind = (cIdx==i)
    ax.scatter(X_np[ind,15],X_np[ind,0], s=30, c=clr[i], label='Cluster %d'%i)
plt.xlabel('Utility')
plt.ylabel('Price')
plt.title('Utility-Price, KMeans clustering with K=4')
plt.legend()
plt.show()

for i in range(4):
    ind = (cIdx==i)
    ax.scatter(X_np[ind,6],X_np[ind,0], s=30, c=clr[i], label='Cluster %d'%i)
plt.xlabel('Finance')
plt.ylabel('Price')
plt.title('Utility-Price, KMeans clustering with K=4')
plt.legend()
plt.show()

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
for i in range(4):
    ind = (cIdx==i)
    ax.scatter(X_np[ind,6],X_np[ind,0], X_np[ind,15], s=30, c=clr[i], label='Cluster %d'%i)
ax.set_xlabel('Finance')
ax.set_ylabel('Price')
ax.set_zlabel('Utility')
plt.title('Finance-Price-Utility, KMeans clustering with K=4')
plt.legend()
plt.show()

# boxplot
label_4 = pd.DataFrame(label_4, columns=['cluster'])

X_cluster = label_4.join(X, how='outer')
c_0 = X_cluster.loc[X_cluster['cluster'] == 0]   # len(c_0) = 19252
c_1 = X_cluster.loc[X_cluster['cluster'] == 1]   # len(c_1) = 2482
c_2 = X_cluster.loc[X_cluster['cluster'] == 2]   # len(c_2) = 307
c_3 = X_cluster.loc[X_cluster['cluster'] == 3]   # len(c_3) = 645

c0_fin = c_0['Finance'].as_matrix()
c1_fin = c_1['Finance'].as_matrix()
c2_fin = c_2['Finance'].as_matrix()
c3_fin = c_3['Finance'].as_matrix()

c0_baby = c_0['Babycare'].as_matrix()
c1_baby = c_1['Babycare'].as_matrix()
c2_baby = c_2['Babycare'].as_matrix()
c3_baby = c_3['Babycare'].as_matrix()

c0_game = c_0['Game'].as_matrix()
c1_game = c_1['Game'].as_matrix()
c2_game = c_2['Game'].as_matrix()
c3_game = c_3['Game'].as_matrix()

fin = [c0_fin,c1_fin,c2_fin,c3_fin]
plt.boxplot(fin)
plt.show()

baby = [c0_baby,c1_baby,c2_baby,c3_baby]
plt.boxplot(baby)
plt.show()

game = [c0_game,c1_game,c2_game,c3_game]
plt.boxplot(game)
plt.show()

# t-test analysis
t1_fin, p1_fin = ttest_ind(c0_fin, c1_fin, equal_var=False)
t2_fin, p2_fin = ttest_ind(c0_fin, c2_fin, equal_var=False)
t3_fin, p3_fin = ttest_ind(c0_fin, c3_fin, equal_var=False)
t4_fin, p4_fin = ttest_ind(c1_fin, c2_fin, equal_var=False)
t5_fin, p5_fin = ttest_ind(c1_fin, c3_fin, equal_var=False)
t6_fin, p6_fin = ttest_ind(c2_fin, c3_fin, equal_var=False)

t1_baby, p1_baby = ttest_ind(c0_baby, c1_baby, equal_var=False)
t2_baby, p2_baby = ttest_ind(c0_baby, c2_baby, equal_var=False)
t3_baby, p3_baby = ttest_ind(c0_baby, c3_baby, equal_var=False)
t4_baby, p4_baby = ttest_ind(c1_baby, c2_baby, equal_var=False)
t5_baby, p5_baby = ttest_ind(c1_baby, c3_baby, equal_var=False)
t6_baby, p6_baby = ttest_ind(c2_baby, c3_baby, equal_var=False)

t1_game, p1_game = ttest_ind(c0_game, c1_game, equal_var=False)
t2_game, p2_game = ttest_ind(c0_game, c2_game, equal_var=False)
t3_game, p3_game = ttest_ind(c0_game, c3_game, equal_var=False)
t4_game, p4_game = ttest_ind(c1_game, c2_game, equal_var=False)
t5_game, p5_game = ttest_ind(c1_game, c3_game, equal_var=False)
t6_game, p6_game = ttest_ind(c2_game, c3_game, equal_var=False)


