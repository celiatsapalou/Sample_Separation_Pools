import pandas as pd

# Load the demultiplex table, specifying the delimiter explicitly
df = pd.read_csv(snakemake.input[0], delimiter='\t')

# Strip potential trailing new line or other whitespace characters
df.columns = df.columns.str.strip()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Print columns to debug and ensure they are read correctly
print("Columns found:", df.columns.tolist())

# Calculate the output paths
df['output_path'] = df.apply(lambda row: f"results/{row['1KG_identified_sample']}/{row['1KG_identified_sample']}.{row['cell']}.bam", axis=1)

# Save the output paths to the specified output file
df['output_path'].to_csv(snakemake.output[0], header=False, index=False)