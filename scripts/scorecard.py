import pandas as pd
import numpy as np
import re

# Load the CSV
df = pd.read_csv("./data/cleaned_telegram_messages.csv", parse_dates=["date"])

# Rename column for consistency
df.rename(columns={'channel': 'vendor_channel'}, inplace=True)

# -- Step 1: Extract numeric prices using regex --
# Assumes prices look like "5500 ብር" or "ዋጋ:-5500 ብር"
def extract_prices(message):
    pattern = r"(\d{2,7})\s?ብር"
    return [int(match) for match in re.findall(pattern, message)]

df["extracted_prices"] = df["message"].apply(extract_prices)

# -- Step 2: Group by Vendor and Compute Metrics --
vendor_stats = []

for vendor, group in df.groupby("vendor_channel"):
    # Ensure views are numeric
    group['views'] = pd.to_numeric(group['views'], errors='coerce')

    # Time range of activity
    days_active = (group['date'].max() - group['date'].min()).days + 1
    posts_per_week = len(group) / (days_active / 7) if days_active > 0 else 0

    # Views
    avg_views = group['views'].mean()
    top_post = group.loc[group['views'].idxmax()]
    top_message = top_post['message']
    top_views = top_post['views']

    # Prices
    all_prices = [p for prices in group['extracted_prices'] for p in prices]
    avg_price = np.mean(all_prices) if all_prices else 0

    # Lending Score (change weights as needed)
    lending_score = (avg_views * 0.6) + (posts_per_week * 0.4)

    vendor_stats.append({
        'Vendor': vendor,
        'Posts per Week': round(posts_per_week, 2),
        'Avg Views': round(avg_views, 2),
        'Top Post Views': top_views,
        'Top Post Summary': top_message[:80] + "...",
        'Avg Price (Birr)': round(avg_price, 2),
        'Lending Score': round(lending_score, 2)
    })

# -- Step 3: Output Scorecard --
scorecard = pd.DataFrame(vendor_stats)
scorecard = scorecard.sort_values(by="Lending Score", ascending=False)

# Print summary
print(scorecard)

# Save to CSV
scorecard.to_csv("./data/vendor_lending_scorecard.csv", index=False)
