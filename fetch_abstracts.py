from Bio import Entrez
import pandas as pd

Entrez.email = "example@email.com"  # required by NCBI (Put your email here)
INPUT_CSV = "data/publications.csv"
OUTPUT_CSV = "data/publications_with_abstracts.csv"

df = pd.read_csv(INPUT_CSV)
abstracts = []

for i, link in enumerate(df['Link']):
    print(f"Fetching {i+1}/{len(df)}: {link}")
    try:
        pmc_id = link.split("/")[-2]  # get PMC ID from URL
        handle = Entrez.efetch(db="pmc", id=pmc_id, rettype="abstract", retmode="text")
        abstract_text = handle.read().strip()
        handle.close()
    except Exception as e:
        print(f"Error fetching {link}: {e}")
        abstract_text = ""
    abstracts.append(abstract_text)

df['Abstract'] = abstracts
df.to_csv(OUTPUT_CSV, index=False)
print(f"Saved abstracts to {OUTPUT_CSV}")