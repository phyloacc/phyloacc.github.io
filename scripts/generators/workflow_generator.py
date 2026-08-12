############################################################
# This generates the file "workflow.html", a sub-page of
# walkthrough.html covering the phyloacc-workflows repo
# (currently: predicting CNEEs from a whole-genome alignment
# with phastCons). Not linked from the top nav bar; reached
# from walkthrough.html.
############################################################

import sys, os
sys.path.append(os.path.abspath('../lib/'))
import read_chunks as RC

######################
# phyloP power-calculation math
# (kept as its own raw string, spliced in via {phylop_math} below, so its
# literal LaTeX braces don't need escaping for html_template's .format() call)
######################

phylop_math = r"""
<p>
    Per-site phyloP scores each base for conservation with the following formula:

    \[ p = \operatorname{erfc}\!\left(\sqrt{\mathrm{LRT}/2}\right), \qquad \mathrm{LRT} = 2\left[\ln L(\hat\rho) - \ln L(1)\right] \]

    where \(\mathrm{LRT}\) measures how much better a slower-than-neutral (conserved) model fits the base
    than the neutral model: a larger \(\mathrm{LRT}\) gives a smaller \(p\), <em>i.e.</em> stronger evidence of
    conservation, and \(\operatorname{erfc}\) is the complementary error function. phyloP reports these
    as scores, \(-\log_{10} p\).
</p>

<p>
    These scores have a <b>ceiling</b> (\(\mathrm{LRT}_{\max}\)), which is determined mainly by the total neutral tree depth
    (substitutions/site) and the number of species in the tree, with a smaller contribution from the
    substitution rate itself (a model whose fastest base turns over more quickly than average raises the
    ceiling). Concretely, the largest \(\mathrm{LRT}\) a site can reach, which sets that ceiling, is
    capped by whichever of two limits is smaller:

    \[ \mathrm{LRT}_{\max} \approx \min\!\Big(\underbrace{2\,T\,\max_b(-Q_{bb})}_{\text{depth}\,\times\,\text{rate}},\ \ \underbrace{2(n-1)\big(-\ln \min_b \pi_b\big)}_{\text{species}\,\times\,\text{composition}}\Big) \]

    The first term grows with the tree depth \(T\) and the fastest base's exit rate \(\max_b(-Q_{bb})\); the
    second with the number of species \(n\) and the rarest base's frequency \(\min_b\pi_b\). The ceiling
    follows whichever term is smaller, so too little depth, or too few species, each cap it.
</p>

<p>
    Then, since millions of sites are being tested, we must correct the resulting scores for multiple tests. 
    This results in a multiple-testing threshold that is set by the number of sites being tested and the desired false-positive rate:

    \[ \text{threshold} = \log_{10}\!\left(M/\alpha\right) \]

    where \(M\) is the number of sites tested and \(\alpha\) the desired false-positive rate — the more
    sites tested, the higher the bar.
</p>

<p>
    If phyloP's score ceiling falls below the multiple-testing threshold, no site is detectable, regardless of how conserved it is.
</p>

<p>
    In other words, conserved sites are detectable only when:

    \[ -\log_{10}\operatorname{erfc}\!\left(\sqrt{\mathrm{LRT}_{\max}/2}\right)\;\ge\;\log_{10}(M/\alpha) \]

    This is the condition under which the tree's best-possible score clears the correction for \(M\) tested sites at level
    \(\alpha\). The ceiling rises with tree depth but eventually saturates, so two things can
    leave phyloP powerless: <b>too little total tree depth</b>, or <b>too few species</b>. Deep,
    taxon-rich trees are comfortably detectable; shallow or
    few-taxon trees need element-based conservation instead.
</p>
"""

######################
# HTML template
######################

html_template = """
<!doctype html>
    {head}

<body>
    {nav}

<a class="internal-link" id="overview"></a>
    <div class="row" id="body-row">
        <div class="col-4-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Page contents</span>
                <ul>
                    <li><a href="workflow.html#overview">Overview</a></li>
                    <ul>
                        <li><a href="workflow.html#cons-method">Conservation scoring method and power</a></li>                    
                    </ul>
                    <li><a href="workflow.html#download">Installing the workflow</a></li>
                    <ol>
                        <li><a href="workflow.html#clone">Clone the repository</a></li>
                        <li><a href="workflow.html#check-conda">Ensure conda is installed</a></li>
                        <li><a href="workflow.html#setup-env">Set up the conda environment</a></li>
                    </ol>
                    <li><a href="workflow.html#inputs">Preparing your inputs</a></li>
                    <ol>
                        <li><a href="workflow.html#required-inputs">Required inputs</a></li>
                        <li><a href="workflow.html#config-file">Pipeline config file</a></li>
                        <ul>
                            <li><a href="workflow.html#config-template">Config template</a></li>
                            <li><a href="workflow.html#chromosome-ids">Matching chromosome IDs</a></li>
                            <li><a href="workflow.html#gc-correction">GC content correction of neutral models (phyloFit)</a></li>
                            <li><a href="workflow.html#splitting">Splitting the alignment into chunks (phastCons)</a></li>
                            <li><a href="workflow.html#rho-estimation">Estimating rho, or using a global value (phastCons)</a></li>
                            <li><a href="workflow.html#phylop-clustering">Conserved site prediction and clustering (phyloP)</a></li>
                            <li><a href="workflow.html#filtering">Filtering parameters</a></li>
                            <li><a href="workflow.html#rule-resources">Specifying resources</a></li>
                            <li><a href="workflow.html#config-reference">Full config reference</a></li>
                        </ul>
                    </ol>
                    <li><a href="workflow.html#running">Running the workflow</a></li>
                    <ol>
                        <li><a href="workflow.html#dryrun">Dry run</a></li>
                        <li><a href="workflow.html#execute">Executing the workflow</a></li>
                        <li><a href="workflow.html#rerunning">Re-running and troubleshooting</a></li>
                    </ol>
                    <li><a href="workflow.html#outputs">Outputs</a></li>
                </ul>
            </div>
        </div>

        <div class="col-20-24" id="main-content-col-page">

            <div class="row" id="top-row-cont">
                <div class="col-24-24" id="top-row"></div>
            </div>

            <div class="header">
                Walkthrough: Predicting conserved elements and neutral models from a whole-genome alignment
            </div>

            <img class="fig-img" src="img/fig1-workflows.png" alt="">

            <center>
                <p><a href="walkthrough.html">&laquo; Back to the PhyloAcc walkthrough overview</a></p>
            </center>

            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Overview</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                A typical set of loci for analysis with PhyloAcc are conserved non-exonic elements (CNEEs). The
                                <a href="https://github.com/phyloacc/phyloacc-workflows" target="_blank">phyloacc-workflows</a> repository contains
                                Snakemake workflows that take a whole-genome alignment (in MAF format) and a reference genome annotation (in GFF format) and produce
                                a set of neutral substitution models and trees (one per scaffold/chromosome), conserved elements, and a final set of CNEE alignments ready to hand to
                                <code class="inline">PhyloAcc</code> (see the <a href="readme.html#inputs">README</a> for how PhyloAcc uses these
                                as input).
                            </p>

                            <p>
                                The pipeline works in three broad stages, each of which can be turned on or off independently in the config file:
                            </p>

                            <ol>
                                <li>
                                    <b>Neutral model estimation</b>: 4-fold degenerate codons are extracted from the alignment and used to fit a
                                    neutral substitution model with <code class="inline">phyloFit</code>.
                                </li>
                                <li>
                                    <b>Conservation scoring</b>: the alignment is split into manageable chunks, and scored with either
                                    <code class="inline">phastCons</code> or <code class="inline">phyloP</code> against the neutral model to call conserved regions.
                                    Users can choose one or both methods, depending on how their data scale both in terms of power and computationally.
                                    See <a href="workflow.html#cons-method">below</a> for more details.
                                </li>
                                <li>
                                    <b>CNEE extraction</b>: conserved regions overlapping coding sequence (from a GFF) are removed, short remaining
                                    fragments are dropped, and the surviving elements are extracted as individual FASTA or MAF alignments.
                                </li>
                            </ol>

                            <p>
                                The pipeline splits the alignment by chromosome/scaffold, both for scalability and to allow for chromosome-specific neutral models.
                                This also means you will end up running PhyloAcc for each chromosome/scaffold separately, rather than on the whole genome at once.
                            </p>

                            <p>
                                Outputs of the pipeline include the neutral models and trees (<code class="inline">.mod</code> files), and the final CNEE alignments 
                                (FASTA files).
                            </p>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <a class="internal-link" id="cons-method"></a>
                            <h2>Conservation scoring method and power</h2>

                            <p>
                                The workflow can use either <code class="inline">phastCons</code> or <code class="inline">phyloP</code> to score conservation.
                                <code class="inline">phastCons</code> aggregates information across sites to directly predict conserved regions, while 
                                <code class="inline">phyloP</code> scores each site independently and requires a separate clustering step to call conserved regions.
                            </p>

                            <p>
                                In general, <code class="inline">phyloP</code> lacks the power to predict conserved sites on small trees, and therefore <code class="inline">phastCons</code>
                                is usually the preferred method (and is the default). However, it can be slow on very large trees, and <code class="inline">phyloP</code>+clustering may be 
                                the only practical option in those cases.
                            </p>

                            <p>
                                If running <code class="inline">phyloP</code>, a power calculation will be performed prior to execution to determine whether the tree is too small to reliably detect conserved sites. 
                                If so, the workflow will exit with an error and suggest switching to <code class="inline">phastCons</code>, or overriding and running <code class="inline">phyloP</code> anyway,
                                which may still result in no conserved sites being detected.
                            </p>

                            <p>
                                One or both of <code class="inline">phyloP</code> and <code class="inline">phastCons</code> can be run in the same workflow, and the config file allows you to
                                specify which method to use with the main workflow switches (<code class="inline">run_phylop</code> and <code class="inline">run_phastcons</code>;
                                see <a href="workflow.html#config-reference">below</a>).
                            </p>

                            Expand the section below to see rough theoretical cutoffs for <code class="inline">phyloP</code>'s power, based on the total neutral tree depth (substitutions/site), number of taxa, and the number of sites tested:

                            <a class="internal-link" id="phylop-power"></a>
                            <details class="fig-toggle">
                                <summary><b><code class="inline">phyloP</code> Power Calculations (click to expand)</b></summary>
                                <center><img class="fig-img fig-img-plot" src="img/phylop-generic-detectability.png" alt="Plot showing that whether per-site phyloP can detect a conserved site depends on total neutral tree depth (x-axis, substitutions/site) and the number of sites tested (y-axis): shallow trees are power-limited regardless of taxon sampling, deeper trees are detectable, with a boundary band in between that depends on taxon sampling."></center>
                                {phylop_math}
                            </details>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>                            

            <br>

            <a class="internal-link" id="download"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Installing the workflow</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <a class="internal-link" id="clone"></a>
                            <h2>1. Clone the repository</h2>

                            <p>
                                Use the following command to clone the repository:
                            </p>

                            <pre class="cmd"><code>git clone https://github.com/phyloacc/phyloacc-workflows.git</code></pre>

                            <p>
                                If you do not have or wish to use git, download the archive directly from GitHub or with the following command:
                            </p>

                            <pre class="cmd"><code>wget https://github.com/phyloacc/phyloacc-workflows/archive/main.zip</code></pre>

                            <p>

                            </p>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="caution_banner">Note - Work in the phyloacc-workflows directory, or provide full paths to the workflow files.</div>
                                    <div id="caution_text">
                                        <p>
                                            Everything below assumes your working directory is the phyloacc-workflows directory. If you work from a different
                                            directory, you may always provide the full path to the workflow files.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            <br>
                            
                            <a class="internal-link" id="check-conda"></a>
                            <h2>2. Ensure conda is installed</h2>

                            <p>
                                The workflow uses conda to manage dependencies. You can check if conda is installed with 
                                <code class="inline">conda --version</code>. If you don't have conda (<em>i.e.</em> if conda command 
                                returns a "command not found" error), check out our tutorial to install it:
                            </p>

                            <center><a class="main-btn" href="https://informatics.fas.harvard.edu/resources/tutorials/installing-command-line-software-conda-mamba/" target="_blank">Installing conda &raquo;</a></center>
                            <br>

                            <a class="internal-link" id="setup-env"></a>
                            <h2>3. Set up the conda environment</h2>

                            <p>
                                The repository includes a small wrapper script, <code class="inline">phyloacc_workflows</code>, that manages a
                                dedicated conda environment for you with all the required dependencies. <!--(with <code class="inline">snakemake</code>, <code class="inline">samtools</code>,
                                <code class="inline">picard</code>, <code class="inline">phast</code> 
                                (<code class="inline">phyloFit</code> and <code class="inline">phastCons</code>),
                                <code class="inline">ncbi-datasets-cli</code>, and <code class="inline">mafutils</code>) so you don't need to install
                                any of these by hand. --> To create it, run:
                            </p>

                            <center><pre class="cmd"><code>./phyloacc_workflows setup</code></pre></center>

                            <p>
                                This creates a conda environment named
                                <code class="inline">phyloacc-workflows</code>.
                                You can confirm the environment is ready at any time with:
                            </p>

                            <center><pre class="cmd"><code>./phyloacc_workflows check</code></pre></center>

                            <p>
                                If you ever change <code class="inline">envs/environment.yml</code> or pull an update that changes it, re-running
                                <code class="inline">./phyloacc_workflows setup</code> will update the existing environment rather than recreate it
                                from scratch.
                            </p>

                            <p>
                                The wrapper has a few other subcommands too (run <code class="inline">./phyloacc_workflows --help</code> for the full
                                list).
                            </p>

                            <!--
                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="rec_banner">Tip - running multiple versions side-by-side</div>
                                    <div id="rec_text">
                                        <p>
                                            If you need more than one copy of the environment (for example, to test a change without disturbing your
                                            working setup), pass <code class="inline">--env-name</code> before the subcommand, or set the
                                            <code class="inline">PHYLOACC_ENV_NAME</code> environment variable:
                                        </p>

                                        <center><pre class="cmd"><code>./phyloacc_workflows --env-name phyloacc-workflows-test setup</code></pre></center>

                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            -->

                            <p>
                                If <code class="inline">./phyloacc_workflows: Permission denied</code> shows up when you try to run it, make the
                                script executable and try again:
                            </p>

                            <center><pre class="cmd"><code>chmod +x phyloacc_workflows</code></pre></center>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="caution_banner">Note - this environment is set up for SLURM</div>
                                    <div id="caution_text">
                                        <p>
                                            <code class="inline">envs/environment.yml</code> installs
                                            <code class="inline">snakemake-executor-plugin-slurm</code>, so <code class="inline">-e slurm</code> works
                                            out of the box. If your cluster uses a different scheduler, you'll need to
                                            install the matching Snakemake executor plugin yourself and pass its name to <code class="inline">-e</code>
                                            instead. See the
                                            <a href="https://snakemake.github.io/snakemake-plugin-catalog/" target="_blank">Snakemake plugin catalog</a>
                                            for the full list of available executors.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            <br>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" id="inputs"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Preparing your inputs</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <a class="internal-link" id="required-inputs"></a>
                            <h2>1. Required inputs</h2>

                            <p>
                                This workflow works in two steps: 1) predict neutral models (one per chromosome) and then 2) using the neutral models, 
                                predict conserved elements. These steps require the following inputs:
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Input</th>
                                        <th>File format</th>
                                        <th>Config key</th>
                                        <th>Description</th>
                                    </tr>
                                    <tr>
                                        <td><b>Whole-genome alignment</b></td>
                                        <td>MAF</td>

                                        <td><code class="inline">maf</code></td>
                                        <td>The alignment the pipeline scans for conserved elements. If you don't have one yet, see
                                        <a href="walkthrough.html#wga">generating a whole-genome alignment</a> in the walkthrough overview.</td>
                                    </tr>
                                    <tr>
                                        <td><b>Reference genome annotation</b></td>
                                        <td>GFF</td>
                                        <td><code class="inline">ref_gff</code></td>
                                        <td>During whole genome alignment, a reference species is specified for the coordinate system in the MAF file.
                                        The GFF annotation for this species is necessary to extract 4-fold degenerate sites for neutral model estimation 
                                        and to exclude coding sequence from the final CNEEs.</td>
                                    </tr>
                                    <tr>
                                        <td><b>Species tree</b></td>
                                        <td>Newick</td>
                                        <td><code class="inline">tree_file</code></td>
                                        <td>The topology is used when estimating the neutral model. If you ran the
                                        <a href="walkthrough.html#wga">Cactus snakemake</a> pipeline to generate your whole-genome alignment, you should
                                        already have this. If you have a .hal file from a previous alignment, you can extract the tree with the
                                        <a href="https://github.com/ComparativeGenomicsToolkit/hal" target="_blank">HAL tools</a> command
                                        <code class="inline">halStats <hal file> --tree</code>. Otherwise, you will have to infer or obtain a tree.</td>
                                    </tr>
                                </table>
                            </div>

                            <p>
                                The paths to these files and other pipeline options are specified in a single YAML config file, described in the pipeline configuration section.
                            </p>                            

                            <a class="internal-link" id="config-file"></a>
                            <h2>2. Pipeline config file</h2>

                            <p>
                                Everything the workflow needs, including the paths to the raw inputs above is specified in a single YAML config file. YAML is a format
                                that works by pairing keys and values as <code class="inline">key: value</code> pairs. The keys are provided and represent
                                specific settings the workflow needs, and you fill in the values.
                            </p>

                            <a class="internal-link" id="config-template"></a>
                            <h3>Config template</h3>

                            <p>
                                There are two ways to get a starting config file. Either works; pick whichever suits you.
                            </p>

                            <p>
                                <b>Quick start (recommended):</b> generate a config with the required
                                fields left blank:
                            </p>

                            <center><pre class="cmd"><code>./phyloacc_workflows init -o my-config.yaml</code></pre></center>

                            <p>
                                <b>Full reference:</b> alternatively, copy the fully-commented template if you'd rather have every
                                option documented inline as you fill it in (also available at
                                <a href="https://github.com/phyloacc/phyloacc-workflows/blob/main/config-template.yaml" target="_blank">config-template.yaml</a>).
                                Copy it from the link above or the internal path below from your local copy of the repository:
                            </p>

                            <center><pre class="cmd"><code>cp config-template.yaml my-config.yaml</code></pre></center>

                            <p>
                                Open <code class="inline">my-config.yaml</code> in an editor and fill in 
                                the following config keys, along with a few other required settings:
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Config key</th>
                                        <th>Description</th>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf</code></td>
                                        <td>Path to the whole-genome alignment described above.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">tree_file</code></td>
                                        <td>Path to the species tree described above.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf_ref_id</code></td>
                                        <td>The species label used for the reference genome in the MAF (the one whose coordinates the MAF, and
                                        ultimately the CNEEs, are reported in). See <a href="workflow.html#chromosome-ids">below</a>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_gff</code></td>
                                        <td>Path to the GFF annotation for the reference genome described above.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_chromosome_groups</code></td>
                                        <td>The reference chromosomes/scaffolds to analyze, organized into named groups (see
                                        <a href="workflow.html#chromosome-ids">below</a>). Group names are organizational only and do not affect the
                                        analysis. They simply become subdirectories of your output.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">output_dir</code></td>
                                        <td>Where all workflow outputs will be written. Created automatically if it doesn't already exist.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">tmp_dir</code></td>
                                        <td>A directory for temporary files. Make sure it has sufficient space as whole-genome MAFs and their
                                        intermediate splits can be large.</td>
                                    </tr>
                                </table>
                            </div>

                            <p>
                                There are many other settings in the config file that are commented within it. In the following sections we highlight
                                a few that are important to understand to know if you need to adjust them for your dataset.
                            </p>
                            
                            <a class="internal-link" id="chromosome-ids"></a>
                            <h3>Matching chromosome IDs</h3>

                            <h4>Relevant config keys: <code class="inline">ref_chromosome_groups</code>, <code class="inline">maf_ref_id</code>,
                                <code class="inline">maf_ref_chr_joiner</code>, <code class="inline">maf_prefix</code>, <code class="inline">gff_prefix</code></h4>

                            <p>
                                A common source of early errors is that the reference chromosome/scaffold IDs don't line up between the MAF and the
                                reference GFF.
                            </p>

                            <p>
                                The easiest solution to this is for the user to match the IDs prior to running the pipeline, most likely by editing
                                the GFF file.
                            </p>

                            <p>
                                However, the pipeline itself provides a method to handle this automatically, <b>as long as the labels share a core ID 
                                (<em>e.g.</em> "chr1" and "1", with "1" being the core)</b>, by specifying a prefix for the MAF and GFF chromosome names.
                                The settings for this are confusing, which is why pre-editing the IDs is recommended. Click below if you'd like to read more about how
                                the prefix system works.
                            </p>

                            <details class="fig-toggle">
                                <summary>Show details on the maf_prefix/gff_prefix system</summary>

                                <p>
                                    The <code class="inline">ref_chromosome_groups</code> key should contain a <em>core ID</em> for each
                                    chromosome/scaffold. The workflow derives each scaffold's actual name from it in the following way:
                                </p>

                                <ul>
                                    <li><b>GFF chromosome name</b> = <code class="inline">gff_prefix</code> + core ID.</li>
                                    <li><b>MAF chromosome name</b> = <code class="inline">maf_prefix</code> + core ID.</li>
                                </ul>

                                <p>
                                    The MAF file itself then is formatted as:
                                </p>

                                <ul>
                                    <li><b>MAF's full <code class="inline">src</code> field</b> = <code class="inline">maf_ref_id</code> +
                                        <code class="inline">maf_ref_chr_joiner</code> + <code class="inline">maf_prefix</code> + core ID.</li>
                                </ul>

                                <p>
                                    <code class="inline">maf_ref_id</code> and <code class="inline">maf_ref_chr_joiner</code> are the species/assembly
                                    prefix on the MAF's full <code class="inline">src</code> field (<em>e.g.</em> the
                                    <code class="inline">Homo_sapiens.</code> in <code class="inline">Homo_sapiens.chr1</code>) &mdash; a separate layer from
                                    <code class="inline">maf_prefix</code>/<code class="inline">gff_prefix</code>, which only prefix the chromosome name
                                    itself.
                                </p>

                                <p>For example, if the MAF's <code class="inline">src</code> field looks like <code class="inline">Homo_sapiens.chr1</code>
                                and the GFF just calls that chromosome <code class="inline">1</code>, you'd set:</p>

                                <pre class="long-cmd"><code>maf_ref_id: "Homo_sapiens"
maf_ref_chr_joiner: "."
maf_prefix: "chr"
gff_prefix: ""</code></pre>

                                <p>and list <code class="inline">"1"</code> under <code class="inline">ref_chromosome_groups</code>.</p>

                                <p>In the opposite case, if the MAF's <code class="inline">src</code> field is <code class="inline">Homo_sapiens.1</code>
                                but the GFF calls that chromosome <code class="inline">chr1</code>:</p>

                                <pre class="long-cmd"><code>maf_ref_id: "Homo_sapiens"
maf_ref_chr_joiner: "."
maf_prefix: ""
gff_prefix: "chr"</code></pre>

                                <p>again listing <code class="inline">"1"</code> under <code class="inline">ref_chromosome_groups</code>.</p>

                                <div id="msg_cont">
                                    <div id="msg">
                                        <div id="caution_banner">Note - the prefix pair only expresses a shared core, not arbitrary relabeling</div>
                                        <div id="caution_text">
                                            <p>
                                                <code class="inline">maf_prefix</code>/<code class="inline">gff_prefix</code> assume the MAF and GFF names
                                                share a common core ID once each file's literal prefix is stripped off (<em>e.g.</em>
                                                <code class="inline">chr1</code> vs <code class="inline">1</code>). They can't express arbitrary relabeling
                                                with no shared core. For example, MAF <code class="inline">chr1</code> against a GFF using
                                                accession-style names like <code class="inline">NC_000001.11</code> doesn't decompose into a prefix and a
                                                core ID.
                                            </p>
                                            <p></p>
                                        </div>
                                    </div>
                                </div>

                                <!--
                                <p>
                                    <code class="inline">maf_chr_prefix</code> (the old name for <code class="inline">maf_prefix</code>) still works as a
                                    deprecated alias. Separately, small version-suffix differences like <code class="inline">CM001009.3</code> vs
                                    <code class="inline">CM001009</code> are reconciled automatically via base-name matching, and aren't part of this
                                    prefix system.
                                </p>
                                -->
                            </details>

                            <a class="internal-link" id="gc-correction"></a>
                            <h3>GC content correction of neutral models (<code class="inline">phyloFit</code>)</h3>

                            <h4>Relevant config keys: <code class="inline">use_gc_corrected_models</code>, <code class="inline">sample_file</code></h4>

                            <p>
                                Because the neutral models are estimated from 4-fold degenerate sites and subsequently applied to the whole genome, if
                                those sites have different GC content the models may be inaccurate. <b>By default, the models are corrected for this by computing
                                GC content directly from the MAF.</b>
                            </p>

                            <p>
                                Alternatively, a <code class="inline">sample_file</code> can be provided for GC correction.
                                If a column called <code class="inline">accessions</code> exists in the sample file, the pipeline uses 
                                <code class="inline">ncbi-datasets-cli</code> to look up the GC content. If pre-computed GC values exist 
                                in a <code class="inline">gc</code> column, those values are used instead.
                                Both columns can exist and different samples can use different methods to provide GC content.
                            </p>

                            <p>
                                With the GC content read, the pipeline uses PHAST's <code class="inline">mod_freqs</code> script to adjust neutral models for each chromosome.
                            </p>                  

                            <p>
                                Set <code class="inline">use_gc_corrected_models: false</code> to disable GC correction.
                            </p>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="warn_banner">Warning - GC correction may or may not be necessary</div>
                                    <div id="warn_text">
                                        <p>
                                            In many species, the GC content of 4-fold degenerate sites is similar to the genome-wide GC content, and the
                                            correction may not make a difference. However, in others (<em>e.g.</em> Drosophila), the 4-fold degenerate
                                            sites differ from the genome overall, and the correction is important. If you are unsure,
                                            we recommend either confirming the consistency of GC content across your genomes or just running the workflow
                                            with the correction.
                                        </p>

                                        <p>
                                            And for these reasons, <code class="inline">use_gc_corrected_models: true</code> is the default setting in the config.
                                        <p></p>
                                    </div>
                                </div>
                            </div>

                            <a class="internal-link" id="splitting"></a>
                            <h3>Splitting the alignment into chunks (<code class="inline">phastCons</code>)</h3>

                            <h4>Relevant config keys: <code class="inline">split_strategy</code>, <code class="inline">num_seqs_max_for_gap</code>,
                                <code class="inline">num_seqs_min_gap_bp</code>, <code class="inline">num_seqs_min_keep_region_len</code></h4>

                            <p>
                                Before scoring conservation, each chromosome's alignment is split into smaller chunks, both for scalability, and
                                so that long stretches with little or no real alignment data don't get scored at all.
                                <code class="inline">split_strategy</code> controls how the pipeline decides where to split.
                            </p>

                            <p>
                                By default (<code class="inline">split_strategy: num_seqs</code>), the pipeline looks directly at the MAF's own
                                alignment blocks: any stretch where too few species are aligned is treated as a gap and used as a split point.
                                Three settings control split behavior:
                            </p>

                            <ul>
                                <li>
                                    <code class="inline">num_seqs_max_for_gap</code> (default <code class="inline">3</code>): a MAF block with this
                                    many species or fewer counts toward a "gap" run.
                                </li>
                                <li>
                                    <code class="inline">num_seqs_min_gap_bp</code> (default <code class="inline">100</code>): the minimum contiguous
                                    length of such a low-coverage run to actually count as a split point. Short blocks with low coverage may not be 
                                    true split points.
                                </li>
                                <li>
                                    <code class="inline">num_seqs_min_keep_region_len</code> (default <code class="inline">6</code>): chunks shorter
                                    than this, after splitting, are dropped.
                                </li>
                            </ul>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="caution_banner">Note - these defaults aren't a tuned recommendation</div>
                                    <div id="caution_text">
                                        <p>
                                            The <code class="inline">num_seqs_*</code> defaults are a starting point from exploratory analysis on one
                                            real alignment, not a tuned recommendation. Review the number and size of chunks they produce on your own
                                            data before trusting them.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>

                            <p>
                                Other split strategies include <code class="inline">ns</code> (split by Ns in a provided reference genome)
                                and <code class="inline">fixed_windows</code> (split into fixed-size windows). These are documented in the config template.
                            </p>                            

                            <a class="internal-link" id="rho-estimation"></a>
                            <h3>Estimating rho, or using a global value (<code class="inline">phastCons</code>)</h3>

                            <h4>Relevant config keys: <code class="inline">rho_mode</code>, <code class="inline">fixed_rho</code>, <code class="inline">global_rho_stat</code></h4>

                            <p>
                                <code class="inline">phastCons</code> needs a single "rho" parameter describing how conserved the alignment is overall
                                relative to the neutral model, and the pipeline applies one such value per chromosome to every chunk it scores. By
                                default (<code class="inline">rho_mode: fixed</code>), that's simply the value you set for
                                <code class="inline">fixed_rho</code> (default <code class="inline">0.3</code>), which we've found to be a reasonable
                                value for typical vertebrate datasets.
                            </p>

                            <p>
                                Alternatively, set <code class="inline">rho_mode: estimate</code> to instead have <code class="inline">phastCons</code> estimate rho
                                separately for each alignment chunk, then summarize those per-chunk estimates into a single chromosome-wide value using
                                <code class="inline">global_rho_stat</code> (<code class="inline">p90</code> (value of the 90th percentile of chunk estimates) by default, or
                                <code class="inline">median</code>/<code class="inline">mean</code> of the chunk estimates). Any chunk whose own estimated rho exceeds that
                                chromosome-wide value is skipped for conservation calling, rather than scored with an inflated rho.
                            </p>

                            <a class="internal-link" id="phylop-clustering"></a>
                            <h3>Conserved site prediction and clustering (<code class="inline">phyloP</code>)</h3>

                            <h4>Relevant config keys: <code class="inline">run_phylop</code>, <code class="inline">phylop_alpha</code>,
                                <code class="inline">phylop_power_gate</code>, <code class="inline">phylop_power_override</code>,
                                <code class="inline">phylop_power_num_sites</code>, <code class="inline">phylop_power_fallback_num_sites</code>,
                                <code class="inline">phylop_cluster_method</code>, <code class="inline">hmm_t0_0</code>, <code class="inline">hmm_t1_1</code>,
                                <code class="inline">hmm_e0_0</code>, <code class="inline">hmm_e1_1</code>, <code class="inline">hmm_s0</code>,
                                <code class="inline">hmm_min_len</code>, <code class="inline">hmm_max_len</code>, <code class="inline">naive_merge_gap_bp</code>,
                                <code class="inline">naive_min_region_sites</code>, <code class="inline">naive_min_region_len_bp</code>,
                                <code class="inline">windowed_window_bp</code>, <code class="inline">windowed_min_sites_per_window</code></h4>

                            <p>
                                The default pipline mode predicts conserved <b>elements</b> with <code class="inline">phastCons</code>, however this may be intractable 
                                for large alignments. In that case, you can use <code class="inline">phyloP</code> to predict conserved <b>sites</b> and then cluster them into elements.
                            </p>

                            <p>
                                To enable this, set <code class="inline">run_phylop: true</code> to additionally call conserved and accelerated sites with
                                <code class="inline">phyloP</code>, which tests each site in the alignment individually against the neutral model, rather
                                than scoring alignment chunks the way <code class="inline">phastCons</code> does (see
                                <a href="workflow.html#cons-method">conservation scoring method</a> above). Significant sites are then clustered into
                                regions and fed into the same CNEE-building stage as <code class="inline">phastCons</code>, producing a second,
                                independent set of CNEEs.
                            </p>

                            <p>
                                <b>Calling significant sites.</b> A site is called conserved or accelerated if it passes an FDR threshold,
                                <code class="inline">phylop_alpha</code> (default <code class="inline">0.05</code>), after Benjamini-Hochberg correction
                                across all sites on the chromosome.
                            </p>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="caution_banner">Caution - per-site calling needs a reasonably deep tree</div>
                                    <div id="caution_text">
                                        <p>
                                            Per-site conserved calling has a hard statistical-power limit on shallow trees: the most-conserved possible
                                            site can only clear a genome-wide FDR threshold once the total neutral tree length is large enough (roughly
                                            more than ~10 substitutions/site). Below that, <code class="inline">phyloP</code> will return few or no
                                            conserved sites by construction. On shallow-tree datasets, prefer
                                            <code class="inline">phastCons</code> instead.
                                        </p>

                                        <p>
                                            Power is checked before running <code class="inline">phyloP</code> on each chromosome (<code class="inline">phylop_power_gate</code>), 
                                            and the run stops with an explanation if the tree is too shallow. You can override this check with
                                        </p>

                                        <p>
                                            For theoretical baselines, see <a href="workflow.html#phylop-power">the power section</a> above.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>

                            <!--
                            <p>
                                Because of this, the pipeline checks the expected power before running <code class="inline">phyloP</code> on each
                                chromosome, controlled by <code class="inline">phylop_power_gate</code> (default <code class="inline">true</code>). If
                                the gate fails, the run stops with an explanation rather than silently returning an empty result; set
                                <code class="inline">phylop_power_override: true</code> to run anyway (with a warning) if you understand the limitation
                                and want to proceed. Set <code class="inline">phylop_power_gate: false</code> to disable the check entirely.
                            </p>
                            

                            <p>
                                The gate compares against <code class="inline">phylop_power_num_sites</code>, the number of sites (<em>M</em>) used in
                                the FDR bar <code class="inline">log10(M/alpha)</code>. By default (<code class="inline">estimate</code>), <em>M</em> is
                                the reference chromosome length, read from the MAF's own <code class="inline">srcSize</code> field (so no
                                <code class="inline">ref_fasta</code> is needed); if that's unavailable it falls back to
                                <code class="inline">ref_fasta</code>'s <code class="inline">.fai</code> index, and finally to
                                <code class="inline">phylop_power_fallback_num_sites</code> (default <code class="inline">100000000</code>). You can
                                also set <code class="inline">phylop_power_num_sites</code> to a fixed positive integer to use for every chromosome.
                            </p>
                            -->

                            <p>
                                <b>Clustering sites into regions.</b> Once significant sites are called, they need to be grouped into contiguous
                                regions before they can be turned into CNEEs. <code class="inline">phylop_cluster_method</code> controls how:
                            </p>

                            <ul>
                                <li>
                                    <b><code class="inline">hmm</code></b> (default): a simple 2-state online HMM (in/out of a conserved element) run
                                    over the per-position conserved/not-conserved stream.
                                </li>
                                <li>
                                    <b><code class="inline">gap_merge</code></b>: Merge significant sites that
                                    are close together, then drop regions that are too small or too short.
                                </li>
                                <li>
                                    <b><code class="inline">windowed</code></b>: bin the chromosome into fixed-size windows; a window is called
                                    conserved if it has enough significant sites, and adjacent conserved windows are merged.
                                </li>
                            </ul>

                            <p>Each method has its own set of tuning parameters, which are documented in <a href="workflow.html#config-reference">the full table below</a> and in the config template.</p>

                            <!--
                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Config key</th>
                                        <th>Default</th>
                                        <th>Used by</th>
                                        <th>Description</th>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_t0_0</code></td>
                                        <td><code class="inline">0.9</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td>Probability of staying outside a conserved element.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_t1_1</code></td>
                                        <td><code class="inline">0.99</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td>Probability of staying inside a conserved element. Higher values produce longer elements.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_e0_0</code></td>
                                        <td><code class="inline">0.8</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td>Probability of emitting a non-conserved position while outside an element.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_e1_1</code></td>
                                        <td><code class="inline">0.5</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td>Probability of emitting a conserved site while inside an element.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_s0</code></td>
                                        <td><code class="inline">0.9</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td>Probability of starting outside an element.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_min_len</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td>Minimum length (bp) for a predicted element to be kept.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_max_len</code></td>
                                        <td><code class="inline">100000</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td>Maximum length (bp) for a predicted element to be kept.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">naive_merge_gap_bp</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td><code class="inline">gap_merge</code></td>
                                        <td>Merge significant sites no more than this far apart into one region.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">naive_min_region_sites</code></td>
                                        <td><code class="inline">5</code></td>
                                        <td><code class="inline">gap_merge</code></td>
                                        <td>Drop regions with fewer than this many significant sites.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">naive_min_region_len_bp</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td><code class="inline">gap_merge</code></td>
                                        <td>Drop regions shorter than this.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">windowed_window_bp</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td><code class="inline">windowed</code></td>
                                        <td>Bin size in bp.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">windowed_min_sites_per_window</code></td>
                                        <td><code class="inline">5</code></td>
                                        <td><code class="inline">windowed</code></td>
                                        <td>Minimum number of significant sites for a bin to be called conserved.</td>
                                    </tr>
                                </table>
                            </div>
                            -->

                            <a class="internal-link" id="filtering"></a>
                            <h3>Filtering parameters</h3>

                            <h4>Relevant config keys: <code class="inline">filter_threshold_4d</code>, <code class="inline">max_gap_pct</code>,
                                <code class="inline">cnee_ces_merge_gap_bp</code>, <code class="inline">cnee_min_len_bp</code></h4>

                            <p>
                                Several thresholds control how aggressively data is filtered at different stages of the pipeline (see also
                                <a href="workflow.html#splitting">splitting the alignment into chunks</a> for the settings that control where chunk
                                boundaries themselves are placed):
                            </p>

                            <ul>
                                <li>
                                    <b>4-fold degenerate sites</b> (<code class="inline">filter_threshold_4d</code>, default
                                    <code class="inline">0.5</code>): sites used to fit the neutral model are dropped if more than this fraction of
                                    sequences are missing at that site.
                                </li>
                                <li>
                                    <b>Chunk quality</b> (<code class="inline">max_gap_pct</code>, default <code class="inline">0.9</code>): after
                                    splitting, a chunk is dropped entirely if more than this fraction of its non-reference alignment columns are gaps.
                                </li>
                                <li>
                                    <b>Final CNEE filtering</b> (<code class="inline">cnee_ces_merge_gap_bp</code>, default
                                    <code class="inline">5</code>; <code class="inline">cnee_min_len_bp</code>, default
                                    <code class="inline">50</code>): conserved regions within <code class="inline">cnee_ces_merge_gap_bp</code> bp of
                                    each other (after coding sequence is removed) are merged into a single element, and anything shorter than
                                    <code class="inline">cnee_min_len_bp</code> bp afterward is dropped.
                                </li>
                            </ul>

                            <p>
                                The defaults are reasonable for typical vertebrate-scale alignments, but you may want to loosen them for smaller or
                                more divergent datasets, or tighten them for very large ones.
                            </p>

                            <a class="internal-link" id="rule-resources"></a>
                            <h3>Specifying resources</h3>

                            <h4>Relevant config keys: <code class="inline">rule_resources</code></h4>

                            <p>
                                At the bottom of the config is a list of per-rule cluster resources, which the workflow passes to Snakemake when submitting jobs. 
                                The required resources depend on the number of species in the alignment and the size of the genomes. 
                                Many rules are fast and light and will use the <code class="inline">default</code> resouces. 
                                Others can be slow and memory-intensive and have their own resource settings.
                            </p>

                            <p>
                                <b>Values in the template are based on a benchmark of a 15 species alignment of mammals.</b> The config notes which rules should scale with
                                genome size and which with sample size. If you run out of memory or time on a rule, increase the resources for that rule in your config
                                file and re-run the workflow.
                            </p>

                            <a class="internal-link" id="config-reference"></a>
                            <h3>Full config reference</h3>

                            <p>
                                Every key recognized by the config file, in the order it appears in <code class="inline">config-template.yaml</code>:
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Config key</th>
                                        <th>Default</th>
                                        <th>Description</th>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf</code></td>
                                        <td><b>Required</b></td>
                                        <td>Path to the input MAF alignment.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf_ref_id</code></td>
                                        <td><b>Required</b></td>
                                        <td>Reference species label as it appears in the MAF (see <a href="workflow.html#chromosome-ids">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_gff</code></td>
                                        <td><b>Required</b></td>
                                        <td>Path to the reference genome's GFF annotation.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">tree_file</code></td>
                                        <td><b>Required</b></td>
                                        <td>Path to the Newick species tree.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_chromosome_groups</code></td>
                                        <td><b>Required</b></td>
                                        <td>Named groups of reference chromosomes/scaffolds to analyze.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">output_dir</code></td>
                                        <td><b>Required</b></td>
                                        <td>Output directory for the workflow.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">tmp_dir</code></td>
                                        <td><b>Required</b></td>
                                        <td>Directory for temporary files.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf_prefix</code></td>
                                        <td><code class="inline">""</code></td>
                                        <td>Prefix on the MAF chromosome name, relative to the core ID in <code class="inline">ref_chromosome_groups</code>
                                        (see <a href="workflow.html#chromosome-ids">above</a>). Replaces <code class="inline">maf_chr_prefix</code>, which
                                        still works as a deprecated alias.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">gff_prefix</code></td>
                                        <td><code class="inline">""</code></td>
                                        <td>Prefix on the GFF chromosome name, relative to the same core ID (see <a href="workflow.html#chromosome-ids">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf_ref_chr_joiner</code></td>
                                        <td><code class="inline">"."</code></td>
                                        <td>Character joining the reference ID and chromosome name in the MAF <code class="inline">src</code> field.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">filter_threshold_4d</code></td>
                                        <td><code class="inline">0.5</code></td>
                                        <td>Maximum fraction of sequences allowed to be missing at a 4-fold degenerate site (see <a href="workflow.html#filtering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">use_gc_corrected_models</code></td>
                                        <td><code class="inline">true</code></td>
                                        <td>Toggle GC correction of <code class="inline">phyloFit</code> models (see <a href="workflow.html#gc-correction">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">sample_file</code></td>
                                        <td>None; GC computed from the MAF if blank</td>
                                        <td>
                                            CSV sample sheet used for GC correction (see <a href="workflow.html#gc-correction">above</a>). Only
                                            relevant if <code class="inline">use_gc_corrected_models: true</code>, and optional even then &mdash; by
                                            default the pipeline calculates GC content directly from the sequences in the MAF. If a sample sheet is
                                            provided with a column called <code class="inline">accession</code>, GC content is instead looked up via
                                            NCBI assembly accessions; a column called <code class="inline">gc</code> can be supplied instead with
                                            precomputed values.
                                        </td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">accession_header</code></td>
                                        <td><code class="inline">accession</code></td>
                                        <td>Column name in <code class="inline">sample_file</code> holding NCBI assembly accessions.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">split_strategy</code></td>
                                        <td><code class="inline">num_seqs</code></td>
                                        <td><code class="inline">num_seqs</code> or <code class="inline">ns</code> (see <a href="workflow.html#splitting">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">num_seqs_max_for_gap</code></td>
                                        <td><code class="inline">3</code></td>
                                        <td>Max species count for a MAF block to count toward a gap run (see <a href="workflow.html#splitting">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">num_seqs_min_gap_bp</code></td>
                                        <td><code class="inline">100</code></td>
                                        <td>Minimum length of a low-coverage run to count as a split point (see <a href="workflow.html#splitting">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">num_seqs_min_keep_region_len</code></td>
                                        <td><code class="inline">6</code></td>
                                        <td>Minimum chunk length (bp) to keep, <code class="inline">split_strategy: num_seqs</code> (see <a href="workflow.html#splitting">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_fasta</code></td>
                                        <td><b>Required</b> if <code class="inline">split_strategy: ns</code></td>
                                        <td>Only needed if you set <code class="inline">split_strategy: ns</code> (see <a href="workflow.html#splitting">splitting the alignment into
                                        chunks</a>). This assembly is used to split the alignment into chunks based on runs of Ns; if it doesn't already
                                        have Ns in it, the assembly must be hard masked first.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_fasta_index</code></td>
                                        <td>Auto-generated if blank; only used if <code class="inline">split_strategy: ns</code></td>
                                        <td>Path to the reference FASTA's <code class="inline">.fai</code> index.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">min_Ns_to_split_by</code></td>
                                        <td><code class="inline">100</code></td>
                                        <td>Minimum run of Ns used as a split point, <code class="inline">split_strategy: ns</code> (see <a href="workflow.html#splitting">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">min_keep_region_len</code></td>
                                        <td><code class="inline">6</code></td>
                                        <td>Minimum chunk length (bp) to keep, <code class="inline">split_strategy: ns</code> (see <a href="workflow.html#splitting">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">max_gap_pct</code></td>
                                        <td><code class="inline">0.9</code></td>
                                        <td>Maximum non-reference gap fraction allowed before a chunk is filtered out (see <a href="workflow.html#filtering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">rho_mode</code></td>
                                        <td><code class="inline">fixed</code></td>
                                        <td><code class="inline">fixed</code> or <code class="inline">estimate</code> (see <a href="workflow.html#rho-estimation">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">fixed_rho</code></td>
                                        <td><code class="inline">0.3</code></td>
                                        <td>Fixed rho value used when <code class="inline">rho_mode: fixed</code>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">global_rho_stat</code></td>
                                        <td><code class="inline">p90</code></td>
                                        <td>Summary statistic (<code class="inline">p90</code>/<code class="inline">median</code>/<code class="inline">mean</code>)
                                        used when <code class="inline">rho_mode: estimate</code>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_output_format</code></td>
                                        <td><code class="inline">fasta</code></td>
                                        <td>Final CNEE alignment format: <code class="inline">none</code>, <code class="inline">fasta</code>, or
                                        <code class="inline">maf</code>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_ces_merge_gap_bp</code></td>
                                        <td><code class="inline">5</code></td>
                                        <td>Gap (bp) allowed when merging adjacent conserved regions into a single CNEE (see <a href="workflow.html#filtering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_min_len_bp</code></td>
                                        <td><code class="inline">50</code></td>
                                        <td>Minimum length (bp) for a conserved region to be kept as a CNEE (see <a href="workflow.html#filtering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_density_bin_bp</code></td>
                                        <td><code class="inline">1000000</code></td>
                                        <td>Bin width (bp) for the summary report's per-chromosome CNEE distribution plot. Cosmetic only &mdash; doesn't
                                        affect any CNEE calling or filtering.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_fasta_header</code></td>
                                        <td><code class="inline">species-coords-id</code></td>
                                        <td>Header format used for extracted CNEE FASTA sequences.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_expected_species</code></td>
                                        <td><code class="inline">""</code>; read from <code class="inline">tree_file</code> if blank</td>
                                        <td>Optional comma-separated species list to validate CNEE FASTA extraction against.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_expected_species_file</code></td>
                                        <td><code class="inline">""</code>; read from <code class="inline">tree_file</code> if blank</td>
                                        <td>Optional file with a newline-delimited species list, as an alternative to <code class="inline">cnee_expected_species</code>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">phylop_alpha</code></td>
                                        <td><code class="inline">0.05</code></td>
                                        <td>FDR threshold for calling a site conserved/accelerated (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">phylop_power_num_sites</code></td>
                                        <td><code class="inline">estimate</code></td>
                                        <td><em>M</em> for the power gate's FDR bar, or a fixed integer (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">phylop_power_fallback_num_sites</code></td>
                                        <td><code class="inline">100000000</code></td>
                                        <td>Fallback <em>M</em> if the MAF's <code class="inline">srcSize</code> and <code class="inline">ref_fasta</code>
                                        are both unavailable (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">phylop_cluster_method</code></td>
                                        <td><code class="inline">hmm</code></td>
                                        <td><code class="inline">hmm</code>, <code class="inline">gap_merge</code>, or <code class="inline">windowed</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_t0_0</code></td>
                                        <td><code class="inline">0.9</code></td>
                                        <td>Probability of staying outside a conserved element, <code class="inline">phylop_cluster_method: hmm</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_t1_1</code></td>
                                        <td><code class="inline">0.99</code></td>
                                        <td>Probability of staying inside a conserved element, <code class="inline">phylop_cluster_method: hmm</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_e0_0</code></td>
                                        <td><code class="inline">0.8</code></td>
                                        <td>Probability of emitting a non-conserved position while outside an element,
                                        <code class="inline">phylop_cluster_method: hmm</code> (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_e1_1</code></td>
                                        <td><code class="inline">0.5</code></td>
                                        <td>Probability of emitting a conserved site while inside an element,
                                        <code class="inline">phylop_cluster_method: hmm</code> (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_s0</code></td>
                                        <td><code class="inline">0.9</code></td>
                                        <td>Probability of starting outside an element, <code class="inline">phylop_cluster_method: hmm</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_min_len</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td>Minimum length (bp) for a predicted element to be kept, <code class="inline">phylop_cluster_method: hmm</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">hmm_max_len</code></td>
                                        <td><code class="inline">100000</code></td>
                                        <td>Maximum length (bp) for a predicted element to be kept, <code class="inline">phylop_cluster_method: hmm</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">naive_merge_gap_bp</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td>Merge gap (bp) between significant sites, <code class="inline">phylop_cluster_method: gap_merge</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">naive_min_region_sites</code></td>
                                        <td><code class="inline">5</code></td>
                                        <td>Minimum significant sites to keep a region, <code class="inline">phylop_cluster_method: gap_merge</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">naive_min_region_len_bp</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td>Minimum region length (bp) to keep, <code class="inline">phylop_cluster_method: gap_merge</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">windowed_window_bp</code></td>
                                        <td><code class="inline">20</code></td>
                                        <td>Bin size (bp), <code class="inline">phylop_cluster_method: windowed</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">windowed_min_sites_per_window</code></td>
                                        <td><code class="inline">5</code></td>
                                        <td>Minimum significant sites for a bin to be called conserved, <code class="inline">phylop_cluster_method: windowed</code>
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">rule_resources</code></td>
                                        <td>See <a href="workflow.html#rule-resources">above</a></td>
                                        <td>Per-rule cluster resources (see <a href="workflow.html#rule-resources">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf_split_chr_dir</code></td>
                                        <td><code class="inline">""</code></td>
                                        <td>Optional override for the chromosome-split MAF directory.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">phylofit_chr_dir</code></td>
                                        <td><code class="inline">""</code></td>
                                        <td>Optional override for the chromosome-specific <code class="inline">phyloFit</code> model directory.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">target_ref_chromosomes</code></td>
                                        <td><code class="inline">[]</code></td>
                                        <td>Optional subset of chromosomes to restrict analysis to, overriding <code class="inline">ref_chromosome_groups</code>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">debug_keep_intermediates</code></td>
                                        <td><code class="inline">false</code></td>
                                        <td>Keep intermediate files that would otherwise be cleaned up.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cleanup_chunk_intermediates</code></td>
                                        <td><code class="inline">true</code></td>
                                        <td>Remove per-chunk intermediate files once a chromosome finishes.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">keep_cnee_sidecars</code></td>
                                        <td><code class="inline">false</code></td>
                                        <td>Keep extra per-CNEE sidecar files produced during extraction.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">run_phylofit</code></td>
                                        <td><code class="inline">true</code></td>
                                        <td>Enable/disable the neutral model (<code class="inline">phyloFit</code>) stage.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">run_phylop</code></td>
                                        <td><code class="inline">true</code></td>
                                        <td>Enable/disable the <code class="inline">phyloP</code> conservation scoring stage (see
                                        <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">run_phastcons</code></td>
                                        <td><code class="inline">true</code></td>
                                        <td>Enable/disable the <code class="inline">phastCons</code> conservation scoring stage.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">build_cnees</code></td>
                                        <td><code class="inline">true</code></td>
                                        <td>Enable/disable CNEE extraction from the conserved regions.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">phylop_power_gate</code></td>
                                        <td><code class="inline">true</code></td>
                                        <td>Master switch for the <code class="inline">phyloP</code> statistical-power check (see
                                        <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">phylop_power_override</code></td>
                                        <td><code class="inline">false</code></td>
                                        <td>Run <code class="inline">phyloP</code> even when the power gate fails, with a warning instead of stopping
                                        (see <a href="workflow.html#phylop-clustering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">display</code></td>
                                        <td><code class="inline">false</code></td>
                                        <td>Print the resolved config and exit, without running anything (debugging).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">version</code></td>
                                        <td><code class="inline">false</code></td>
                                        <td>Print the pipeline version and exit.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">info</code></td>
                                        <td><code class="inline">false</code></td>
                                        <td>Print pipeline meta information and exit.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">debug</code></td>
                                        <td><code class="inline">false</code></td>
                                        <td>Enable verbose debug logging.</td>
                                    </tr>
                                </table>
                            </div>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" id="running"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Running the workflow</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <p>
                                The workflow is executed through the same <code class="inline">phyloacc_workflows</code> wrapper used for setup. Its
                                <code class="inline">run</code> subcommand activates the conda environment and passes everything you give it straight
                                through to <code class="inline">snakemake</code>, defaulting to the Snakefile in the repository unless you specify
                                your own with <code class="inline">-s</code>.
                            </p>

                            <a class="internal-link" id="dryrun"></a>
                            <h2>1. Dry run</h2>

                            <p>
                                Always start with a dry run to make sure the config file is valid and to see what jobs Snakemake plans to run, before
                                anything is actually submitted or executed:
                            </p>

                            <center><pre class="cmd"><code>./phyloacc_workflows run --configfile my-config.yaml -j 20 -e slurm --dryrun</code></pre></center>

                            <p>
                                Here, <code class="inline">-j 20</code> is the maximum number of jobs Snakemake will have in flight at once, and
                                <code class="inline">-e slurm</code> tells Snakemake to submit jobs to a SLURM cluster using the resources you set per
                                rule under <code class="inline">rule_resources</code> in your config file. If you're testing on a single machine
                                instead of a cluster, drop <code class="inline">-e slurm</code> and Snakemake will run everything locally using up to
                                <code class="inline">-j</code> CPU cores.
                            </p>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="caution_banner">Caution - don't run this on a login node without an executor</div>
                                    <div id="caution_text">
                                        <p>
                                            If you run <code class="inline">phyloacc_workflows run</code> without <code class="inline">-e/--executor</code>
                                            and without an active SLURM job allocation, the wrapper will print a warning: Snakemake will run every step
                                            directly on whichever machine you launched it from. On a shared cluster login node, that means real compute
                                            work running where it shouldn't. Either add <code class="inline">-e slurm</code>, or request an interactive
                                            allocation first.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>

                            <h4>Here is an example rulegraph for fitting neutral models and extracting CNEEs</h4>
                            
                            <center><a class="main-btn" href="https://github.com/phyloacc/phyloacc-workflows/blob/main/phylofit-phastcons-rulegraph.png" target="_blank">Pipeline rulegraph &raquo;</a></center>


                            <a class="internal-link" id="execute"></a>
                            <h2>2. Executing the workflow</h2>

                            <p>
                                Once the dry run looks right, drop <code class="inline">--dryrun</code> to actually run it:
                            </p>

                            <center><pre class="cmd"><code>./phyloacc_workflows run --configfile my-config.yaml -j 20 -e slurm</code></pre></center>
    
                            <p>
                                Depending on the size of your alignment and how many chromosomes/scaffolds you're analyzing, this can take anywhere
                                from minutes to many hours. Snakemake will print progress as jobs are submitted and complete, and each rule also
                                writes its own log under <code class="inline">&lt;output_dir&gt;/logs/&lt;rule name&gt;/</code> for closer
                                inspection.
                            </p>

                            <a class="internal-link" id="rerunning"></a>
                            <h2>3. Re-running and troubleshooting</h2>

                            <p>
                                Snakemake only re-runs rules whose outputs are missing or out of date, so if a run is interrupted or errors out, address the
                                cause of the failure and then run the exact same command again and it will pick up where it left off rather than starting over.
                            </p>

                            <p>
                                If a particular rule keeps failing, check its log file first, both under
                                <code class="inline">&lt;output_dir&gt;/logs/&lt;rule name&gt;/</code> and (for cluster runs) in the SLURM job's own
                                output. Common early culprits are a chromosome/scaffold ID that doesn't match between the MAF and GFF
                                (see <a href="workflow.html#chromosome-ids">Matching chromosome IDs</a>), or a cluster partition/resource in
                                <code class="inline">rule_resources</code> that doesn't exist on your system.
                            </p>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" id="outputs"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Outputs</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <p>
                                All outputs are written under the <code class="inline">output_dir</code> you set in your config file, organized into
                                numbered subdirectories reflecting the stage of the pipeline that produced them. The ones you'll care about most are:
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Path (relative to <code class="inline">output_dir</code>)</th>
                                        <th>Contents</th>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">02-neutral-model/phylofit/</code></td>
                                        <td>Per-chromosome neutral substitution models (<code class="inline">.mod</code> files) fit with
                                        <code class="inline">phyloFit</code>, GC-corrected by default.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">04-phastcons/regions/&lt;group&gt;/&lt;chromosome&gt;.bed</code></td>
                                        <td>All conserved regions called by <code class="inline">phastCons</code> for that chromosome, before coding
                                        sequence is removed.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">05-cnees/phastcons/bed/&lt;group&gt;/&lt;chromosome&gt;.cnees.bed4</code></td>
                                        <td>The final CNEE coordinates for that chromosome (BED4: chromosome, start, end, CNEE ID), with coding
                                        sequence removed and short fragments filtered out.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">05-cnees/phastcons/fasta/&lt;group&gt;/&lt;chromosome&gt;/</code></td>
                                        <td>One alignment file per CNEE (in the format set by <code class="inline">cnee_output_format</code>), plus a
                                        <code class="inline">manifest.txt</code> listing them. This directory is what you point PhyloAcc's
                                        <code class="inline">-d</code> option at (see the <a href="readme.html#inputs">README</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">logs/</code></td>
                                        <td>Per-rule log files, useful for troubleshooting failed or unexpected runs.</td>
                                    </tr>
                                </table>
                            </div>

                            <p>
                                If <code class="inline">run_phylop</code> is also enabled, CNEE building runs a second time on
                                <code class="inline">phyloP</code>'s clustered regions, writing an equivalent, independent set of outputs under
                                <code class="inline">05-cnees/phylop/</code> instead of <code class="inline">05-cnees/phastcons/</code>. With both stages
                                enabled you end up with two CNEE sets, one per method.
                            </p>

                            <p>
                                From here, the CNEE alignment directory for a chromosome (or all of them pooled together) is ready to hand straight to
                                <code class="inline">phyloacc.py</code> along with the neutral model produced above. See the PhyloAcc
                                <a href="readme.html">README</a> for how to set up and run PhyloAcc itself on these inputs.
                            </p>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <center>
                <p><a href="walkthrough.html">&laquo; Back to the PhyloAcc walkthrough overview</a></p>
            </center>

            <div class="sep_div"></div>

        </div>
    </div>

    <!-- dynamically load mathjax for compatibility with self-contained -->
    <script>
        (function () {{
            var script = document.createElement("script");
            script.type = "text/javascript";
            script.src  = "https://mathjax.rstudio.com/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML";
            document.getElementsByTagName("head")[0].appendChild(script);
        }})();
    </script>

    {footer}
</body>
"""

######################
# Main block
######################
pagefile = "workflow.html";
print("Generating " + pagefile + "...");
title = "PhyloAcc - phyloacc-workflows"
page_style = "file";

head = RC.readHead(title, page_style);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w", encoding="utf-8") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer, phylop_math=phylop_math));
