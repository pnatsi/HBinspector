# HBinspector
Script to produce the hidden break plot from a 28S sequence and a paired RNA-seq dataset. This script depends on the following software to run:
- [kallisto](https://pachterlab.github.io/kallisto/download) 
- [samtools](http://www.htslib.org/download/) 
- [bedtools](https://bedtools.readthedocs.io/en/latest/content/installation.html) 
<br>

The local paths to these tools **must** be defined in the config file.

<br>
Furthermore, the following Python packages are also required: <br>
- matplotlib <br>
- numpy 
 <br> 

 All the above tools and packages can be easily installed via the ```conda``` environment.
 

## Arguments
Argument    |  Description             
:-------------:|:-----------------------
`-seq` | file w/ the 28S rRNA sequence
`-reads` | files w/ paired aboveRNA-seq reads (need to provide two filenames, see Example Usage)
`-c` | (full) path to config file
`-left` | Position of the conserved 20-mer lying before the hidden break region in the 28S sequence*
`-right` | Position of the conserved 20-mer lying after the hidden break region in the 28S sequence**

<br>   
<br>
* left conserved region: AGUGGAGAAGGGUUCCAUGU <br>
** right conserved region: CGAAAGGGAATCGGGTTTAA
 
## Example Usage

HBinspector needs a config file to run. This file will contain the paths to required tools (kallisto, samtools, bedtools) as well as the preferred path to write output, and the analysed species name (to be used in output files).
<br>
Please change the provided `config.txt` file accordingly before running your own analysis.

```
python HBinspector.py -seq membranipora28S.fasta -reads SRR2131259_1.fastq.gz SRR2131259_2.fastq.gz -c config.txt -left 1657 -right 1935
```

## Citations

If you use HBinspector please cite the following publications:

- Bray.N.L., Pimentel.H., Melsted.P., Pachter.L. (2016) “Near-optimal probabilistic RNA-seq quantification” Nat Biotechnol, 34, 525–527.
- Li.H., Handsaker.B., Wysoker.A., Fennell.T., Ruan.J., Homer.N., Marth.G., Abecasis.G., Durbin.R.; 1000 Genome Project Data Processing Subgroup. (2009) The Sequence Alignment / Map format and SAMtools. Bioinformatics. 25, 2078–2079.
- Quinlan.A.R., Hall.I.M. (2010) BEDTools: a flexible suite of utilities for comparing genomic features. Bioinformatics, 26, 841–842. 

 
<br>
Who<br> 
 Paschalis Natsidis, PhD candidate (p.natsidis@ucl.ac.uk); <br>
<br>
Where<br>
 Telford Lab, UCL;<br>
 ITN IGNITE; 
<br>
<br>
When<br> 
 September 2019; 
