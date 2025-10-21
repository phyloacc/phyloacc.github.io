############################################################
# For ConGen2020 site, 08.20
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

    <div class="row" id="section-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-col">
            <div class="row" id="section-row">
                <div class="col-2-24" id="inner-margin"></div>
                <div class="col-20-24" id="section-content">
                    <h4>Find here a list of links to relevant resources.</h4>
                </div>
                <div class="col-2-24" id="inner-margin"></div>
            </div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>

    <a name="links"></a>
    <div class="row" id="section-header-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-header-row">
            <div id="section-header">OEB275R Workshop</div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>
    <div class="row" id="section-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-col">
            <div class="row" id="section-row">
                <div class="col-2-24" id="inner-margin"></div>
                <div class="col-20-24" id="section-content">

                    <ul id="links-list">
                        <li><a href="https://github.com/gwct/oeb275r-phyloacc-data" target="_blank">Data repo</a></li>
                    </ul>

                    <ul id="links-list">
                        <li><a href="https://canvas.harvard.edu/courses/106414" target="_blank">Course webpage</a></li>
                    </ul>                                                


                </div>
                <div class="col-2-24" id="inner-margin"></div>
            </div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>

    <div class="row" id="section-header-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-header-row">
            <div id="section-header">PhyloAcc</div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>
    <div class="row" id="section-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-col">
            <div class="row" id="section-row">
                <div class="col-2-24" id="inner-margin"></div>
                <div class="col-20-24" id="section-content">

                    <ul id="links-list">
                        <li><a href="https://phyloacc.github.io" target="_blank">Main website</a></li>
                    </ul>

                    <ul id="links-list">
                        <li><a href="https://github.com/phyloacc/PhyloAcc" target="_blank">Github organization</a></li>
                    </ul>

                    <ul id="links-list">
                        <li><a href="https://doi.org/10.1093/molbev/msz049" target="_blank">2019 Paper describing species tree model</a></li>
                    </ul>                                        

                </div>
                <div class="col-2-24" id="inner-margin"></div>
            </div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>

    <a name="other"></a>
    <div class="row" id="section-header-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-header-row">
            <div id="section-header">Literature & Resources</div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>
    <div class="row" id="section-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-col">
            <div class="row" id="section-row">
                <div class="col-2-24" id="inner-margin"></div>
                <div class="col-20-24" id="section-content">

                    <ul id="links-list">
                        <li><a href="http://compgen.cshl.edu/phast/index.php" target="_blank">PHAST: various phylogenetic sequence methods (including phastCons for identifying conserved elements and phyloFit for estimating neutral substitution rates)</a></li>
                    </ul>    

                    <ul id="links-list">
                        <li><a href="https://doi.org/10.1093/sysbio/syw018" target="_blank">Description of how phylogenetic discordance can influence estimates of substitution rates (Mendes & Hahn 2016)</a></li>
                    </ul>    

                    <ul id="links-list">
                        <li><a href="https://doi.org/10.1093/molbev/msaa106" target="_blank">Concordance factors (Minh et al. 2020)</a></li>
                    </ul>   

                    <ul id="links-list">
                        <li><a href="http://dx.doi.org/doi:10.1038/ng.3198" target="_blank">Convergent evolution in marine mammal protein coding genes (Foote et al. 2015)</a></li>
                    </ul>          

                    <ul id="links-list">
                        <li><a href="https://doi.org/10.1093/molbev/msw112" target="_blank">Another study on convergent evolution in marine mammal genomes (Chikina et al. 2016)</a></li>
                    </ul> 

                    <ul id="links-list">
                        <li><a href="https://doi.org/10.1093/molbev/msy147" target="_blank">BPP: More on Bayesian phylogenetics (Flouri et al. 2016)</a></li>
                    </ul>                                         

                    <ul id="links-list">
                        <li><a href="https://doi.org/10.1186/s12915-017-0434-y" target="_blank">General review of methods to detect selection in the genome (Booker et al. 2017)</a></li>
                    </ul>    

                </div>
                <div class="col-2-24" id="inner-margin"></div>
            </div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>

    <!--
    <a name="inst-links"></a>
    <div class="row" id="section-header-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-header-row">
            <div id="section-header">Instructors</div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>
    <div class="row" id="section-cont">
        <div class="col-4-24" id="outer-margin"></div>
        <div class="col-16-24" id="section-col">
            <div class="row" id="section-row">
                <div class="col-2-24" id="inner-margin"></div>
                <div class="col-20-24" id="section-content">

                    <ul id="links-list">
                        <li><a href="https://gwct.github.io/" target="_blank">Gregg Thomas</a> - Bioinformatics Scientist at Harvard University</li>
                    </ul>

                    <p>&nbsp;</p>
                    <p>&nbsp;</p>

                </div>
                <div class="col-2-24" id="inner-margin"></div>
            </div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>   
    -->

    {footer}
</body>
"""

######################
# Main block
######################
pagefile = "links.html";
print("Generating " + pagefile + "...");
year = RC.getYear();
title = "PhyloAcc OEB275R - " + year;

head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));