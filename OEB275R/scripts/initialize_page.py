import sys, os

import lib.read_chunks as RC

######################
# Python template
######################

py_template = """

############################################################
# For ConGen2021 site, 08.21
# This generates the file "{name}.html"
############################################################

import sys, os
sys.path.append('..')
import lib.read_chunks as RC

######################
# HTML template
######################

html_template = \"\"\"
<!doctype html>
    {{head}}

<body>
    {{nav}}

    <a class="internal-link" name="SECTION 1 NAME"></a>
   	<div class="row" id="header">MAIN HEADER</div>

    <div class="row" id="body-row">
        <div class="col-3-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Page contents</span>
                <ul>
{links}
                </ul>
            </div>
        </div>

        <div class="col-21-24" id="main-cont">
            <div class="row" id="top-row-cont">
                <div class="col-24-24" id="top-row"></div>
            </div>

            {sections}

        </div>
    </div>

    <div class="row" id="btm-nav">
        <div class="col-3-24" id="nav-bnt-margin"></div>
        <div class="col-6-24" id="nav-btn-cont">
            <div class="nav-btn">
                <a href="PREVIOUS.html">&lt;&nbsp;Previous</a>    
            </div>
        </div>
        <div class="col-6-24" id="nav-margin"></div>
        <div class="col-6-24" id="nav-btn-cont">
            <div class="nav-btn">
                <a href="NEXT.html">Next&nbsp;&gt;</a>
            </div>
        </div>
        <div class="col-3-24" id="nav-btn-margin"></div>
    </div>

    {{footer}}
\"\"\"

######################
# Main block
######################
pagefile = "{name}.html";
print("Generating " + pagefile + "...");
title = "ConGen2021 - Intro to Bioinformatics"


head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer, co="<code class='inline'>", cc="</code>"));
"""

######################
# Section template
######################

section = """
            <!-- ------- BEGIN SECTION ------- -->

            <a class="internal-link" name="SECTION LINK"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">SECTION TITLE</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                        
                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <!-- -------- END SECTION -------- -->
"""

######################
# Link template
######################

link = '\t\t\t\t\t<li><a href="{name}.html#SECTION LINK">SECTION TITLE</a></li>\n'

######################
# Main block
######################

print()
print("###### Initialize page ######");
print("# PYTHON VERSION: " + ".".join(map(str, sys.version_info[:3])))
print("# Script call: " + " ".join(sys.argv) + "\n----------");

page_name = sys.argv[1];
num_sections = int(sys.argv[2]);
overwrite = True;

print("# Initializing page generator for " + page_name + " with " + str(num_sections) + " sections");
outfilename = "generators/" + page_name + "_generator.py";
overwrite = "x";

if os.path.isfile(outfilename):
    while overwrite not in ["y", "n"]:
        overwrite = input("WARNING: Output file named " + outfilename + " alredy exists! Overwrite? (y/n) ").lower();

    if overwrite == "n":
        sys.exit("Exiting to prevent overwrite.");
    else:
        print("Continuing to generate and OVERWRITE file.");

sections = "";
links = "";
for i in range(num_sections):
    sections += section;
    if i == 1:
        sections = sections.replace('<a class="internal-link" name="SECTION LINK"></a>', "");
    
    if i != 1:
        links += link.format(name=page_name);

with open(outfilename, "w") as outfile:
    outfile.write(py_template.format(name=page_name, links=links, sections=sections));

