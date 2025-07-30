import pandas as pd
import tldextract
import re

# Extract everything after http(s)://
def extract_after_http(url):
    if pd.isna(url):
        return None
    match = re.search(r'https?://(.+)', url)
    return match.group(1) if match else None

# Extract the core domain using tldextract
def get_core_domain(url):
    if pd.isna(url):
        return None
    ext = tldextract.extract(url)
    return ext.domain  # Just the core (e.g., 'zimblecode')

# Load Excel files
file_a = '<file_a url>'
file_b = '<file_b url>'

# Load the files
df_a = pd.read_excel(file_a)
df_b = pd.read_excel(file_b)

# Clean URLs
df_a['clean_link'] = df_a['Link'].apply(extract_after_http)
df_b['clean_source'] = df_b['Source url'].apply(extract_after_http)

# Extract core domains using tldextract
df_a['core_domain'] = df_a['clean_link'].apply(get_core_domain)
df_b['core_domain'] = df_b['clean_source'].apply(get_core_domain)

# Make a set of all core domains from A
core_domains_a = set(df_a['core_domain'].dropna().unique())

# Match against all domains
df_b['match_found'] = df_b['core_domain'].apply(
    lambda x: 'Match' if x in core_domains_a else 'No Match'
)

# ✅ Remove rows where 'Source url' contains 'domain-list' or 'blogspot.com'
df_b = df_b[~df_b['Source url'].str.contains('domain-list|blogspot\.com', case=False, na=False)]


# Save result
df_b.to_excel('<result_url>', index=False)
print("✅ Matching complete. Results saved to 'matched_output.xlsx'.")
