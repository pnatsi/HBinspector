import os
import matplotlib.pyplot as plt
import numpy as np
import argparse


#HERE BEGINS THE INPUT ARGUMENTS DEFINITION
usage = "A program to perform the hidden break analysis using a 28S sequence and paired RNA-Seq reads.  \nPlease provide full paths for every input file!"
toolname = "HBinspector"
footer = "Who \n Paschalis Natsidis (p.natsidis@ucl.ac.uk); \n \nWhere \n Telford Lab, UCL;\n\
 ITN IGNITE; \n  \nWhen\n September 2019; \n\n"

parser = argparse.ArgumentParser(description = usage, prog = toolname, epilog = footer, formatter_class=argparse.RawDescriptionHelpFormatter,)
parser.add_argument('-seq', metavar = 'filename', dest = 'sequence', required = True,
                    help = 'FASTA file with 28S sequence')
parser.add_argument('-reads', metavar = 'filename', dest = 'reads', nargs = 2, required = True,
                    help = 'Two fastq files with forward/reverse RNA reads')
parser.add_argument('-c', metavar = 'filename', dest = 'config', required = True,
                    help = 'full path to config file')

parser.add_argument('-left', metavar = 'int', dest = 'left', required = True,
                    help = 'position of the conserved region located before the hidden break')
parser.add_argument('-right', metavar = 'int', dest = 'right', required = True,
                    help = 'position of the conserved region located after the hidden break')

#parser.print_help()

args = parser.parse_args()

#READ USER INPUT
sequence_file = args.sequence
reads_file = args.reads
config_file = args.config

left_pos = args.left
right_pos = args.right

################################################################################################################
#READ CONFIG FILE

config = open(config_file, 'r')
config_lines = config.readlines()

proper_lines = []
for line in config_lines:
    if "=" in line:
        proper_lines.append(line.strip())

for line in proper_lines:
    if "kallisto" in line:
        kallisto_path = line.split("=")[1]
    if "samtools" in line:
        samtools_path = line.split("=")[1]
    if "bedtools" in line:
        bedtools_path = line.split("=")[1]
    if "output" in line:
        output_dir = line.split("=")[1]
    if "species" in line:
        species_name = line.split("=")[1]
    
working_dir = output_dir
bin_dir = os.environ['HOME'] + "/bin/"

################################################################################################################
#PREPARE FILENAMES
basename = species_name.split(" ")[0] + "_" + species_name.split(" ")[1]
file_prefix = output_dir + "/" + basename

bed_file = file_prefix + ".bed"
index_file = file_prefix + ".index"
bam_file = file_prefix + ".bam"
kallisto_results_dir = output_dir + "/kallisto_results_" + basename
tsv_file = output_dir + "/" + basename + "_coverage.tsv"

################################################################################################################
#RUN KALLISTO
os.system(kallisto_path + " index -i " + index_file + " " + sequence_file)
os.system("mkdir " + kallisto_results_dir)
os.system(kallisto_path + " quant -i " + index_file + " -o " + kallisto_results_dir + " --pseudobam -t 8 " + reads_file[0] + " " + reads_file[1])
os.system("mv " + kallisto_results_dir + "/pseudoalignments.bam " + bam_file)

#CREATE BED FILE
os.system(samtools_path + " view -H " + bam_file + " > bamheader_" + basename + ".txt")
header_file = open(output_dir + "/bamheader_" + basename + ".txt", "r")
header_file_lines = header_file.readlines()
third_line = header_file_lines[2].strip()
SN = third_line.split("\t")[1]
seq_header = SN.split(":")[1]
LN = third_line.split("\t")[2]
seq_length = LN.split(":")[1]

write_bedfile = open(bed_file, "w")
write_bedfile.write(seq_header + "\t" + "1" + "\t" + seq_length + "\t" + "rRNA_unit" + "\t" + "0" + "\t" + "+")
write_bedfile.close()

#RUN BEDTOOLS
print("\n\nCalculating coverage ...\n")
os.system(bedtools_path + " coverage -a " + bed_file + " -b " + bam_file + " -bed -d -s > " + tsv_file)
print("Calculating coverage ... Done!\n\n")

################################################################################################################
#DRAW THE PLOT
print("\nDrawing the plot ...\n")
coverage = []
tsv = open(tsv_file, "r")   

for line in tsv.readlines():
    coverage.append(int(line.split('\t')[-1].strip()))

fig, ax = plt.subplots()
fig.set_size_inches(15.5, 10)

ax.set_xlabel("Position")
ax.set_ylabel("Reads mapped")
ax.set_title(species_name.split(" ")[0] + " " + species_name.split(" ")[1], fontsize = 10)  
ax.tick_params(axis="both", which="both", bottom=False, top=False, labelbottom=True, left=False, right=False, labelleft=True)

ax.spines["top"].set_visible(False)  
ax.spines["right"].set_visible(False) 
ax.spines["bottom"].set_visible(False) 
ax.spines["left"].set_visible(False)

fill_color = "#4d4f53"
ax.fill(np.arange(len(coverage)+2), [0] + coverage + [0], fill_color, alpha = 0.5, label = "Read coverage")

ax.axvline(x = int(left_pos), ymin = 0.05, ymax = 0.95, linestyle = ":", c = "black", label = "Conserved elements")
ax.axvline(x = int(right_pos), ymin = 0.05, ymax = 0.95, linestyle = ":", c = "black", label = "Conserved elements")

fig.savefig(output_dir + "/" + basename + "_coverage.png")

print("Drawing the plot ... Done!\n")
print("Hidden Break plot saved at " + output_dir + "/" + basename + "_coverage.png\n")
