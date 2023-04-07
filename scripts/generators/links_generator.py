############################################################
# For Referee docs, 11.19
# This generates the file "links.html"
############################################################

import sys, os
sys.path.append(os.path.abspath('../lib/'))
import read_chunks as RC
######################
# HTML template
######################

html_template = """
<!doctype html>
    {head}

<body>
    {nav}

	<div class="row" id="main-content-row">
		<div class="col-3-24 margin-main"></div>
		<div class="col-18-24" id="main-content-col">
            <div class="row" id="title-row">
                <div class="col-2-24 margin"></div>
                <div class="col-8-24" id="logo-cont">
                    <img id="logo-main" src="img/logo2.png">
                </div>
                <div class="col-2-24 margin"></div>
            </div>

            

            <div class="row">
                <div class="col-1-24 margin-main"></div>
                <div class="col-22-24">

                    <h1>Links</h1>

                    <h3>PhyloAcc</h3>
                        <ul>
                            <p>
                                <a href="https://github.com/phyloacc" target="_blank">Github organization</a> / 
                                All code, data, and documentation relating to PhyloAcc is hosted here
                            </p>

                            <p>
                                <a href="https://bioconda.github.io/recipes/phyloacc/README.html" target="_blank">Bioconda page</a> / 
                                Information about the PhyloAcc bioconda package
                            </p>

                            <p>
                                <a href="https://doi.org/10.1093/molbev/msz049" target="_blank">Original paper (PhyloAcc-ST)</a> / 
                                The original manuscript in which PhyloAcc was developed, with a results relating to flightlessness in birds and marine mammals
                            </p>

                            <p>
                                <a href="https://doi.org/10.1101/2022.12.23.521765" target="_blank">Discordance paper (Phyloacc-GT; pre-print)</a> / 
                                The pre-print of hte manuscript in which the gene tree model was developed
                            </p>

                            <p>
                                <a href="https://news.harvard.edu/gazette/story/2019/05/harvard-study-explores-genetics-behind-evolution-of-flightless-birds/" target="_blank">The evolution of flightless birds</a> / 
                                An article in The Harvard Gazette covering research related to PhyloAcc
                            </p>                            
                        </ul>

                    <h3>Other helpful software</h3>
                        <ul>
                            <p>
                                <a href="http://compgen.cshl.edu/phast/" target="_blank">PHAST</a> / 
                                Software that can predict conserved elements and estimate a neutral model for PhyloAcc's input
                            </p>

                            <p>
                                <a href="http://www.iqtree.org/" target="_blank">IQ-TREE</a> / 
                                Maximum likelihood phylogenetic inference that is used in the PhyloAcc pipeline when estimating branch lengths on a species tree
                            </p>

                            <p>
                                <a href="https://github.com/smirarab/ASTRAL" target="_blank">ASTRAL</a> / 
                                Species tree inference method used in the PhyloAcc pipeline to estimate branch lengths in coalescent units
                            </p>

                            <p>
                                <a href="https://github.com/lliu1871/mp-est" target="_blank">MP-EST</a> / 
                                Species tree inference software used to estimate branch lengths in coalescent units
                            </p>
                        </ul>

                    <h3>People</h3>
                        <ul>
                            <p>
                                <a href="https://xyz111131.github.io/zhirui_lab/" target="_blank">Zhirui Hu</a> / 
                                One of the lead developers of PhyloAcc
                            </p>

                            <p>
                                Han Yan / 
                                One of the lead developers of PhyloAcc</p>
                            <p>
                                <a href="https://gwct.github.io/" target="_blank">Gregg Thomas</a> / 
                                One of the lead developers of PhyloAcc
                            </p>

                            <p>
                                <a href="https://scholar.harvard.edu/tsackton" target="_blank">Timothy Sackton</a> / 
                                Director of the Harvard Bioinformatics group and developer of PhyloAcc
                            </p>

                            <p>
                                <a href="https://edwards.oeb.harvard.edu/" target="_blank">Edwards Lab</a> / 
                                PhyloAcc is developed in Scott Edwards' lab at the Harvard University Museuem of Comparative Zoology
                            </p>

                            <p>
                                <a href="https://sites.harvard.edu/junliu/" target="_blank">Jun Liu</a> / 
                                PhyloAcc is developed in Jun Liu's group in the Department of Statistics at Harvard University
                            </p>

                            <p>
                                <a href="https://informatics.fas.harvard.edu/" target="_blank">Harvard Informatics</a> / 
                                PhyloAcc is developed in the Harvard Informatics group
                            </p>
                        </ul>

                </div>
                <div class="col-1-24 margin-main"></div>
            </div>

        </div>
        <div class="col-3-24 margin-main"></div>
    </div>



    {footer}
</body>
"""

######################
# Main block
######################
pagefile = "links.html";
print("Generating " + pagefile + "...");
title = "PhyloAcc - Links"
page_style = "file";

head = RC.readHead(title, page_style);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));