############################################################
# For ConGen2020 site, 08.20
# This generates the file "programs.html"
############################################################

import sys, os, csv
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

    <a class="internal-link" name="top"></a>
    <div class="row" id="header">Data science programs</div>

    <div class="row" id="body-row">
        <div class="col-3-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Page contents</span>
                <ul>
                    <li><a href="programs.html#top">Intro</a></li>
                    <li><a href="programs.html#editor-table">Text editors</a></li>
                    <li><a href="programs.html#ft-table">File transfer programs</a></li>
                    <li><a href="programs.html#ssh-table">SSH clients</a></li>
                </ul>
            </div>
        </div>

        <div class="col-21-24" id="main-cont">
            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <p>
                                Part of becoming an efficient data scientist is trying out and learning the tools that work best for you. There are definitely plenty
                                out there to try. Here we have assembled lists of popular FREE software for common data science tasks. If you feel any information 
                                is inaccurate or out of date, or if you want to recommend a program to add to the lists, please contact 
                                <a href="https://gwct.github.io/" target="_blank">me</a>.
                            </p>

                            <p>Programs listed with a <span id="used-prog">GREEN BACKGROUND</span> are ones used in this workshop.</p>

                            <p>Programs listed with a * are the ones used by the authors of this workshop.</p>
                    
                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" name="editor-table"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Text editors</div>
                </div>
            </div>
            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <p>
                                Your text editor will be your most used program, and will be how you interact with your data,
                                 so its important to find one that does exactly what you need!
                            </p>

                            {editor_table}
                            <div id="sep_div"></div>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" name="ft-table"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">File transfer programs</div>
                </div>
            </div>
            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <p>
                                File transfer programs will allow you to move files between your machine and your lab's/institution's server,
                                or between servers. Sometimes you'll only want to move one or a few files to inspect them and a graphical, drag and
                                drop program is sufficient. Other times though you'll need to be moving thousands of files or very large files and
                                a command line file transfer may be required to automate the process. Below are a list of some popular programs of
                                each type.
                            </p>

                            <p>
                                Cloud services, like 
                                <a href="https://www.box.com/home" target="_blank">Box</a>, 
                                <a href="https://www.dropbox.com/?landing=dbv2" target="_blank">Dropbox</a>,
                                <a href="https://www.microsoft.com/en-us/microsoft-365/onedrive/online-cloud-storage" target="_blank">OneDrive</a>, or
                                <a href="https://www.google.com/drive/" target="_blank">Google Drive</a> are also extremely useful for syncing folders across devices, but can
                                be difficult to set up on a server. I personally use Box to store all of my active documents and project folders (sans
                                large data), and am able to sync between my home and work computers. These programs may not be free, but be sure to check with your
                                institution, which may offer free accounts with large or even unlimited storage while you work for them
                            </p>

                            {ft_table}
                            <div id="sep_div"></div>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" name="ssh-table"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">SSH clients to connect to remote servers</div>
                </div>
            </div>
            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <p>
                                <a href="https://en.wikipedia.org/wiki/Secure_Shell" target="_blank">SSH</a> is the protocol that allows us to connect our local
                                machine to a remote machine and run commands on it in the terminal. The most common SSH client is openSSH and is widely used. Until recently,
                                however, it was not available on Windows and a third-party client was required. PuTTY is by far the best SSH client for Windows, and is
                                still a great option for older versions or versions without openSSH installed.
                            </p>

                            {ssh_table}
                            <div id="sep_div"></div>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <!-- <a class="internal-link" name="other-table"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Other helpful programs</div>
                </div>
            </div>
            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            {other_table}
                            <div id="sep_div"></div>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div> -->
        
        </div>
    </div>

    {footer}
</body>
"""

table_template = """
<div class="table-cont">
    <table class="prog-table">
        {table_rows}
    </table>
</div>
"""

######################
# Main block
######################
pagefile = "programs.html";
print("Generating " + pagefile + "...");
year = RC.getYear();
title = "PhyloAcc OEB275R - " + year;

head = RC.readHead(title);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

tables = {'editor' : "../../data/text-editors.csv", 'ft' : "../../data/ftp.csv", 'ssh' : "../../data/ssh.csv", 'other' : "../../data/other.csv" };

for table in tables:
    #print(table);
    cur_rows, headers = "",  [];
    first = True;
    with open(tables[table]) as csvfile:
        table_reader = csv.reader(csvfile);
        for line in table_reader:
            if first:
                cur_rows += "<thead>";
                for col in line:
                    headers.append(col);
                    if col == "Used":
                        continue;
                    cur_rows += "<th>" + col + "</th>";
                cur_rows += "</thead>";
                first = False
                #print(headers);
                continue;
            # Get the header lines and add the <th> tags.

            #print(line);
            if line[-1] == "Y":
                cur_rows += "<tr id='used-prog'>";
            else:
                cur_rows += "<tr>";
            for c in range(len(line)):
                cur_header = headers[c];
                cur_col = line[c];
                cur_col = cur_col.replace('"', '');

                if cur_header == "Used":
                    continue;

                if cur_header == "Link":
                    cur_rows += "<td><a href='" + cur_col + "' target='_blank'>Website</a></td>";
                elif cur_header == "Paper":
                    cur_rows += "<td><a href='" + cur_col + "' target='_blank'>Paper</a></td>";
                else:
                    cur_rows += "<td>" + cur_col + "</td>";
            cur_rows += "</tr>";
            # Go through columns in rows to add <td> tags.

        if table == "editor":
            editor_table = table_template.format(table_rows=cur_rows);
        elif table == "ft":
            ft_table = table_template.format(table_rows=cur_rows);
        elif table == "ssh":
            ssh_table = table_template.format(table_rows=cur_rows);
        elif table == "other":
            other_table = table_template.format(table_rows=cur_rows);

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, editor_table=editor_table, ft_table=ft_table, ssh_table=ssh_table, other_table=other_table, footer=footer));