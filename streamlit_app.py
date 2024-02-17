#Input the relevant libraries
import numpy as np
import pandas as pd
import streamlit as st
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.naive_bayes import GaussianNB
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

# Define the Streamlit app
def app():
    
    st.title('Understanding Gaussian and Bernoulli Naive Bayes')
    st.subheader('by Louie F. Cervantes M.Eng., WVSU College of ICT')
 
    st.write("""Both Gaussian and Bernoulli Naive Bayes are variants \
        of the Naive Bayes algorithm, a popular machine learning \
        technique for classification. However, they differ in \
        how they handle data and are suited for different types of datasets.""")

    st.write('Key Differences:')
    st.write('Data Type:')
    text = """ Gaussian Naive Bayes: Assumes features are continuous 
    and follow a normal distribution (bell-shaped curve). Examples: 
    height, weight, temperature."""
    st.write(text)

    text = """Bernoulli Naive Bayes: Assumes features are binary 
    (yes/no, true/false, present/absent). Examples: email spam 
    filter (spam/not spam), image pixel (black/white). Conditional 
    Probability Distribution:"""
    st.write(text)

    text = """Gaussian Naive Bayes: Uses a Gaussian distribution to 
    estimate the probability of a feature value given a class. 
    Bernoulli Naive Bayes: Uses a Bernoulli distribution to estimate 
    the probability of a feature being present or absent given a class."""
    st.write(text)

    st.text('Assumptions:')

    text = """Gaussian Naive Bayes: Assumes independence between features, 
    which may not be realistic in most real-world scenarios.
    Bernoulli Naive Bayes: Makes the same independence assumption, 
    but it might be less sensitive to it due to simpler data."""

    st.write(text)
    st.write('Best Datasets:')

    text = """Gaussian Naive Bayes: Works best for datasets with numerically 
    continuous features that are normally distributed. Examples: predicting 
    house prices based on size, number of bedrooms, etc. Can be sensitive to 
    outliers and non-normal distributions."""

    st.write(text)

    text = """Bernoulli Naive Bayes: Ideal for datasets with binary features or 
    features that can be easily converted to binary. Examples: text classification 
    (spam/not spam), document categorization, image recognition (presence of 
    specific objects). Not ideal for continuous data or large numbers of 
    discrete categories."""
    st.write(text)

    # Create the logistic regression 
    clf = GaussianNB() 
    options = ['Gaussian Naive Bayes', 'Bernoulli Naive Bayes']
    selected_option = st.selectbox('Select the classifier', options)
    if selected_option=='Bernoulli Naive Bayes':
        clf = BernoulliNB()
    else:
        clf = GaussianNB()
    
    # Create the logistic regression 
    dbfile = 'three-clusters.csv'
    options = ['Multiclass', 'Binary']
    selected_option = st.selectbox('Select the dataset', options)
    if selected_option=='Binary':
        dbfile = 'two-clusters.csv'
    else :
        dbfile = 'three-clusters.csv'

        
    if st.button('Start'):
        
        df = pd.read_csv(dbfile, header=0)
        st.subheader('The Dataset')
        # display the dataset
        st.dataframe(df, use_container_width=True)  

        #load the data and the labels
        X = df.values[:,0:-1]
        y = df.values[:,-1]          
        
        # Split the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(X, y, \
            test_size=0.2, random_state=42)
        
        clf.fit(X_train,y_train)
        y_test_pred = clf.predict(X_test)
        st.subheader('Confusion Matrix')
        st.write('Confusion Matrix')
        cm = confusion_matrix(y_test, y_test_pred)
        st.text(cm)
        st.subheader('Performance Metrics')
        st.text(classification_report(y_test, y_test_pred))
        st.subheader('VIsualization')
        visualize_classifier(clf, X_test, y_test_pred)

def labeltonumeric(df, column):
    from sklearn.preprocessing import LabelEncoder
    le = LabelEncoder()
    df[column] = le.fit_transform(df[column])
    return df

def visualize_classifier(classifier, X, y, title=''):
    # Define the minimum and maximum values for X and Y
    # that will be used in the mesh grid
    min_x, max_x = X[:, 0].min() - 1.0, X[:, 0].max() + 1.0
    min_y, max_y = X[:, 1].min() - 1.0, X[:, 1].max() + 1.0

    # Define the step size to use in plotting the mesh grid 
    mesh_step_size = 0.01

    # Define the mesh grid of X and Y values
    x_vals, y_vals = np.meshgrid(np.arange(min_x, max_x, mesh_step_size), np.arange(min_y, max_y, mesh_step_size))

    # Run the classifier on the mesh grid
    output = classifier.predict(np.c_[x_vals.ravel(), y_vals.ravel()])

    # Reshape the output array
    output = output.reshape(x_vals.shape)
    
    # Create the figure and axes objects
    fig, ax = plt.subplots()

    # Specify the title
    ax.set_title(title)
    
    # Choose a color scheme for the plot
    ax.pcolormesh(x_vals, y_vals, output, cmap=plt.cm.gray)
    
    # Overlay the training points on the plot
    ax.scatter(X[:, 0], X[:, 1], c=y, s=75, edgecolors='black', linewidth=1, cmap=plt.cm.Paired)
    
    # Specify the boundaries of the plot
    ax.set_xlim(x_vals.min(), x_vals.max())
    ax.set_ylim(y_vals.min(), y_vals.max())
    
    # Specify the ticks on the X and Y axes
    ax.set_xticks(np.arange(int(X[:, 0].min() - 1), int(X[:, 0].max() + 1), 1.0))
    ax.set_yticks(np.arange(int(X[:, 1].min() - 1), int(X[:, 1].max() + 1), 1.0))

    
    st.pyplot(fig)
    
#run the app
if __name__ == "__main__":
    app()
