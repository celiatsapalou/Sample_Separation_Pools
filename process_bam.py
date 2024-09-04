import pandas as pd
import os
import shutil
import sys

def process_bam_files(bam_folder, predictions_file, new_base_folder):
    # Load the Excel file
    df = pd.read_excel(predictions_file)
    
    # Create a dictionary for quick lookup based on the cell code
    sample_dict = {str(row['cell']).strip(): row['1KG_identified_sample'] for _, row in df.iterrows()}
    
    # Ensure the new base folder exists
    os.makedirs(new_base_folder, exist_ok=True)
    
    # Process each BAM file in the folder
    for filename in os.listdir(bam_folder):
        if filename.endswith('.bam') or filename.endswith('.bam.bai'):
            # Extract the sample prefix after 'TRU' (e.g., '1A40', '3C05')
            parts = filename.split('TRU')
            if len(parts) > 1:
                sample_prefix = parts[1][:4]  # Extract the first four characters after 'TRU'

                # Check if the extracted sample_prefix exists in the predictions file
                if sample_prefix in sample_dict:
                    new_prefix = sample_dict[sample_prefix]
                    new_filename = new_prefix + "." + filename

                    # Create a new directory for the sample if it doesn't exist
                    sample_dir = os.path.join(new_base_folder, new_prefix)
                    os.makedirs(sample_dir, exist_ok=True)

                    # Copy and rename the file
                    old_path = os.path.join(bam_folder, filename)
                    new_path = os.path.join(sample_dir, new_filename)

                    shutil.copy2(old_path, new_path)
                else:
                    print(f"Sample prefix {sample_prefix} not found in sample_dict")
            else:
                print(f"Could not find 'TRU' in filename: {filename}")

    # Create a done.txt file to signal completion
    with open(os.path.join(new_base_folder, "done.txt"), "w") as f:
        f.write("Done")

if __name__ == "__main__":
    bam_folder = sys.argv[1]
    predictions_file = sys.argv[2]
    new_base_folder = sys.argv[3]
    process_bam_files(bam_folder, predictions_file, new_base_folder)
