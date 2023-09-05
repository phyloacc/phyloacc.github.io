############################################################
# For Referee docs, 11.19
# This generates the file "index.html"
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

					<div class="col-20-24" id="title-col">
						<h1>Bayesian estimation of lineage specific substitution rates in conserved non-coding regions while accounting for phylogenetic discordance</h1>
					</div>
					<div class="col-2-24 margin"></div>
				</div>

				<div class="sep-div-small"></div>

				<div class="row" id="install-row">
					<div class="col-2-24 margin"></div>
					<div class="col-20-24" id="install-col">

						<h2>Install</h2>

						<p>
							For those with the most up to date version of Anaconda installed, you can 
							<a href="https://bioconda.github.io/recipes/phyloacc/README.html" target="_blank">install PhyloAcc with bioconda</a>
							in a fresh environment with a single command:
						</p>

						<div id="install-cont">
							<code>conda install phyloacc</code>
						</div>

						<h3>
							For more help or troubleshooting installation, please see the <a href="https://phyloacc.github.io/install.html">Install page</a>.
						</h3>

						<div class="row" id="title-row">
							<div class="col-2-24 margin"></div>
							<div class="col-20-24" id="title-col">
								<center>
									<a href="https://bioconda.github.io/recipes/phyloacc/README.html" target="_blank">
										<img src="https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg?style=flat" />
										<img src="https://anaconda.org/bioconda/phyloacc/badges/platforms.svg" />
										<img src="https://img.shields.io/conda/vn/bioconda/phyloacc?label=version" />
										<img src="https://anaconda.org/bioconda/phyloacc/badges/latest_release_date.svg" />
										<img src="https://img.shields.io/conda/dn/bioconda/phyloacc.svg?style=flat" />
									</a>
									<a href="https://github.com/phyloacc" target="_blank">
										<img src="https://img.shields.io/github/commits-since/phyloacc/PhyloAcc/v2.0.0" />
										<img src="https://anaconda.org/bioconda/phyloacc/badges/license.svg" />
									</a>
									
								</center>
							</div>
							<div class="col-2-24 margin"></div>
						</div>

					</div>
					<div class="col-2-24 margin"></div>
				</div>

				<div class="row" id="about-row">
					<div class="col-2-24 margin"></div>
					<div class="col-20-24" id="about-col">

						<h2>About</h2>
						<p>
							PhyloAcc is a program to detect shifts of DNA substitution rates in noncoding, conserved genomic regions. It can be used to identify genomic elements
							that have experienced accelerated rates along certain lineages in a phylogeny. This can be used, for example, to identify convergent rate shifts
							that coincide with phenotypic convergence.
						</p>

						<p>
							Substitution rates are estimated per lineage in the input species tree while accounting for underlying phylogenetic discordance. Three separate models
							are fit to the data: one allowing only conserved or background rates on all lineages, one allowing accelerated rates on specified target lineages, and a full model
							that allows accelerated rates on every lineage. The likelihoods of these nested models are compared for each element with Bayes Factors and questions
							can be formulated based on these comparisons.

							<!--
							The underlying model assumes a latent discrete state (Z) of relative substitution 
							rate along each branch of the phylogeny. This rate can be classifed as neutral, conserved, or accelerated. For each genomic element, PhyloAcc assumes a neutral 
							or conserved state at the common ancestor of the phylogeny, transit to conserved state if not yet being conserved and then reach an accelerated 
							state in some lineages. Our method utilizes adaptive collapsed Gibbs sampling to obtain the pattern of substitution rate shifts (posterior 
							distribution of Z) as well as relative substitution rates of conserved and accelerated state. To identify DNA elements that have accelerated rates on 
							specific branches, we compare marginal likelihoods under three models: a null model (M0) where all branches are neutral or conserved; an accelerated 
							model (M1) in which branches leading to target species are accelerated; and a full model (M2), with no constraints on latent states. Then we use 
							two Bayes factors: between M1 and M0 (BF1) and between M1 and M2 (BF2) as criteria to identify DNA elements accelerated exclusively in target 
							lineages.
							-->
						</p>

						<div id="buttons_container">
								<a class="main-btn" href="https://phyloacc.github.io/install.html">Install &raquo;</a><span id="buffer"></span>
								<a class="main-btn" href="readme.html">README &raquo;</a><span id="buffer"></span>
								<a class="main-btn"" href="https://github.com/phyloacc/PhyloAcc/issues" target="_blank">Report Issue &raquo;</a>
						</div>

						<h2>Citations</h2>
                        <p id="paper">
							Yan H, Hu Z, Thomas GWC, Edwards SV, Sackton TB, Liu JS.
							2023.
							PhyloAcc-GT: A Bayesian method for inferring patterns of substitution rate shifts on targeted lineages accounting for gene tree discordance.
							<em>Molecular Biology and Evolution</em>
							<a href="https://doi.org/10.1093/molbev/msad195" target="_blank">10.1093/molbev/msad195</a>
						</p>
                        
                        Version 1 (the "species tree" version):
						<p id="paper">
							Hu Z, Sackton TB, Edwards SV, Liu JS.
							2019.
							Bayesian detection of convergent rate changes of conserved noncoding elements on phylogenetic trees.
							<em>Molecular Biology and Evolution</em>
							<a href="https://doi.org/10.1093/molbev/msz049" target="_blank">10.1093/molbev/msz049</a>
						</p>


					</div>
					<div class="col-2-24 margin"></div>
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
pagefile = "index.html";
print("Generating " + pagefile + "...");
title = "PhyloAcc"
page_style = "NA"

head = RC.readHead(title, page_style);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));