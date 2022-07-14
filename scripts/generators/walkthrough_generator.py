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

            <center><h1>Coming soon!</h1></center>
        </div>
        <div class="col-3-24 margin-main"></div>
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