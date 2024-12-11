import pandas as pd
import os
import shutil
import sys
import re

def process_bam_files(bam_folders, predictions_files, output_dir):
    # Split the paths into lists
    bam_folders = bam_folders.split()
    predictions_files = predictions_files.split()

    # Merge the predictions from all given Excel files into a single dictionary
    sample_dict = {}
    for predictions_file in predictions_files:
        if not os.path.exists(predictions_file):
            print(f"ERROR: Predictions file not found: {predictions_file}")
            continue
        # Load each predictions file and update the dictionary using the last three characters of the `cell`
        df = pd.read_excel(predictions_file)
        sample_dict.update({str(row['cell'])[-3:]: row['1KG_identified_sample'] for _, row in df.iterrows()})

    if not sample_dict:
        print("ERROR: No valid predictions files were processed.")
        return

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Regular expression to extract the last three characters before ".sort"
    regex = re.compile(r"([A-Z]\d{2})(?=\.sort)")

    # Process each BAM file in the folders
    for bam_folder in bam_folders:
        if not os.path.exists(bam_folder):
            print(f"ERROR: BAM folder not found: {bam_folder}")
            continue
        
        for filename in os.listdir(bam_folder):
            if filename.endswith(".bam") or filename.endswith(".bam.bai"):
                # Search for the last three characters before ".sort" in the filename
                match = regex.search(filename)
                if match:
                    sample_suffix = match.group(1)  # Extract the matched group
                    print(f"Processing file: {filename}, extracted suffix: {sample_suffix}")
                    
                    # Check if the extracted suffix exists in the predictions dictionary
                    if sample_suffix in sample_dict:
                        new_prefix = sample_dict[sample_suffix]
                        new_filename = new_prefix + "." + filename

                        # Create a new directory for the sample if it doesn't exist
                        sample_dir = os.path.join(output_dir, new_prefix)
                        os.makedirs(sample_dir, exist_ok=True)

                        # Copy and rename the file
                        old_path = os.path.join(bam_folder, filename)
                        new_path = os.path.join(sample_dir, new_filename)
                        shutil.copy2(old_path, new_path)
                    else:
                        print(f"WARNING: Sample suffix {sample_suffix} not found in sample_dict")
                else:
                    print(f"WARNING: No matching cell identifier found in filename: {filename}")

    # Create a "done.txt" file to indicate completion
    done_file_path = os.path.join(output_dir, "done.txt")
    with open(done_file_path, "w") as done_file:
        done_file.write("Processing complete.\n")
    print(f"Processing complete. Marker file created at: {done_file_path}")

if __name__ == "__main__":
    # Accept BAM folders, predictions files, and output directory from command-line arguments
    bam_folders = sys.argv[1]  # Space-separated BAM folder paths
    predictions_files = sys.argv[2]  # Space-separated predictions file paths
    output_dir = sys.argv[3]

    process_bam_files(bam_folders, predictions_files, output_dir)
