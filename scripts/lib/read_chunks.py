############################################################
# For murine web development, 11.17
# Functions to read static html chunks
############################################################

def readHead(title, page_style):
    headfile = "../html-chunks/head.html";
    return open(headfile, "r").read().replace("TMPTITLE", title).replace("PAGESTYLESHEET", page_style);

def readNav(active_url):
    navfile = "../html-chunks/nav.html";
    navlines = open(navfile, "r").readlines()
    for x in range(len(navlines)):
        if active_url in navlines[x]:
            navlines[x] = navlines[x].replace(active_url, "#");
            if 'class="nav-link"' in navlines[x]:
                navlines[x] = navlines[x].replace('class="nav-link"', 'class="nav-link" id="active"');
    return "".join(navlines);

def readFooter():
    import time, subprocess
    from datetime import datetime
    footerfile = "../html-chunks/footer.html";
    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S");
    zone = subprocess.check_output("date +%Z").decode().strip();
    return open(footerfile, "r").read().replace("DATETIME", now + " " + zone);

def readCalcs():
    calcsfile = "../html-chunks/calcs_main.html";
    return open(calcsfile, "r").read();

def readScores():
    calcsfile = "../html-chunks/scores_main.html";
    return open(calcsfile, "r").read();