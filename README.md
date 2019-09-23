# HBinspector
Script to produce the hidden break plot from a 28S sequence and a paired RNA-seq dataset
<br> 
<br>  
## Arguments
Argument    |  Description             
:-------------:|:-----------------------
-seq filename | file w/ gene counts (from OrthoFinder output)
-reads filename | directory to write the output file(s)
-c filename | file w/ species. Analyze these species only
-left filename | file w/ species. Remove these species from analysis
-right | creates tsv file
<br>   
 
## Example usage

```
python orthocounts2bin.py -i /Users/pnatsi/orthology/Orthogroups.GeneCounts.tsv -o /Users/pnatsi/orthology/ -tsv -fasta
```
 
**Careful! Only full path to config file is currently supported**
 
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
