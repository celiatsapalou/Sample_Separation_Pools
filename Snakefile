configfile: "config.yaml"

rule all:
    input:
        expand(os.path.join(config["symlink_dir"], "{sample}_symlinks"), sample=config["samples"])

rule create_symlinks:
    input:
        bam_dir=lambda wildcards: os.path.join(config["bam_base_dir"], wildcards.sample, config["subdir"], "bam"),
        predictions=lambda wildcards: os.path.join(config["predictions_dir"], f"{wildcards.sample}--{config['subdir']}", f"{config['subdir']}_predictions_lite.xlsx")
    output:
        symlink_dir=directory(os.path.join(config["symlink_dir"], "{sample}_symlinks"))  # Mark as directory
    shell:
        """
        # Create symlink directory if not exists
        mkdir -p {output.symlink_dir}
        
        # Create symlinks for BAM files
        for bam_file in $(ls {input.bam_dir}); do
            ln -s {input.bam_dir}/$bam_file {output.symlink_dir}/$bam_file
        done
        """

# Rule to process the BAM files using the predictions and renaming them
rule process_bam_files:
    input:
        symlink_dir="{sample}_symlinks",
        predictions=lambda wildcards: os.path.join(config["predictions_dir"], f"{wildcards.sample}--{config['subdir']}", f"{config['subdir']}_predictions_lite.xlsx")
    output:
        done_file=os.path.join(config["symlink_dir"], "{sample}_symlinks/done.txt")
    script:
        "process_bam.py"
