import sys
import treec as tree

# ../../../PhyloAcc/src/PhyloAcc-interface/phyloacc.py -a neutral/neutral_100_1.fasta -b neutral/neutral_100_1.bed -m neut_ver3_genetree2.named.notheta.mod -o neutral-theta-re-estimation-1 -t "rhePen;rheAme" -g "galGal;nipNip;halLeu" -r gt --theta -n 12 -p 4 -j 100 -batch 14 -part "holy-smokes,holy-info,shared" -time 8 --overwrite --nophyloacc --dev -inf-frac-theta 0.0
# snakemake -p -s /n/home07/gthomas/projects/phyloacc/Yan-etal-2022/data/SimulatedData/neutral-theta-re-estimation-1/phyloacc-job-files/snakemake/run_phyloacc.smk --configfile /n/home07/gthomas/projects/phyloacc/Yan-etal-2022/data/SimulatedData/neutral-theta-re-estimation-1/phyloacc-job-files/snakemake/phyloacc-config.yaml --profile /n/home07/gthomas/projects/phyloacc/Yan-etal-2022/data/SimulatedData/neutral-theta-re-estimation-1/phyloacc-job-files/snakemake/profiles/slurm_profile
# iqtree -t neut_ver3_genetree2.named.notheta.tre --tree-fix -p neutral-theta-re-estimation-1/phyloacc-job-files/iqtree/alns/ --prefix neutral-theta-re-estimation-1/phyloacc-job-files/iqtree/concat -T 1
# Need to root and rearrange concat tree... why does iqtree do that?

case = sys.argv[1];
if case not in ["1", "2", "3"]:
    sys.exit("case must be 1, 2, or 3.")

spec_tree_file = "sims.tre";
subs_tree_file = f"neutral-{case}-concat.tre";
theta_tree_file = "sims-theta.tre";
coal_tree_file = f"neutral-{case}-coalescent.tre";

subs_tree = tree.Tree(open(subs_tree_file, "r").read());
subs_tree.showAttrib("label", "length", "clade");
print(subs_tree.rooted);

theta_tree = tree.Tree(open(theta_tree_file, "r").read());
theta_tree.showAttrib("label", "length", "clade");
print(theta_tree.rooted);

coal_tree = tree.Tree(open(coal_tree_file, "r").read());
coal_tree.showAttrib("label", "length", "clade");
print(coal_tree.rooted);

spec_tree = tree.Tree(open(spec_tree_file, "r").read());
spec_tree.showAttrib("label", "length", "clade");
print(spec_tree.rooted);

outfilename = f"neutral-{case}-comps.tsv";
print("writing output file: " + outfilename);
with open(outfilename, "w") as outfile:
    headers = ["sim", "node", "label", "bl.spec", "bl.subs", "bl.coal", "input.theta", "est.theta"];
    outfile.write("\t".join(headers) + "\n");

    for node in subs_tree.nodes:
        if subs_tree.type[node] != "internal" or node == subs_tree.root:
            continue;

        #print(node);
        outline = [ case, node, subs_tree.label[node], spec_tree.bl[node], subs_tree.bl[node], coal_tree.bl[node], theta_tree.bl[node] ];

        if float(coal_tree.bl[node]) != 0:
            est_theta = (2 * float(subs_tree.bl[node])) / float(coal_tree.bl[node]);
        else:
            est_theta = "NA"

        outline.append(str(est_theta));

        outfile.write("\t".join(outline) + "\n");

