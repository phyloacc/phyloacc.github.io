import sys, os, argparse

print()
print("###### Build site pages ######");
print("PYTHON VERSION: " + ".".join(map(str, sys.version_info[:3])))
print("# Script call: " + " ".join(sys.argv) + "\n----------");

parser = argparse.ArgumentParser(description="Gets stats from a bunch of abyss assemblies.");
parser.add_argument("--all", dest="all", help="Build all pages", action="store_true", default=False);
parser.add_argument("--index", dest="index", help="Without --all: build index.html. With --all: exlude index.html", action="store_true", default=False);
parser.add_argument("--start", dest="start", help="Without --all: build start.html. With --all: exlude start.html", action="store_true", default=False);
parser.add_argument("--marine", dest="marine", help="Without --all: build marine-mammals.html. With --all: exlude marine-mammals.html", action="store_true", default=False);
parser.add_argument("--run", dest="run", help="Without --all: build run-phyloacc.html. With --all: exlude run-phyloacc.html", action="store_true", default=False);
parser.add_argument("--results", dest="results", help="Without --all: build phyloacc-results.html. With --all: exlude phyloacc-results.html", action="store_true", default=False);
parser.add_argument("--end", dest="end", help="Without --all: build end.html. With --all: exlude end.html", action="store_true", default=False);
parser.add_argument("--terms", dest="terms", help="Without --all: build terms.html. With --all: exlude terms.html", action="store_true", default=False);
parser.add_argument("--programs", dest="programs", help="Without --all: build programs.html. With --all: exlude programs.html", action="store_true", default=False);
parser.add_argument("--links", dest="links", help="Without --all: build links.html. With --all: exlude links.html", action="store_true", default=False);
args = parser.parse_args();
# Input options.

#cwd = os.getcwd();
os.chdir("generators");

pages = {
    'index' : args.index,
    'start' : args.start,
    'marine' : args.marine,
    'run' : args.run,
    'results' : args.results,
    'end' : args.end,
    'terms' : args.terms,
    'programs' : args.programs,
    'links' : args.links
}

if args.all:
    pages = { page : False if pages[page] == True else True for page in pages };

if pages['index']:
    os.system("python index_generator.py");

if pages['start']:
    os.system("python start_generator.py");

if pages['marine']:
    os.system("python marine_mammal_generator.py");

if pages['run']:
    os.system("python run_phyloacc_generator.py");

if pages['results']:
    os.system("python phyloacc_results_generator.py");

if pages['end']:
    os.system("python end_generator.py");

if pages['terms']:
    os.system("python terms_generator.py");

if pages['programs']:
    os.system("python programs_generator.py");

if pages['links']:
    os.system("python links_generator.py");

print("----------\nDone!");


