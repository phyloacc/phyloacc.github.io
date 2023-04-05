import sys
import os
import treec as tree

# ../../../PhyloAcc/src/PhyloAcc-interface/phyloacc.py -a simu_AccelerationPattern_CaseB.fasta -b simu_AccelerationPattern_CaseB.bed -m neut_ver3_genetree2.named.mod -m neut_ver3_genetree2.named.notheta.mod -o caseB-theta-reestimation -t "rhePen;rheAme" -g "galGal;nipNip;halLeu" -r gt --theta -n 12 -p 4 -j 12 -batch 14 -part "holy-info,shared" -time 8 --overwrite
# snakemake -p -s /n/home07/gthomas/projects/phyloacc/Yan-etal-2022/data/SimulatedData/caseB-theta-reestimation/phyloacc-job-files/snakemake/run_phyloacc.smk --configfile /n/home07/gthomas/projects/phyloacc/Yan-etal-2022/data/SimulatedData/caseB-theta-reestimation/phyloacc-job-files/snakemake/phyloacc-config.yaml --profile /n/home07/gthomas/projects/phyloacc/Yan-etal-2022/data/SimulatedData/caseB-theta-reestimation/phyloacc-job-files/snakemake/profiles/slurm_profile --dryrun

case = sys.argv[1];
if case not in ["A", "B", "C"]:
    sys.exit("case must be A, B, or C.")

subs_tree_file = "sims.tre";
theta_tree_file = "sims-theta.tre";
coal_tree_file = f"case{case}-coalescent.tre";

subs_tree = tree.Tree(open(subs_tree_file, "r").read())
subs_tree.showAttrib("label", "length", "type")

theta_tree = tree.Tree(open(theta_tree_file, "r").read())
theta_tree.showAttrib("label", "length", "clade")

coal_tree = tree.Tree(open(coal_tree_file, "r").read())
coal_tree.showAttrib("label", "length", "clade")

outfilename = f"case{case}-comps.tsv";
print("writing output file: " + outfilename);
with open(outfilename, "w") as outfile:
    headers = ["sim", "node", "label", "bl.subs", "bl.coal", "sim.theta", "est.theta"];
    outfile.write("\t".join(headers) + "\n");

    for node in subs_tree.nodes:
        if subs_tree.type[node] != "internal" or node == subs_tree.root:
            continue;

        #print(node);
        outline = [ case, node, subs_tree.label[node], subs_tree.bl[node], coal_tree.bl[node], theta_tree.bl[node] ];

        if float(coal_tree.bl[node]) != 0:
            est_theta = (2 * float(subs_tree.bl[node])) / float(coal_tree.bl[node]);
        else:
            est_theta = "NA"

        outline.append(str(est_theta));

        outfile.write("\t".join(outline) + "\n");

