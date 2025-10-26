import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import string
from nltk.tokenize import word_tokenize
import re

import gdown
import json


# import data excel dari gdrive
url = 'https://drive.google.com/file/d/1fY3UZtTHq1axQHQoqANAX8mrf3ANQ4js/view?usp=sharing'
path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
df = pd.read_csv(path)

print(df['content'])


# Function to download and load slang dictionary from Google Drive
def load_slang_dict(drive_url):
    # Extract the file ID from the Google Drive URL
    file_id = drive_url.split('/')[-2]

    # Construct the download URL
    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'

    # Download the file using gdown (it will be saved locally as 'slang_dict.txt')
    gdown.download(download_url, 'slang_dict.txt', quiet=False)

    # File txt tidak bisa dibaca karena kode meminta file json, maka dari itu kita 
    # perlu merubah format txt ke json    
    slang_dict = {}
    with open('slang_dict.txt', "r", encoding="utf-8") as f:
        for line in f:
            if "," in line:
                key, value = line.strip().split(",", 1)
                slang_dict[key.strip()] = value.strip()

    with open('slang_dict.json', "w", encoding="utf-8") as f:
        json.dump(slang_dict, f, ensure_ascii=False, indent=4)

    # Now open the downloaded file and load it as a dictionary
    with open('slang_dict.json', 'r', encoding='utf-8') as file:
        slang_dict = json.load(file)

    return slang_dict

def normalize_slang(text, slang_dict):
    words = word_tokenize(text)
    normalized_words = [slang_dict.get(word,word) for word in words]
    return ' '.join(normalized_words)


# Example usage:
drive_url = 'https://drive.google.com/file/d/13D5cVPKioABoR3wocU8fCJztSjzRySwd/view?usp=sharing'
slang_dict = load_slang_dict(drive_url)

# Print the loaded slang dictionary
# print(slang_dict)
# normalize_slang = normalize_slang(df['content'][0], slang_dict)
# normalize_slang = normalize_slang('kpn kowe ktdrn', slang_dict)
# print(normalize_slang)




def preprocess_text(text, slang_dict, stemmer):
    if not isinstance(text, str):  # ✅ lewati jika bukan string
        return ""
    # Lowercasing
    text = text.lower()

    # Normalize slang and abbreviations
    text = normalize_slang(text, slang_dict)

    # Remove punctuation
    text = re.sub(r'[^\w\s]', '', text)

    # Tokenize the text
    tokens = word_tokenize(text)

    # Remove stopwords
    custom_stopwords = set(stopwords.words('indonesian'))  # Add more stopwords as needed
    tokens = [word for word in tokens if word not in custom_stopwords]

    # Stemming
    tokens = [stemmer.stem(word) for word in tokens]

    # Join the tokens back into a single string
    return ' '.join(tokens)

#create stemmer
factory = StemmerFactory()
stemmer = factory.create_stemmer()

#example
text = 'adlh bgmn nih? lbh bae kowe tdrn smua'

#preprocess text
# preprocessed_text = preprocess_text(text,slang_dict,stemmer)

# loop preprocessing
preprocessed_texts = []
for index, row in df.iterrows():
    preprocessed_text = preprocess_text(row['content'], slang_dict, stemmer)
    preprocessed_texts.append(preprocessed_text)

df['preprocessed_content'] = preprocessed_texts
print(df[['content','preprocessed_content']])
df.to_csv('preprocessed_data.csv')
# print('preprocessed text:', preprocessed_text)



