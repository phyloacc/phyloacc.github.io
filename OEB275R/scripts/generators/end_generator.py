############################################################
# For ConGen2020 site, 08.20
# This generates the file "end.html"
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
                    <center><h1>Thank you for attending the PhyloAcc course!</h1></center>

                    <div class="row" id="img-row">
                        <div class="col-7-24" id="margin"></div>
                        <div class="col-10-24" id="img-col">
                            <img id="res-img" src="img/pooh-meme.png">
                            <center><span class="fig-caption">Source unknown.</span></center>
                        </div>
                        <div class="col-7-24" id="margin"></div>
                    </div>

                    <!-- <p>Be sure to check out the <a href="programs.html">Programs</a> and <a href="terms.html">Terms</a> pages, and the slides for the lecture
                        and the workshop are available on the <a href="links.html">Links</a> page.</p> -->

                    <p>&nbsp;</p>
                    <p>&nbsp;</p>

                    <div id="sep_div"></div>
                    <div id="sep_div"></div>
                    <div id="sep_div"></div>
                    <div id="sep_div"></div>
                    <div id="sep_div"></div>
                </div>
                <div class="col-2-24" id="inner-margin"></div>
            </div>
        </div>
        <div class="col-4-24" id="outer-margin"></div>
    </div>

    <!--
    <div class="row" id="btm-nav">
        <div class="col-1-24" id="nav-bnt-margin"></div>
        <div class="col-8-24" id="nav-btn-cont">
            <div class="nav-btn">
                <a href="phyloacc-results.html">&lt;&nbsp;what is this go back</a>    
            </div>
        </div>
        <div class="col-12-24" id="nav-margin"></div>
        <div class="col-6-24" id="nav-btn-cont">
            <!-- <div class="nav-btn">
                <a href="end.html">Next?&nbsp;&gt;</a>
            </div> 
        </div>
        <div class="col-3-24" id="nav-btn-margin"></div>
    </div>
    -->

    {footer}
</body>
</html>
"""

######################
# Main block
######################
pagefile = "end.html";
print("Generating " + pagefile + "...");
year = RC.getYear();
title = "PhyloAcc OEB275R - " + year;

head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));