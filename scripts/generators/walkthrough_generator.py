############################################################
# For Referee docs, 11.19
# This generates the file "walkthrough.html"
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
    
<a class="internal-link" name="install"></a>
    <div class="row" id="body-row">
        <div class="col-4-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Coming soon!</span>
                
                <!--
                <ul>
                    <li><a href="readme.html#install">Installation</a></li>
                    <li><a href="readme.html#inputs">Inputs</a></li>
                    <li><a href="readme.html#usage">Usage</a></li>
                    <ol>
                        <li><a href="readme.html#st">Species tree model</a></li>
                        <li><a href="readme.html#gt">Gene tree model</a></li>
                        <li><a href="readme.html#adaptive">Adaptive model</a></li>
                        <li><a href="readme.html#snakemake">Executing snakemake</a></li>
                        <li><a href="readme.html#gather">Gather outputs</a></li>
                    </ol>
                    <li><a href="readme.html#output">Output</a></li>
                    <ol>
                        <li><a href="readme.html#elem_lik">elem_lik.txt</a></li>
                        <li><a href="readme.html#id-key">id_key.txt</a></li>
                        <li><a href="readme.html#elem_z">elem_z.txt</a></li>
                        <li><a href="readme.html#rate_postZ">rate_postZ_M*.txt</a></li>
                    </ol>
                    <li><a href="readme.html#options">Options</a></li>
                    <ol>
                        <li><a href="readme.html#io">Input/output</a></li>
                        <li><a href="readme.html#mcmc">MCMC</a></li>
                        <li><a href="readme.html#scf">sCF</a></li>
                        <li><a href="readme.html#batch">Batching</a></li>
                        <li><a href="readme.html#cluster">Cluster</a></li>
                        <li><a href="readme.html#phyloacc">PhyloAcc</a></li>
                        <li><a href="readme.html#misc">Miscellaneous</a></li>
                    </ol>
                </ul>
                -->

            </div>
        </div>

        <div class="col-20-24" id="main-content-col-page">

            <div class="row" id="top-row-cont">
                <div class="col-24-24" id="top-row"></div>
            </div>

            <div class="header">
                PhyloAcc Walkthrough
            </div>

            <center>
                <h3>Coming soon!</h3>
            </center>
            

            <!--
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Installation</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                With Anaconda already setup, Phyloacc can be installed with the command <code class="inline">conda install phyloacc</code>.
                                For more detailed installation instructions, see the <a href="">install page</a>.
                            </p>

                            <p>
                                Note that PhyloAcc is currently only compatible on Linux and OSX operating systems.
                            </p>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>


            <a class="internal-link" name="inputs"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Inputs</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                You will need the following data to perform an analysis with PhyloAcc
                            </p>

                            <ol>
                                <li>
                                    A set of <b>alignments</b> for a set of species from the regions you wish to estimate substitution rates for (e.g. CNEEs).
                                </li>

                                <li>
                                    A phylogenetic tree in Newick format from the same set of species with branch lengths estimated in terms of relative
                                    number of substitutions corresponding to neutral/background substitution rates.
                                </li>

                                <li>
                                    A transition rate matrix for bases in the neutral/background model.
                                </li>

                                <p>
                                    (2) and (3) can be obtained running <a href="http://compgen.cshl.edu/phast/phyloFit-tutorial.php" target="_blank">phyloFit</a> on alignments
                                    of likely neutrally evolving sites (e.g. 4-fold degenerate sites in genes) and will be given in a single .mod file output from that program.
                                </p>

                                <li>
                                    For running the gene tree model, a phylogenetic tree with the same topology as the one provided in (2), but with branch lengths in 
                                    coalescent units. This can be obtained from species tree inference methods like
                                    <a href="http://faculty.franklin.uga.edu/lliu/mp-est" target="_blank">MP-EST</a> or 
                                    <a href="https://github.com/smirarab/ASTRAL" target="_blank">ASTRAL</a>. 
                                    PhyloAcc has the capability to to estimate this directly from the input alignments with the <code class="inline">--theta</code> option,  
                                    by building locus trees using
                                    <a href="http://www.iqtree.org/" target="_blank">IQ-TREE</a> 
                                    and then using those as input to 
                                    <a href="https://github.com/smirarab/ASTRAL" target="_blank">ASTRAL</a>. This will be done for at most the 5000 longest alignments that are
                                    longer than 100bp and have at least 20% informative sites. These requirements are to ensure there is phylogenetic signal to infer this tree
                                    given that some inputs to PhyloAcc may be conserved and have few variable sites.
                                    However, you must be sure the alignments you are estimating rates for with PhyloAcc are also suitable for tree inference if you use this
                                    option. Also note that using the <code class="inline">--theta</code> option may significantly add to the runtime of the workflow.
                                </li>
                            </ol>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>
            -->

        </div>
    </div>

    {footer}
</body>
"""

######################
# Main block
######################
pagefile = "walkthrough.html";
print("Generating " + pagefile + "...");
title = "PhyloAcc - Walkthrough"
page_style = "file";

head = RC.readHead(title, page_style);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));