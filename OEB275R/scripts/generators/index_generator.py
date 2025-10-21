############################################################
# For ConGen2020 site, 08.20
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

    <div class="main-content">

        <div class="row" id="section-cont">
            <div class="col-4-24" id="outer-margin"></div>
            <div class="col-16-24" id="section-col">
                <div class="row" id="sep-row"></div>
                <div class="row" id="section-row">
                    <div class="col-2-24" id="inner-margin"></div>
                    <div class="col-4-24" id="phyloacc-logo-col">
                        <img id="phyloacc-logo" src="img/phyloacc-logo2.png">
                    </div>
                    <div class="col-1-24" id="logo-margin"></div>
                    <div class="col-10-24" id="section-content">
                        <center>
                            <h1>Welcome to the <a href="https://phyloacc.github.io/" target="_blank">PhyloAcc</a> 
                                <a href="https://canvas.harvard.edu/courses/106414" target="_blank">OEB275R</a>
                                course!</h1>
                                <p>This web page will guide you through some of the activities we have planned for you today!</p>
                        </center>
                    </div>
                    <div class="col-1-24" id="logo-margin"></div>
                    <div class="col-4-24" id="phyloacc-logo-col">
                        <img id="phyloacc-logo" src="img/harvard-info-logo.png">
                    </div>
                    <div class="col-2-24" id="inner-margin"></div>
                </div>
                <div class="row" id="sep-row"></div>
            </div>
            <div class="col-4-24" id="outer-margin"></div>
        </div>

        <!--
        <a name="instructors"></a>
        <div class="row" id="section-header-cont">
            <div class="col-4-24" id="outer-margin"></div>
            <div class="col-16-24" id="section-header-row">
                <div id="section-header">Instructor</div>
            </div>
            <div class="col-4-24" id="outer-margin"></div>
        </div>
        <div class="row" id="section-cont">
            <div class="col-4-24" id="outer-margin"></div>
            <div class="col-16-24" id="section-col">
                <div class="row" id="section-row">
                    <div class="col-2-24" id="inner-margin"></div>
                    <div class="col-20-24" id="section-content">

                        <div id="sep_div"></div>

                        <div class="row" id="instructor">
                            <div class="col-4-24" id="inst-img-cont">
                                <img id="inst-img" src="img/gt.jpg">
                            </div>
                            <div class="col-20-24" id="inst-text">
                                <p><a href="https://gwct.github.io/" target="_blank">Gregg Thomas</a>: A bioinformatics scientist in the
                                    <a href="https://informatics.fas.harvard.edu/" target="_blank">FAS Informatics group</a> at Harvard University and recent postdoc
                                    at the <a href="http://www.thegoodlab.org/" target="_blank">University of Montana</a> where he studied the phylogenetics and comparative 
                                    genomics of the mouse and rat radiation. He got his PhD at <a href="https://hahnlab.sitehost.iu.edu/" target="_blank">Indiana University</a> where
                                    he worked on comparative genomics of arthropods, mutation rate evolution in primates, and convergent evolution using comparative genomics. In general,
                                    Gregg uses and develops computational methods to study molecular evolution and phylogenetics to determine what forces drive divergence and 
                                    adaptation between species.                                
                                </p>
                            </div>
                        </div>

                        <div id="sep_div"></div>

                        <div id="sep_div"></div>

                    </div>
                    <div class="col-2-24" id="inner-margin"></div>
                </div>
            </div>
            <div class="col-4-24" id="outer-margin"></div>
        </div>
        -->

        <a name="nav"></a>
        <div class="row" id="section-header-cont">
            <div class="col-4-24" id="outer-margin"></div>
            <div class="col-16-24" id="section-header-row">
                <div id="section-header">Navigation</div>
            </div>
            <div class="col-4-24" id="outer-margin"></div>
        </div>
        <div class="row" id="section-cont">
            <div class="col-4-24" id="outer-margin"></div>
            <div class="col-16-24" id="section-col">
                <div class="row" id="section-row">
                    <div class="col-2-24" id="inner-margin"></div>
                    <div class="col-20-24" id="section-content">
                        <p>In the nav bar at the top of the page you'll find links to navigate this workshop and to resources we've compiled. Come back to this page any time by clicking 
                            the <a href="#">Intro</a> link above. Go to the first page of the workhop by clicking on the <a href="start.html">Workshop</a> link above or the link below.
                            If you come across a term or file format you don't recognize, check the <a href="terms.html">Terminology</a> page to see if it's listed there.
                            A table of useful data science programs and their use-cases has been compiled as a resource under the <a href="programs.html">Programs</a> link. Finally, some other links have
                            been organized in the <a href="links.html">Links</a> page.
                        </p>

                        <p>Use the links below to start and navigate to various parts of the workshop.</p>

                        <center><h1><a href="start.html" id="start-btn">Get Started</a></h1></center>

                        <div class="row" id="link-row">
                            <div class="col-3-24" id="inner-margin"></div>
                            <div class="col-4-24" id="btm-link"><a href="marine-mammals.html">Marine mammal data</a></div>
                            <div class="col-3-24" id="inner-margin"></div>
                            <div class="col-4-24" id="btm-link"><a href="run-phyloacc.html">Running PhyloAcc</a></div>
                            <div class="col-3-24" id="inner-margin"></div>
                            <div class="col-4-24" id="btm-link"><a href="phyloacc-results.html">Analyzing PhyloAcc results</a></div>
                            <div class="col-3-24" id="inner-margin"></div>
                        </div>
                        <div id="sep_div"></div>
                    </div>
                    <div class="col-2-24" id="inner-margin"></div>
                </div>
            </div>
            <div class="col-4-24" id="outer-margin"></div>
        </div>   
    </div>

    {footer}
</body>
</html>
"""

######################
# Main block
######################
pagefile = "index.html";
print("Generating " + pagefile + "...");
year = RC.getYear();
title = "PhyloAcc OEB275R - " + year

head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));