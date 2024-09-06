# Load the config.yaml file
configfile: "config.yaml"

# Variables loaded from the config file
samples = config["samples"]
bam_base_dir = config["bam_base_dir"]
predictions_dir = config["predictions_dir"]
symlink_dir = config["symlink_dir"]
renamed_bams_dir = config.get("renamed_bams_dir", "renamed_bams")  # Default directory if not specified in config

# Rule all to trigger symlinking and processing for all samples
rule all:
    input:
        expand(os.path.join(renamed_bams_dir, "{sample}_renamed_bams/done.txt"), sample=samples.keys())

# Rule to create symlinks for individual BAM and BAI files using process_bam.py
rule create_symlinks:
    input:
        bam_dir=lambda wildcards: os.path.join(bam_base_dir, wildcards.sample, samples[wildcards.sample], "bam"),
        predictions=lambda wildcards: os.path.join(predictions_dir, f"{wildcards.sample}--{samples[wildcards.sample]}", f"{samples[wildcards.sample]}_predictions_lite.xlsx")
    output:
        done=os.path.join(renamed_bams_dir, "{sample}_renamed_bams/done.txt")
    params:
        renamed_bams=os.path.join(renamed_bams_dir, "{sample}_renamed_bams")
    shell:
        """
        mkdir -p {params.renamed_bams}
        
        # Run the process_bam.py script to process and rename each BAM file
        python process_bam.py {input.bam_dir} {input.predictions} {params.renamed_bams}
        
        # Create a done.txt file to mark the completion
        touch {output.done}
        """
