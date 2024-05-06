from functions import *
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import seaborn as sns



# Combine and save data from scrapped articles to csv file "uncleaned_data.csv"
filename = 'uncleaned_data.csv'
filename_preprocess = 'preprocessed_data.csv'
combine_and_save_data(filename)

# Read the uncleaned data
uncleaned_data = pd.read_csv(filename)

# Pre-Processing data on train
preprocessed_data = preprocess_data(uncleaned_data)

# Save preprocessed train dataset to CSV
# save_preprocessed_data(preprocessed_data, filename_preprocess)

preprocessed_df = pd.DataFrame(preprocessed_data)

# Separating into train and test data
# Separating into train and test data
train_set = preprocessed_df.iloc[:40]  # Access the first 40 rows
test_set = preprocessed_df.iloc[40:]   # Access the remaining rows



# #--------------------------------------------------------------------------------------------------------
# #--------------------------------------------------------------------------------------------------------
# #                               2. Graph Construction:
# #--------------------------------------------------------------------------------------------------------
# #--------------------------------------------------------------------------------------------------------

# Generate the graph for the training set
train_graphs = []
for index, row in train_set.iterrows():
    # Build the directed graph
    graph = construct_graph(row['content_tokens'])
    train_graphs.append(graph)

# Generate the graph for the test set
test_graphs = []
for index, row in test_set.iterrows():
    # Build the directed graph
    graph = construct_graph(row['content_tokens'])
    test_graphs.append(graph)























# import os

# # Define the folder to save the graph files
# graph_folder = "Graphs"
# if not os.path.exists(graph_folder):
#     os.makedirs(graph_folder)

# # Function to save graph as image
# def save_graph_as_image(graph, filename):
#     # Draw the graph using matplotlib
#     pos = nx.spring_layout(graph)  # You may choose a different layout
#     nx.draw(graph, pos, with_labels=True, node_color='skyblue', node_size=500, edge_color='black', linewidths=1, font_size=10)
    
#     # Save the plot as an image
#     plt.savefig(filename)
    
#     # Clear the current plot to avoid overlap in subsequent iterations
#     plt.clf()

# # Generate and save graphs for the training set
# for i, graph in enumerate(train_graphs):
#     filename = os.path.join(graph_folder, f"train_graph_{i}.png")
#     save_graph_as_image(graph, filename)

# # Generate and save graphs for the test set
# for i, graph in enumerate(test_graphs):
#     filename = os.path.join(graph_folder, f"test_graph_{i}.png")
#     save_graph_as_image(graph, filename)

# print("Graphs saved successfully in the Graphs folder.")



# Extracting labels
train_labels = train_set['label'].tolist()
test_labels = test_set['label'].tolist()

# Classification
i = 0
k = 3
predicted_labels = []
true_labels = []
for test_instance in test_graphs:
    predicted_label = knn(train_graphs, test_instance, k, train_labels)
    true_label = test_labels[i]
    i += 1
    predicted_labels.append(predicted_label)
    true_labels.append(true_label)
    print(f'Predicted class: {predicted_label} ------- Actual Class: {true_label}')

# Evaluation
accuracy = accuracy_score(true_labels, predicted_labels)
accuracy_percentage = accuracy * 100
print("Accuracy: ", accuracy_percentage)

# Compute evaluation metrics
report = classification_report(test_labels, predicted_labels)

# Print classification report
print("Classification Report:")
print(report)

# Compute confusion matrix
cm = confusion_matrix(test_labels, predicted_labels)

# Plot confusion matrix
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, cmap='Blues', fmt='d', xticklabels=np.unique(train_labels), yticklabels=np.unique(train_labels))
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()
