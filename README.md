# Py-SLR (a tool to aid in Systematic Literature Reviews)

PySLR is a simple, Python-written CLI tool (inspired by [slR](https://github.com/jcppc/slR), a similar tool but in R) to generate plots from XSLX tables with bibliography information.
These tables can be automatically generated from Bibtex files, needing only human input to classify and add additional information. 
The menu presents the following features:
- **Create dimension plots**: Create PDF figures with the plots of each dimension;
- **Create bibliometric plots**: Create bibliometry graphs about the articles (Demographics, publication sites...) (require author affiliation manual information);
- **Create radar plots**: Create radar plots for reviewed publications (require manual evaluation of publications with scores);
- **Create stacked dimension plots**: Create stacked bar frequency charts joining two dimensions;
- **Update Table from Bibtex**: Given a .bib files with new entries, update the review tables;
- **Get reference difference**: Given .bib files from the same databases but different fetch dates, return a file with the new references;
- **Create LaTeX information table**: Create a LaTeX table containing basic information about the reviewed publications;
- **Create LaTeX summary table**: Create a LaTeX table containing the taxonomic evaluation of the reviewed publications;

## How to use

The JSON configurations file (config.json) must be present in the root folder of the code.
It must be filled with the names of the paths, folders, and files containing the inputs and outputs of the tool.  
