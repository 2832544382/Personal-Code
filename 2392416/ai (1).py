import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture as GMM
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from sklearn.model_selection import KFold, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
from sklearn.decomposition import PCA
from sklearn.metrics import precision_score, recall_score, accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.naive_bayes import GaussianNB
from sklearn.dummy import DummyClassifier
import seaborn as sns

penguins = pd.read_csv(r'C:\Users\28325\OneDrive\Desktop\AI\penguins.csv')
penguins_clean = penguins.dropna(subset=['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])

X = penguins_clean[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
y = penguins_clean['species']
cmap = ListedColormap(['#FFAAAA', '#AAFFAA', '#AAAAFF'])
#Elbow
k_values = range(1, 11)
sse = []

for k in k_values:
    kmeans = KMeans(n_clusters=k, random_state=0)
    kmeans.fit(X)
    sse.append(kmeans.inertia_) 

plt.figure(figsize=(3, 2))
plt.plot(k_values, sse, marker='o')
plt.xlabel('Number of k')
plt.ylabel('SSE (Inertia)')
plt.title('Elbow Method for K-Means')

plt.tight_layout()
plt.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\elbows.png')
plt.show()




gmm = GMM(n_components=3, random_state=7)
gmm.fit(X)
labels = gmm.predict(X)
centers = gmm.means_
print(gmm.score(X))
features_pairs = [
    (('bill_length_mm', 'bill_depth_mm'), 'Bill', 'Bill Length (mm)', 'Bill Depth (mm)'),
    (('flipper_length_mm', 'body_mass_g'), 'Flipper', 'Flipper Length (mm)', 'Body Mass (g)')
]

fig, ax = plt.subplots()

ax.plot([], [], 'o', color=cmap(0), label='Adelie', markersize=10)
ax.plot([], [], 'o', color=cmap(1), label='Gentoo', markersize=10)
ax.plot([], [], 'o', color=cmap(2), label='Chinstrap', markersize=10)

legend = ax.legend(loc='center')

ax.axis('off')

bbox = legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted())

fig.set_size_inches(bbox.width, bbox.height)
plt.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\markers.png')

plt.show()

fig, axes = plt.subplots(1, 3, figsize=(9, 3))

for i, ((x_feature, y_feature), title, xlabel, ylabel) in enumerate(features_pairs):
    sc = axes[i].scatter(penguins_clean[x_feature], penguins_clean[y_feature], c=y.map({'Adelie': 0, 'Chinstrap': 1, 'Gentoo': 2}), cmap=cmap, label=y.unique(), s=2)
    axes[i].scatter(centers[:, X.columns.get_loc(x_feature)], centers[:, X.columns.get_loc(y_feature)], s=50, c='red', marker='*', label='Centers')
    axes[i].set_title(title)
    axes[i].set_xlabel(xlabel)
    axes[i].set_ylabel(ylabel)

axes[2].set_axis_off()
legend1 = axes[2].legend(*sc.legend_elements(), title="Species", loc='center')
axes[2].add_artist(legend1)

plt.tight_layout()
plt.show()

fig.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\gmms.png')

#box plot
y_labels = ['Bill Length (mm)', 'Bill Depth (mm)', 'Flipper Length (mm)', 'Body Mass (g)']
species_categories = penguins_clean['species'].unique()
fig, axes = plt.subplots(1, 4, figsize=(16, 4))

for i, feature in enumerate(X):
    data_to_plot = [penguins_clean[penguins_clean['species'] == species][feature] for species in species_categories]
    axes[i].boxplot(data_to_plot, labels=species_categories)
    axes[i].set_title(f'{y_labels[i]}')
    axes[i].set_xlabel('Species', fontsize=14)
    axes[i].set_ylabel(y_labels[i], fontsize=14)
    axes[i].tick_params(axis='both', labelsize=16)

plt.tight_layout()
plt.show()
fig.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\boxplot.png')

total_count = []

#Baseline Dummy
dummy = DummyClassifier(strategy="most_frequent")
X_dummy= penguins_clean[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
dummy.fit(X_dummy, y)
dummy.predict(X_dummy)
total_count.append(dummy.score(X_dummy,y))

X_dummy= penguins_clean[['bill_length_mm', 'bill_depth_mm']]
dummy.fit(X_dummy, y)
dummy.predict(X_dummy)
total_count.append(dummy.score(X_dummy,y))

X_dummy= penguins_clean[['flipper_length_mm', 'body_mass_g']]
dummy.fit(X_dummy, y)
dummy.predict(X_dummy)
total_count.append(dummy.score(X_dummy,y))

#print(dummy.score(X_dummy,y))

#PCA
pca = PCA(n_components=3)
X_pca = pca.fit_transform(X)


#Cross Validation

from sklearn.model_selection import train_test_split, KFold
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Assume penguins_clean is loaded as before
X_kfold = penguins_clean[['bill_length_mm', 'bill_depth_mm','flipper_length_mm', 'body_mass_g']].values
y_kfold = penguins_clean['species'].factorize()[0]

X_train, X_test, y_train, y_test = train_test_split(X_kfold, y_kfold, test_size=0.2, random_state=42)

kf = KFold(n_splits=5, shuffle=True, random_state=42)
max_k = 30

training_accuracies = []
validation_accuracies = []

for k in range(1, max_k + 1):
    knn = KNeighborsClassifier(n_neighbors=k)
    for train_index, test_index in kf.split(X_train):
        # Corrected indexing here using .iloc for pandas DataFrame or direct indexing for numpy arrays
        X_train_fold, X_test_fold = X_train[train_index], X_train[test_index]
        y_train_fold, y_test_fold = y_train[train_index], y_train[test_index]

        knn.fit(X_train_fold, y_train_fold)
        train_predictions = knn.predict(X_train_fold)
        test_predictions = knn.predict(X_test_fold)

        train_accuracy = accuracy_score(y_train_fold, train_predictions)
        validation_accuracy = accuracy_score(y_test_fold, test_predictions)

        training_accuracies.append(train_accuracy)
        validation_accuracies.append(validation_accuracy)

mean_train_accuracies = [np.mean(training_accuracies[i * 5:(i + 1) * 5]) for i in range(max_k)]
mean_valid_accuracies = [np.mean(validation_accuracies[i * 5:(i + 1) * 5]) for i in range(max_k)]

max_train_accuracy = max(mean_train_accuracies)
max_valid_accuracy = max(mean_valid_accuracies)
best_k_train = mean_train_accuracies.index(max_train_accuracy) + 1
best_k_valid = mean_valid_accuracies.index(max_valid_accuracy) + 1

print(f"Maximum Training Accuracy: {max_train_accuracy:.2f} at k={best_k_train}")
print(f"Maximum Validation Accuracy: {max_valid_accuracy:.2f} at k={best_k_valid}")

plt.figure(figsize=(4, 2))
plt.plot(range(1, max_k + 1), mean_train_accuracies, label='Mean Training Accuracy')
plt.plot(range(1, max_k + 1), mean_valid_accuracies, label='Mean Validation Accuracy')
plt.xlabel('Number of Neighbors: k')
plt.ylabel('Accuracy')
plt.title('KNN Training and Validation Accuracy')
plt.legend()
plt.show()

#KNN
'''
X_Knn = penguins_clean[['bill_length_mm', 'bill_depth_mm','flipper_length_mm', 'body_mass_g']]
y = penguins_clean['species'].factorize()[0]
X_train_Knn, X_test_Knn, y_train_Knn, y_test_Knn = train_test_split(X_Knn, y, test_size=0.2, random_state=42)
knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(X_train_Knn, y_train_Knn)
ypred_test = knn.predict(X_test_Knn)
total_count.append(accuracy_score(y_test_Knn, ypred_test))
cm1 = confusion_matrix(y_test_Knn, ypred_test)

X_Knn = penguins_clean[['bill_length_mm', 'bill_depth_mm']]
y = penguins_clean['species'].factorize()[0]
X_train_Knn, X_test_Knn, y_train_Knn, y_test_Knn = train_test_split(X_Knn, y, test_size=0.2, random_state=42)
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train_Knn, y_train_Knn)
ypred_test = knn.predict(X_test_Knn)
total_count.append(accuracy_score(y_test_Knn, ypred_test))
cm2 = confusion_matrix(y_test_Knn, ypred_test)
'''
X_Knn = penguins_clean[['flipper_length_mm', 'body_mass_g']]
y = penguins_clean['species'].factorize()[0]
X_train_Knn, X_test_Knn, y_train_Knn, y_test_Knn = train_test_split(X_Knn, y, test_size=0.2, random_state=42)
knn = KNeighborsClassifier(n_neighbors=6)
knn.fit(X_train_Knn, y_train_Knn)
ypred_test = knn.predict(X_test_Knn)
total_count.append(accuracy_score(y_test_Knn, ypred_test))
cm3 = confusion_matrix(y_test_Knn, ypred_test)

#print("Accuracy:", accuracy_score(y_test_Knn, ypred_test))

knn_cm = confusion_matrix(y_test_Knn, ypred_test)
print("Confusion Matrix:\n", knn_cm)

# Create mesh grid
h = 0.1

x_min, x_max = X_train_Knn['flipper_length_mm'].min() - 1, X_train_Knn['flipper_length_mm'].max() + 1
y_min, y_max = X_train_Knn['body_mass_g'].min() - 1, X_train_Knn['body_mass_g'].max() + 1

#x_min, x_max = X_train_Knn['bill_length_mm'].min() - 1, X_train_Knn['bill_length_mm'].max() + 1
#y_min, y_max = X_train_Knn['bill_depth_mm'].min() - 1, X_train_Knn['bill_depth_mm'].max() + 1
xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

# Convert mesh grid arrays to DataFrame for prediction
#mesh_df = pd.DataFrame(np.c_[xx.ravel(), yy.ravel()], columns=['bill_length_mm', 'bill_depth_mm'])
mesh_df = pd.DataFrame(np.c_[xx.ravel(), yy.ravel()], columns=['flipper_length_mm', 'body_mass_g'])
Z = knn.predict(mesh_df)  # Use DataFrame with column names for prediction
Z = Z.reshape(xx.shape)

# Visualize the decision boundaries
plt.figure(figsize=(4, 4))
plt.contourf(xx, yy, Z, alpha=0.8, cmap=cmap)  # Adjusted cmap to 'viridis' as it wasn't defined in your snippet
#plt.scatter(X_train_Knn['bill_length_mm'], X_train_Knn['bill_depth_mm'], c=y_train_Knn, edgecolors='k', cmap=cmap, s=10)  # Same cmap as contourf for consistency

plt.scatter(X_train_Knn['flipper_length_mm'], X_train_Knn['body_mass_g'], c=y_train_Knn, edgecolors='k', cmap=cmap, s=10)  # Same cmap as contourf for consistency
plt.xlabel('Flipper Length (mm)',fontdict={'fontsize':10})
plt.ylabel('Body Mass (g)',fontdict={'fontsize':10})
plt.title('Flipper Length vs Body Mass (k=6)')
#plt.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\First_two.png')
plt.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\Second_two.png')
plt.show()



#Naive Bayes
#X_Bayes = penguins_clean[['bill_length_mm', 'bill_depth_mm']]
#X_Bayes = penguins_clean[['flipper_length_mm', 'body_mass_g']]
X_Bayes= penguins_clean[['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']]
X_train_Bayes, X_test_Bayes, y_train_Bayes, y_test_Bayes = train_test_split(X_Bayes, y, test_size=0.2, random_state=42) #change X_Bayes to pca
nb = GaussianNB()
nb.fit(X_train_Bayes, y_train_Bayes)
predictions = nb.predict(X_test_Bayes)
total_count.append(accuracy_score(y_test_Bayes, predictions))
cm4 = confusion_matrix(y_test_Bayes, predictions)

X_Bayes= penguins_clean[['bill_length_mm', 'bill_depth_mm']]
X_train_Bayes, X_test_Bayes, y_train_Bayes, y_test_Bayes = train_test_split(X_Bayes, y, test_size=0.2, random_state=42) #change X_Bayes to pca
nb = GaussianNB()
nb.fit(X_train_Bayes, y_train_Bayes)
predictions = nb.predict(X_test_Bayes)
total_count.append(accuracy_score(y_test_Bayes, predictions))
cm5 = confusion_matrix(y_test_Bayes, predictions)

X_Bayes= penguins_clean[['flipper_length_mm', 'body_mass_g']]
X_train_Bayes, X_test_Bayes, y_train_Bayes, y_test_Bayes = train_test_split(X_Bayes, y, test_size=0.2, random_state=42) #change X_Bayes to pca
nb = GaussianNB()
nb.fit(X_train_Bayes, y_train_Bayes)
predictions = nb.predict(X_test_Bayes)
total_count.append(accuracy_score(y_test_Bayes, predictions))
cm6 = confusion_matrix(y_test_Bayes, predictions)

print(accuracy_score(y_test_Bayes, predictions))
nb_cm = confusion_matrix(y_test_Bayes, nb.predict(X_test_Bayes))
print(nb_cm)

#total
print(total_count)
groups = ['All Features', 'BL & BW', 'FL & BM']
algorithms = ['Dummy', 'KNN', 'Naive Bayes']

n_groups = 3
index = np.arange(n_groups)
bar_width = 0.25

fig, (ax1, ax2) = plt.subplots(1,2,figsize=(6, 2))
bars1 = ax1.bar(index, total_count[0:3], bar_width, label='Dummy')
bars2 = ax1.bar(index + bar_width, total_count[3:6], bar_width, label='KNN')
bars3 = ax1.bar(index + 2 * bar_width, total_count[6:9], bar_width, label='Naive Bayes')

ax1.set_xlabel('Datasets')
ax1.set_ylabel('Accuracy')
ax1.set_title('Accuracy of 3 algorithms')
ax1.set_xticks(index + bar_width)
ax1.set_xticklabels(groups)

ax2.legend(handles=[bars1, bars2, bars3], labels=algorithms, title="Algorithms")
ax2.axis('off')
plt.subplots_adjust(wspace=0.1)
plt.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\accus.png')
plt.tight_layout()
plt.show()

fig, axes = plt.subplots(nrows=1, ncols=3, figsize=(9, 6))

#cms = [cm1, cm2, cm3]
cms = [cm4, cm5, cm6]

#titles = ["KNN BL & BW", "KNN FL & BM", "KNN All Features"]
titles = ["NB BL & BW", "NB FL & BM", "NB All Features"]

class_labels = ['Adelie', 'Gentoo', 'Chinstrap']

ticks = [0, 1, 2] 
for ax, cm, title in zip(axes, cms, titles):
    cax = ax.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
    for (i, j), val in np.ndenumerate(cm):
        ax.text(j, i, f'{val}', ha='center', va='center', color='white' if val > np.max(cm)/2 else 'black')
    ax.set_title(title)
    ax.set_xlabel('Predicted')
    ax.set_ylabel('Actual')
    ax.set_xticks(ticks) 
    ax.set_yticks(ticks)  
    ax.set_xticklabels(class_labels) 
    ax.set_yticklabels(class_labels) 

plt.tight_layout()
#plt.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\knncm.png', bbox_inches='tight', pad_inches=0.1)
plt.savefig(r'C:\Users\28325\OneDrive\Desktop\AI\penguin_pic\nbcm.png', bbox_inches='tight', pad_inches=0.1)

plt.show()
