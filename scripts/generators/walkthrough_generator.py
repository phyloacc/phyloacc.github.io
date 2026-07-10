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

<a class="internal-link" id="overview"></a>
    <div class="row" id="body-row">
        <div class="col-4-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Page contents</span>
                <ul>
                    <li><a href="walkthrough.html#needs">Introduction</a></li>
                    <li><a href="walkthrough.html#infer-loci">Preparing required inputs</a></li>
                    <ul>
                        <li><a href="walkthrough.html#scratch">Starting from scratch</a></li>
                        <li><a href="walkthrough.html#species-tree">A note on the species tree</a></li>                                                    
                        <li><a href="walkthrough.html#wga">Phase 1:Generating a whole-genome alignment</a></li>
                        <li><a href="walkthrough.html#cnee-neutral-model">Phase 2: Predicting conserved elements and a neutral model</a></li>
                    </ul>

                    <li><a href="walkthrough.html#run-phyloacc">Running PhyloAcc</a></li>
                </ul>
            </div>
        </div>

        <div class="col-20-24" id="main-content-col-page">

            <div class="row" id="top-row-cont">
                <div class="col-24-24" id="top-row"></div>
            </div>

            <div class="header">
                PhyloAcc Walkthrough
            </div>

            <!-- <center>
                <h3>An overview of what PhyloAcc needs, and where to get it</h3>
            </center> -->

            <a class="internal-link" id="needs"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Introduction</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                PhyloAcc is a Bayesian method for detecting lineage-specific shifts in subsitution rates in a given multi-species alignment
                                with a corresponding phylogenetic tree and neutral model. It does this by allowing each lineage to belong to one of three
                                rate classes (conserved, neutral, accelerated) and fitting 3 models to the locus that differ in which lineages are allowed
                                to have different rates:
                            </p>

                            <ol>
                                <li>
                                    <b>M0 - null model</b>: all branches in the tree have the same neutral substitution rate
                                </li>
                                <li>
                                    <b>M1 - target model</b>: some target branches in the tree are allowed to have a different 
                                    accelerated substitution rates than the rest of the tree
                                </li>
                                <li>
                                    <b>M2 - full model</b>: all branches in the tree may have the conserved, neutral, or accelerated substitution rate
                                </li>
                            </ol>
                        
                            <p>
                                PhyloAcc compares the likelihood of each model using Bayes Factors to determine which model fits the data best for that
                                locus. If a model fits M1 best, then there is good evidence for lineage specific acceleration in the target branches.
                            </p>

                            <p>
                                PhyloAcc is generalizeable to any set of loci (though notably there is no codon model implemented yet), but the most
                                common use case is conserved non-exonic elements (CNEEs) or other noncoding regulatory elements.
                            </p>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" id="infer-loci"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Preparing required inputs</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <p>
                                PhyloAcc requires the following inputs to run:
                            </p>

                            <ol>
                                <li>
                                    <b>Sequence alignments</b> for the regions you're testing (<em>e.g.</em> CNEEs).
                                </li>
                                <li>
                                    <b>A neutral substitution model</b>: the expected, background rate of substitution in the absence of selection.
                                    This is estimated (e.g. with <code class="inline">phyloFit</code>) from putatively neutral sites, typically 4-fold
                                    degenerate sites in genes, and given to PhyloAcc as a <code class="inline">.mod</code> file (output from 
                                    <code class="inline">phyloFit</code>).
                                </li>
                                <li>
                                    <b>A phylogenetic tree</b>: for your species, with branch lengths in units of substitutions under the neutral model.
                                    You will need the species tree in Newick format beforehand and the branch lengths will be re-estimated by 
                                    <code class="inline">phyloFit</code> and bundled together with the substitution rate matrix in the same <code class="inline">.mod</code>.
                                    (PhyloAcc's gene tree model additionally needs a tree with branch lengths in coalescent units, which it may be able to estimate
                                    automatically.)
                                </li>
                            </ol>

                            <a class="internal-link" id="scratch"></a>
                            <h2>Starting from scratch</h2>

                            <h4>High level flowchart of inferring conserved elements and running PhyloAcc</h4>

                            <img class="fig-img" src="img/fig1.png" alt="Overview of inputs and pipelines: genome assemblies and a species tree go into a Cactus-snakemake pipeline to produce a whole-genome alignment (MAF); the MAF, a sample sheet, and a reference genome and annotation go into phyloacc-workflows to produce neutral substitution models and CNEE alignments; those are then fed into PhyloAcc to produce accelerated elements.">

                            <p>
                                If starting from scratch, in other words if you need to infer the conserved elements and neutral model yourself, you will 
                                need to generate a whole genome alignment in order to predict conserved elements and neutral models. This requires the following inputs:
                            </p>

                            <ol>
                                <li>
                                    The genome FASTA files of the species you wish to analyze.
                                </li>
                                <li>
                                    At least one annotated reference genome (GFF file).
                                </li>
                                <li>
                                    A Newick-formatted tree containing at least the topology of the species in the FASTA files.
                                </li>
                            </ol>

                            <a class="internal-link" id="species-tree"></a>
                            <h3>A note on the species tree</h3>

                            <p>
                                We don't currently provide guidance on inferring or acquiring a species tree since there are many ways to do so. However, at least a topology is
                                required for both the whole-genome alignment and inferring the neutral model. 
                            </p>

                            <p>
                                Here a a couple ways you could get a species tree:
                            </p>

                            <ul>
                                <li>
                                    Extract a tree from a published phylogeny of your species of interest.
                                </li>
                                <li>
                                    Infer a tree from a set of single-copy orthologs between your species. This is relatively easy if you already have orthologs identified, 
                                    but will require more work if not.
                                </li>
                            </ul>

                            <p>
                                We aim to provide more guidance on this in the future.
                            </p>

                            <a class="internal-link" id="wga"></a>
                            <h2>Phase 1: Generating a whole-genome alignment</h2>

                            <img class="fig-img" src="img/fig1-cactus.png" alt="">

                            <p>
                                A whole genome alignment (WGA) gives us access to any locus in the genome and is the best starting point for inferring both conserved elements
                                and neutral models. For this step, all you need are the genome FASTA files of each species you want to include in your analysis and a species
                                tree in Newick format (branch lengths in units of expected substitutions per site are helpful, but just the topology is required). 
                            </p>

                            <p> 
                                We recommend
                                <a href="https://github.com/ComparativeGenomicsToolkit/cactus" target="_blank">Cactus</a> for building whole genome alignments. 
                                We have developed Snakemake workflows for running Cactus. Get started here:
                            </p>
                            
                            <center><a class="main-btn" href="https://informatics.fas.harvard.edu/resources/tutorials/whole-genome-alignment-cactus/" target="_blank">Cactus Snakemake tutorial &raquo;</a></center>

                            <p>
                                This will generate a whole-genome alignment in MAF format, which is the starting point for Phase 2.
                            </p>
                            
                            <a class="internal-link" id="cnee-neutral-model"></a>
                            <h2>Phase 2: Predicting conserved elements and a neutral model</h2>

                            <img class="fig-img" src="img/fig1-workflows.png" alt="">

                            <p>
                                With the whole-genome alignment MAF file, you can predict conserved elements and estimate a neutral model. You will also
                                need an annotation (GFF file) for at least one species in your alignment in order to extract 4-fold degenerate sites for estimating
                                the neutral model and a sample sheet (CSV file) that lists the species in your alignment (and optionally their corresponding NCBI accessions
                                or pre-calculated GC content).
                            </p>

                            <p>
                                We provide a set of <code class="inline">phyloacc-workflows</code> that fits a neutral model by chromosome with 
                                <code class="inline">phyloFit</code>, predicts conserved elements with <code class="inline">phastCons</code>, 
                                and extracts a final set of CNEE alignments. These are the direct inputs for PhyloAcc. See our walkthrough here:
                            </p>

                            <center><a class="main-btn" href="workflow.html">phyloacc-workflows walkthrough &raquo;</a></center>                
                            <br>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" id="run-phyloacc"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Running PhyloAcc</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <img class="fig-img" src="img/fig1-phyloacc.png" alt="">

                            <p>
                                Once you have your loci and neutral model (and tree), whether from your own alignments or from the
                                workflow above, head to the README for installing and running <code class="inline">PhyloAcc</code> itself,
                                including all inputs, usage examples, and options.
                            </p>

                            <center><a class="main-btn" href="readme.html">PhyloAcc README &raquo;</a></center>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>
            <div class="sep_div"></div>
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
