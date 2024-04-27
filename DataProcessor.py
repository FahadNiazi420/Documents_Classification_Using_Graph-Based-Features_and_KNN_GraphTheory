import os
import pandas as pd
import re
import nltk

# # Set NLTK data path
# nltk.data.path.append("C:\\Users\\fkk42\\AppData\\Roaming\\nltk_data")

# # Download necessary NLTK data
# nltk.download('punkt', download_dir="C:\\Users\\fkk42\\AppData\\Roaming\\nltk_data")
# nltk.download('wordnet', download_dir="C:\\Users\\fkk42\\AppData\\Roaming\\nltk_data")

# Import required NLTK modules
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer


# Function to create the Processed Data folder if it doesn't exist
def create_processed_folder():
    folder_name = "Processed Data"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)


# Function to clean and preprocess text
def clean_text(text):
    # Lowercase the text
    text = text.lower()

    # Remove special characters and digits
    text = re.sub(r'[^a-zA-Z\s]', '', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [word for word in tokens if word not in stop_words]

    # Initialize WordNetLemmatizer
    lemmatizer = WordNetLemmatizer()

    # Lemmatize tokens
    lemmatized_tokens = [lemmatizer.lemmatize(word) for word in filtered_tokens]

    # Join tokens back into text
    cleaned_text = ' '.join(lemmatized_tokens)

    return cleaned_text


# Function to clean and preprocess text column in a DataFrame
def clean_and_preprocess_column(df, column_name):
    df[column_name] = df[column_name].apply(clean_text)
    return df


# Function to clean and preprocess each dataset
def clean_and_preprocess_datasets():
    create_processed_folder()

    # Read each dataset from Unprocessed Data folder
    unprocessed_folder = "Unprocessed Data"
    for filename in os.listdir(unprocessed_folder):
        if filename.endswith(".csv"):
            unprocessed_filepath = os.path.join(unprocessed_folder, filename)
            processed_filepath = os.path.join("Processed Data", f"cleaned_{filename}")

            # Read dataset
            df = pd.read_csv(unprocessed_filepath)

            # Clean and preprocess "Text Scraped" column
            df = clean_and_preprocess_column(df, 'Text Scraped')

            # Update column names
            new_headers = ["Website name", "Cleaning date", "Cleaning time", "links",
                           "Number of words Cleaned", "Cleaned Text"]
            df.columns = new_headers

            # Calculate number of words cleaned
            df['Number of words Cleaned'] = df['Cleaned Text'].str.split().str.len()

            # Save cleaned dataset
            df.to_csv(processed_filepath, index=False)


# Call the function to clean and preprocess datasets
clean_and_preprocess_datasets()
