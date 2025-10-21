

############################################################
# For ConGen2021 site, 08.21
# This generates the file "advanced.html"
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

    <a class="internal-link" name="clone"></a>
   	<div class="row" id="header">Analyzing PhyloAcc results</div>

    
    <div class="row" id="body-row">
        <!--
        <div class="col-3-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Page contents</span>
                <ul>
					<li><a href="advanced.html#clone">Cloning the github repo</a></li>
					<li><a href="advanced.html#zip">Downloading a zip file</a></li>
                </ul>
            </div>
        </div>
        -->

        <div class="col-24-24" id="main-cont">

            <!-- ------- BEGIN SECTION ------- -->

            <div class="row" id="top-row-cont">
                <div class="col-24-24" id="top-row"></div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-1-24" id="inner-margin"></div>
                        <div class="col-22-24" id="section-content">

                            <p>
                                The rest of the workshop will be spent going through marine mammal data pre-run through PhyloAcc using RStudio and RMarkdown.
                            </p>

                            <center><h1>
                                <a href="https://github.com/gwct/oeb275r-phyloacc-data" target="_blank">Download data from github</a>
                            </h1></center>

                            <p>
                                To download the data, click on the link above and click on the green button labeled "Code" on the github page. Then click Download ZIP
                                and the download should start automatically.
                            </p>

                            <div class="row" id="img-row">
                                <div class="col-4-24" id="margin"></div>
                                <div class="col-16-24" id="img-col">
                                    <img id="res-img" src="img/github-zip.png">
                                    <center><span class="fig-caption">Figure 4.1: The location of the URL to download a zip file of the github repo.</span></center>
                                </div>
                                <div class="col-4-24" id="margin"></div>
                            </div>

                            <p>
                                We'll continue the class from the RMarkdown document in RStudio!
                            </p>

                            <center><h2>
                                A fully rendered page from the RMarkdown analysis is also available 
                                <a href="phyloacc_analyses.html" target="_blank">HERE</a> to follow along with in case technical issues arise.
                            </h2></center>

                            <div id="sep_div"></div>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="msg_banner">Tip - More info about git</div>
                                    <div id="msg_text">
                                        <p>
                                            If you're interested in learning more about git there are a ton of guides and docs out there for you to search for. To get
                                            started, I've put together a couple of how-tos for understanding git basics here:
                                        </p>

                                        <center><a href="https://github.com/goodest-goodlab/good-protocols/tree/main/how-tos" target="_blank">git how-tos</a></center>

                                        <p></p>
                                    </div>
                                </div>
                            </div>

                            <div id="sep_div"></div> 

                        </div>
                        <div class="col-1-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>
            
            <!-- -------- END SECTION -------- -->

        </div>
    </div>

    <div class="row" id="btm-nav">
        <div class="col-3-24" id="nav-bnt-margin"></div>
        <div class="col-6-24" id="nav-btn-cont">
            <div class="nav-btn">
                <a href="run-phyloacc.html">&lt;&nbsp;Previous</a>    
            </div>
        </div>
        <div class="col-12-24" id="nav-margin"></div>
        <div class="col-6-24" id="nav-btn-cont">
            <div class="nav-btn" id="end-btn">
                <a href="end.html">Next?&nbsp;&gt;</a>
            </div>
        </div>
        <div class="col-3-24" id="nav-btn-margin"></div>
    </div>


    {footer}
"""

######################
# Main block
######################
pagefile = "phyloacc-results.html";
print("Generating " + pagefile + "...");
year = RC.getYear();
title = "PhyloAcc OEB275R - " + year;

head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer, co="<code class='inline'>", cc="</code>"));
