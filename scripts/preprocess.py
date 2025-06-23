import pandas as pd
import re
import os

# Load scraped data
input_file = "./data/raw_telegram_messages.csv"
output_file = "./data/cleaned_telegram_messages.csv"

# Load CSV
df = pd.read_csv(input_file)

# Step 1: Remove duplicate messages
df.drop_duplicates(subset="message", inplace=True)

# Step 2: Normalize Amharic text (strip unwanted whitespace, punctuation)
def normalize_amharic(text):
    # Remove extra spaces, tabs, newlines
    text = re.sub(r'\s+', ' ', str(text)).strip()
    return text

# Step 3: Remove emojis & non-Amharic symbols
def remove_emojis(text):
    emoji_pattern = re.compile(
        "["u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"     # symbols & pictographs
        u"\U0001F680-\U0001F6FF"     # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"     # flags
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', str(text))

# Apply both functions
df["message"] = df["message"].apply(normalize_amharic)
df["message"] = df["message"].apply(remove_emojis)

# Optional: Drop rows with empty or too-short messages
df = df[df["message"].str.len() > 5]

# Save cleaned data
os.makedirs("data", exist_ok=True)
df.to_csv(output_file, index=False)

print(f"Preprocessed data saved to: {output_file}")
