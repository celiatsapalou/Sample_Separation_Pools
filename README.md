# Fixed `process_bam.py` Script

## Overview

This repository includes the updated `process_bam.py` script, which has been enhanced to utilize regular expression matching for analysis between:

1. The **`predictions_lite.xlsx` cell ID column**
2. The **matching BAM file's cell ID (3 characters before .sort.bam) **

## Key Updates

- The script now matches cell IDs in a more robust and flexible manner using **regular expressions**, improving the accuracy of the analysis.
- Enhanced functionality ensures compatibility between the predictions file and BAM files by automating the matching process.


## Usage

1. **Prepare Input Files**:
   - Place your `predictions_lite.xlsx` file in the specified input directory (DEMULTIPLEXING).
   - Ensure your BAM files are in the designated BAM file directory ("/g/korbel2/weber/MosaiCatcher_files/DEMULTIPLEXING_POOLS/DEMULTIPLEXING_POOLS/MOSAICATCHER_GATHERING/").

2. **Run the Script**:

   ```bash
   python process_bam.py --predictions predictions_lite.xlsx --bam_dir /path/to/bam/files
   ```

3. **Output**:
   - The script will generate a folder called "renamed_bams" with the cells seperated for each sample