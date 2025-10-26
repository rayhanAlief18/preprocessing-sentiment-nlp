import gdown
import json

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
    return ''.join(normalized_words)

# Example usage:
drive_url = 'https://drive.google.com/file/d/13D5cVPKioABoR3wocU8fCJztSjzRySwd/view?usp=sharing'
slang_dict = load_slang_dict(drive_url)

# Print the loaded slang dictionary
print(slang_dict)
