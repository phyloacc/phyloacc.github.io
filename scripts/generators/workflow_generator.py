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
                    <li><a href="workflow.html#download">Installing the workflow</a></li>
                    <ol>
                        <li><a href="workflow.html#clone">Clone the repository</a></li>
                        <li><a href="workflow.html#check-conda">Ensure conda is installed</a></li>
                        <li><a href="workflow.html#setup-env">Set up the conda environment</a></li>
                    </ol>
                    <li><a href="workflow.html#inputs">Preparing your inputs</a></li>
                    <ol>
                        <li><a href="workflow.html#required-inputs">Required inputs</a></li>
                        <li><a href="workflow.html#chromosome-ids">Matching chromosome IDs</a></li>
                        <li><a href="workflow.html#config-file">Building a config file</a></li>
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
                                Snakemake workflows that take a whole-genome alignment (in MAF format) and a reference genome and produce
                                a neutral substitution models and trees (one per chromosome), conserved elements, and a final set of CNEE alignments ready to hand to
                                <code class="inline">PhyloAcc</code> (see the <a href="readme.html#inputs">README</a> for how PhyloAcc uses these
                                as input).
                            </p>

                            <p>
                                The pipeline works in three broad stages, each of which can be turned on or off independently in the config file:
                            </p>

                            <ol>
                                <li>
                                    <b>Neutral model estimation</b>: 4-fold degenerate codons are extracted from the alignment and used to fit a
                                    neutral substitution model with <code class="inline">phyloFit</code>, optionally GC-corrected per chromosome.
                                </li>
                                <li>
                                    <b>Conservation scoring</b>: the alignment is split into manageable chunks and scored with
                                    <code class="inline">phastCons</code> against the neutral model to call conserved regions.
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
                                Outputs of the pipeline include the neutral model and tree (<code class="inline">.mod</code> files), and the final CNEE alignments 
                                (FASTA files).
                            </p>

                            <!--
                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="caution_banner">This walkthrough covers the phastCons/CNEE pipeline only</div>
                                    <div id="caution_text">
                                        <p>
                                            The <code class="inline">phyloacc-workflows</code> repository also contains work-in-progress pipelines for
                                            other, clustering-based approaches to predicting conserved elements. As of this writing, only the
                                            <code class="inline">phastCons</code>-based CNEE pipeline described here is complete and working, and it
                                            lives on the <code class="inline">dev</code> branch of the repository.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            -->

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

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
                                Everything the workflow needs is specified in a single YAML config file, a template of which is found in the repository at
                                <code class="inline">config-template.yaml</code>. Copy this template and fill
                                in the paths for your project (more on this <a href="workflow.html#config-file">below</a>). At minimum, you'll
                                need to gather the following before you start:
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Config key</th>
                                        <th>Description</th>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf</code></td>
                                        <td>The whole-genome alignment to scan for conserved elements, in MAF format.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">tree_file</code></td>
                                        <td>A Newick-formatted tree containing the species in the MAF.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf_ref_id</code></td>
                                        <td>The species label used for the reference genome in the MAF (the one whose coordinates the MAF, and
                                        ultimately the CNEEs, are reported in).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_fasta</code></td>
                                        <td>The FASTA file for the reference genome named in <code class="inline">maf_ref_id</code>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_fasta_index</code></td>
                                        <td>The <code class="inline">.fai</code> index for <code class="inline">ref_fasta</code>. This must literally
                                        be <code class="inline">ref_fasta + ".fai"</code>; if it doesn't exist yet the workflow will build it for you
                                        the first time it runs (via <code class="inline">samtools faidx</code>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_gff</code></td>
                                        <td>A GFF annotation of the reference genome, used both to extract 4-fold sites for neutral model estimation and
                                        to exclude coding sequences from the final CNEEs.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_chromosome_groups</code></td>
                                        <td>The reference chromosomes/scaffolds to analyze, organized into named groups (see
                                        <a href="workflow.html#chromosome-ids">below</a>). Group names are organizational only and do not affect the 
                                        analysis. They simply become subdirectories of your output.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">sample_file</code></td>
                                        <td>A CSV sample sheet with, at minimum, a column called <code class="inline">accession</code> containing an
                                        NCBI assembly accession for each genome in the MAF which is used to look up GC content for model correction, or
                                        a column called <code class="inline">gc</code> with precomputed values can be supplied instead of accessions.
                                        Not needed if you set <code class="inline">use_gc_corrected_models: false</code>.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">output_dir</code></td>
                                        <td>Where all workflow outputs will be written. Created automatically if it doesn't already exist.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">tmp_dir</code></td>
                                        <td>A scratch directory for temporary files. Make sure it has sufficient space as whole-genome MAFs and their
                                        intermediate splits can be large.</td>
                                    </tr>
                                </table>
                            </div>

                            <a class="internal-link" id="chromosome-ids"></a>
                            <h2>2. Matching chromosome IDs</h2>

                            <p>
                                A common source of early errors is that the reference chromosome/scaffold IDs don't line up between the MAF, the
                                reference FASTA/index, and the GFF. The workflow expects the IDs listed in
                                <code class="inline">ref_chromosome_groups</code> to match those in <code class="inline">ref_fasta_index</code> and
                                <code class="inline">ref_gff</code> exactly, and it derives the expected MAF <code class="inline">src</code> label for
                                each chromosome from three settings:
                            </p>

                            <ul>
                                <li><code class="inline">maf_ref_id</code>: the reference species name as it appears in the MAF.</li>
                                <li><code class="inline">maf_ref_chr_joiner</code>: the character joining the reference ID and the chromosome name in
                                    the MAF (usually <code class="inline">"."</code>).</li>
                                <li><code class="inline">maf_chr_prefix</code>: an optional prefix on the chromosome name in the MAF that isn't present
                                    in the GFF/FASTA index.</li>
                            </ul>

                            <p>For example, if the MAF's <code class="inline">src</code> field looks like <code class="inline">Mus_musculus.CM001010.3</code>,
                            and the GFF/FASTA index also call that chromosome <code class="inline">CM001010.3</code>, you'd set:</p>

                            <pre class="long-cmd"><code>maf_ref_id: "Mus_musculus"
maf_chr_prefix: ""
maf_ref_chr_joiner: "."</code></pre>

                            <p>But if the MAF instead labels it <code class="inline">Homo_sapiens.chr1</code> while the GFF/FASTA index just call it
                            <code class="inline">1</code>, you'd set:</p>

                            <pre class="long-cmd"><code>maf_ref_id: "Homo_sapiens"
maf_chr_prefix: "chr"
maf_ref_chr_joiner: "."</code></pre>

                            <p>and list <code class="inline">"1"</code> (not <code class="inline">"chr1"</code>) under
                            <code class="inline">ref_chromosome_groups</code>.</p>

                            <a class="internal-link" id="config-file"></a>
                            <h2>3. Building a config file</h2>

                            <p>
                                Copy the template and start filling in the paths and chromosome groups for your project:
                            </p>

                            <center><pre class="cmd"><code>cp config-template.yaml my-config.yaml</code></pre></center>

                            <p>
                                Open <code class="inline">my-config.yaml</code> in an editor. The required inputs described above are all near the top
                                of the file, under a section marked <code class="inline">YOU MUST FILL THESE IN</code>. Everything below that has a
                                working default and generally doesn't need to change for a first run, but a few settings are worth knowing about:
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Config key</th>
                                        <th>Description</th>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">run_phylofit</code>, <!--<code class="inline">run_phylop</code>,-->
                                        <code class="inline">run_phastcons</code>, <code class="inline">build_cnees</code></td>
                                        <td>The primary on/off switches for each stage of the pipeline.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_output_format</code></td>
                                        <td>Format for the final, per-element CNEE alignments: <code class="inline">fasta</code>,
                                        <code class="inline">maf</code>, or <code class="inline">none</code> to skip extraction and keep only the
                                        CNEE coordinates.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">rho_mode</code>, <code class="inline">fixed_rho</code></td>
                                        <td>By default (<code class="inline">rho_mode: fixed</code>) phastCons uses a fixed conservation parameter
                                        (<code class="inline">fixed_rho: 0.3</code>) for every chunk. Set <code class="inline">rho_mode: estimate</code>
                                        to instead estimate rho per chunk and derive a chromosome-wide value from it.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">cnee_min_len_bp</code></td>
                                        <td>Minimum length (bp) for a conserved region to be kept as a CNEE after removing coding sequence.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">rule_resources</code></td>
                                        <td>
                                            Per-rule cluster resources (SLURM partition, memory, CPUs, time limit). Resources required depends on the number
                                            of species in the alignment and the size of the genomes. This is hard to predict. Many rules are fast and light, but some 
                                            (especially <code class="inline">run_phastcons</code>) can be slow and memory-intensive. 
                                            If you run out of memory or time on a rule, increase the resources for that rule in your config file and re-run the workflow.
                                            <b>You must provide a partition name applicable to your cluster</b>.
                                        </td>
                                    </tr>
                                </table>
                            </div>

                            <!--
                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="rec_banner">Tip - you don't need phyloP to get CNEEs</div>
                                    <div id="rec_text">
                                        <p>
                                            <code class="inline">run_phylop</code> controls a separate, independent site-level conservation analysis
                                            and isn't required to produce CNEEs with phastCons. If all you want out of this workflow is a set of CNEE
                                            alignments, you can set <code class="inline">run_phylop: false</code> and skip that stage entirely.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            -->

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

                            <pre class="long-cmd"><code>./phyloacc_workflows run \\
    --configfile my-config.yaml \\
    -j 20 \\
    -e slurm \\
    --dryrun</code></pre>

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
                            
                            <center><a class="main-btn" href="https://github.com/phyloacc/phyloacc-workflows/blob/main/phylofit-phastcons-rulgraph.png" target="_blank">Pipeline rulegraph &raquo;</a></center>


                            <a class="internal-link" id="execute"></a>
                            <h2>2. Executing the workflow</h2>

                            <p>
                                Once the dry run looks right, drop <code class="inline">--dryrun</code> to actually run it:
                            </p>

                            <pre class="long-cmd"><code>./phyloacc_workflows run \\
    --configfile my-config.yaml \\
    -j 20 \\
    -e slurm</code></pre>
    
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
                                output. Common early culprits are a chromosome/scaffold ID that doesn't match between the MAF, FASTA index, and GFF
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

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));
