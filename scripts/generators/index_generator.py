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
		<div class="col-3-24 margin"></div>
		<div class="col-18-24" id="main-content-col">

				<div class="row" id="title-row">
					<div class="col-2-24 margin"></div>
					<div class="col-20-24" id="title-col">
						<img class="pure-img" id="logo_main" src="img/ref-logo.png">
						<h1>PhyloAcc: Bayesian estimation of substitution rates in conserved non-coding regions along a phylogeny</h1>
					</div>
					<div class="col-2-24 margin"></div>
				</div>

				<div class="row header-row">
					<div class="col-2-24 margin"></div>
					<div class="col-20-24 header-col">
						<h2>
							Install
						</h2>
					</div>
					<div class="col-2-24 margin"></div>
				</div>

				<div class="row" id="install-row">
					<div class="col-2-24 margin"></div>
					<div class="col-20-24" id="install-col">
						<div id="install-cont">
							<code>conda install phyloacc</code>
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
							The underlying model assumes a latent discrete state (Z) of relative substitution 
							rate along each branch of the phylogeny. This rate can be classifed as neutral, conserved, or accelerated. For each genomic element, PhyloAcc assumes a neutral 
							or conserved state at the common ancestor of the phylogeny, transit to conserved state if not yet being conserved and then reach an accelerated 
							state in some lineages. Our method utilizes adaptive collapsed Gibbs sampling to obtain the pattern of substitution rate shifts (posterior 
							distribution of Z) as well as relative substitution rates of conserved and accelerated state. To identify DNA elements that have accelerated rates on 
							specific branches, we compare marginal likelihoods under three models: a null model (M0) where all branches are neutral or conserved; an accelerated 
							model (M1) in which branches leading to target species are accelerated; and a full model (M2), with no constraints on latent states. Then we use 
							two Bayes factors: between M1 and M0 (BF1) and between M1 and M2 (BF2) as criteria to identify DNA elements accelerated exclusively in target 
							lineages.
						</p>

						<div id="buttons_container">
								<a class="main-btn" href="#.html">README &raquo;</a><span id="buffer"></span>
								<a class="main-btn"" href="https://github.com/phyloacc/PhyloAcc/issues" target="_blank">Report Issue &raquo;</a>
						</div>

						<h2>Citation</h2>
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
		<div class="col-3-24 margin"></div>
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

head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));