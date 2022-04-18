############################################################
# For Referee docs, 11.19
# This generates the file "readme.html"
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

 <a class="internal-link" name="concepts"></a>
   	<div class="row" id="header">Command concepts</div>

    <div class="row" id="body-row">
        <div class="col-3-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Page contents</span>
                <ul>
                    <li><a href="commands.html#concepts">Commands as concepts</a></li>
                    <li><a href="commands.html#text-proc">Commands as text</a></li>
                    <li><a href="commands.html#text-editors">Text editors</a></li>
                    <li><a href="commands.html#philosophy">The Unix philosophy</a></li>
                    <li><a href="commands.html#pipe-redirect">Piping and redirecting</a></li>
                </ul>
            </div>
        </div>

        <div class="col-21-24" id="main-cont">

            <div class="row" id="top-row-cont">
                <div class="col-24-24" id="top-row"></div>
            </div>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">What is a command?</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                I think it is important to ground ourselves in some of the computational concepts that are common among data scientists and
                                bioinformaticians. This can again help to remove the black box of the computer and the terminal, and can improve our 
                                productivity as scientists. With that, I want to step back and just sort of reintroduce the concept of commands from the 
                                command line from a conceptual standpoint.
                            </p>

                            <p>
                                What is a command? A command is basically just a program or an app. It is a chunk of code that someone has written that takes
                                input, processes that input, and produces output. The really common and useful chunks of code (e.g. <code class="inline">ls</code>
                                or <code class="inline">cd</code>) have become mainstays in modern operating systems to the extent that we don't even need to 
                                think about the underlying code, but it is there.
                            </p>

                            <p>
                                The other main difference between commands and modern programs or apps is that they are invoked almost entirely in a text-based
                                terminal program. This provides versatility, as commands can be scripted to run in sequence, as well as the power to convey complex
                                instructions to the computer.
                            </p>

                            <p>
                                Imagine being in a country where you don't know the language. Maybe you go into a coffee shop and want to order something, but
                                without knowledge of the language, you basically have to resort to pointing at what you want on the menu. This is really effective! 
                                It can convey a lot of meaning and be really quick to get across some ideas. But there may be details that you can't convey because
                                they aren't on the menu, like that you wanted extra sugar in your coffee.
                            </p>

                            <p>
                                But if you knew the language you could easily get this information and much more complex and nuanced information across in
                                your order. This is the difference between using the mouse to convey instructions to the computer, and using text-based commands, 
                                and opens up a wide-range of possibilities for the user of the computer... though just like learning a new spoken language, 
                                it can be difficult to grasp at first.
                            </p>
 
                            <div class="row" id="img-row">
                                <div class="col-4-24" id="margin"></div>
                                <div class="col-16-24" id="img-col">
                                    <img id="res-img" src="img/coffee.png">
                                    <center><span class="fig-caption">Figure 3.1: Coffee ordered by pointing at the menu 
                                        <a href="https://pixabay.com/vectors/drink-coffee-tea-beverage-156144/" target="_blank">(left)</a> vs. coffee ordered 
                                        with language <a href="https://www.buzzfeednews.com/article/stephaniemcneal/venti-diabetes" target="_blank">(right)</a>.</span></center>
                                </div>
                                <div class="col-4-24" id="margin"></div>
                            </div>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

        </div>
    </div>






    {footer}
</body>
"""

######################
# Main block
######################
pagefile = "install.html";
print("Generating " + pagefile + "...");
title = "PhyloAcc - Install"

head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));