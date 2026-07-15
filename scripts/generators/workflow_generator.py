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
                        <ul>
                            <li><a href="workflow.html#hard-masking">The reference genome must be hard masked</a></li>
                        </ul>
                        <li><a href="workflow.html#config-file">Pipeline config file</a></li>
                        <ul>
                            <li><a href="workflow.html#config-template">Config template</a></li>
                            <li><a href="workflow.html#chromosome-ids">Matching chromosome IDs</a></li>
                            <li><a href="workflow.html#gc-correction">Optional GC content correction</a></li>
                            <li><a href="workflow.html#rho-estimation">Estimating rho, or using a global value</a></li>
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
                                        <td><b>Reference genome assembly</b></td>
                                        <td>FASTA</td>
                                        <td><code class="inline">ref_fasta</code></td>
                                        <td>The MAF file uses one species' genome as the reference for coordinates. This same assembly is used to split
                                        the alignment into chunks based on runs of Ns, so the conserved element prediction can be done on smaller pieces
                                        of the alignment for scalability. <b>IMPORTANT: The reference assembly must contain Ns</b>. See
                                        <a href="workflow.html#hard-masking">hard-masking the reference genome</a> below.</td>
                                    </tr>
                                    <tr>
                                        <td><b>Reference genome annotation</b></td>
                                        <td>GFF</td>
                                        <td><code class="inline">ref_gff</code></td>
                                        <td>Used both to extract 4-fold degenerate sites for the neutral model and to exclude coding sequence from the
                                        final CNEEs.</td>
                                    </tr>
                                    <tr>
                                        <td><b>Species tree</b></td>
                                        <td>Newick</td>
                                        <td><code class="inline">tree_file</code></td>
                                        <td>The topology is used when estimating the neutral model. If you ran the 
                                        <a href="walkthrough.html#wga">Cactus snakemake</a> pipeline to generate your whole-genome alignment, you should
                                        already have this. If you have a .hal file from a previous alignment, you can extract the tree with the
                                        <a href="https://github.com/ComparativeGenomicsToolkit/hal" target="_blank">HAL tools</a> command
                                        <code class="inline">halStats <hal file> --tree</code>. Otherwise, you will have to infer a tree.</td>
                                    </tr>
                                    <tr>
                                        <td><b>Sample sheet</b></td>
                                        <td>CSV</td>
                                        <td><code class="inline">sample_file</code></td>
                                        <td><b>Required only if correcting neutral models for GC content (<code class="inline">use_gc_corrected_models: true</code>)</b>. 
                                        With, at minimum, either a column called <code class="inline">accession</code> containing an NCBI assembly
                                        accession for each genome in the MAF, used to look up GC content for neutral model correction <b>OR</b> a column called
                                        <code class="inline">gc</code> with precomputed values can be supplied instead of accessions. </td>
                                    </tr>
                                </table>
                            </div>

                            <p>
                                The paths to these files and other pipeline options are specified in a single YAML config file, described in the pipeline configuration section.
                            </p>                            

                            <a class="internal-link" id="hard-masking"></a>
                            <h3>The reference genome must be hard masked</h3>

                            <p>
                                For scalability, the pipeline splits the alignment into chunks wherever the reference assembly has a run of Ns (see
                                <a href="workflow.html#filtering">Filtering parameters</a>), and the resulting chunks are scored for conservation.
                                If your assembly is highly contiguous and mostly free of Ns, there will be few natural places to split the alignment,
                                chunks will be large, and repetitive sequence will be included in the <code class="inline">phastCons</code> scan. Practically,
                                the pipeline will take prohibitively long to run.
                            </p>

                            <p>
                                If your assembly doesn't contain Ns, we recommend hard-masking it with
                                <a href="https://www.repeatmasker.org/" target="_blank">RepeatMasker</a>. Hard-masking replaces repetitive sequence 
                                with <code class="inline">N</code>, which both gives the pipeline's Ns-based splitting real breakpoints
                                to work with and excludes those repeat regions from conservation scoring entirely.
                            </p>

                            <center><pre class="cmd"><code>RepeatMasker -pa [threads] -species "[species or clade name]" -dir [output directory] [genome.fasta]</code></pre></center>

                            <p>
                                This produces <code class="inline">[genome.fasta].masked</code> alongside a few report files. Specify this masked assembly as
                                <code class="inline">ref_fasta</code> in the pipeline config and make sure it's the exact same assembly/coordinates already
                                used to build your MAF since masking a different assembly version will shift coordinates and break the Ns-based
                                chunking.
                            </p>

                            <h4>Checking runs of Ns</h4>
                                <p>
                                    You can also check whether your assembly has meaningful runs of Ns, both before and after masking, with a few quick bash commands.
                                </p>

                                <p>
                                    First, extract the runs of Ns and write their lengths to a file:
                                </p>

                                <center><pre class="cmd"><code>awk '/^>/{{if(seq)print seq; seq=""; next}}{{seq=seq $0}}END{{if(seq)print seq}}' [genome.fasta] | grep -oE 'N+' | awk '{{print length($0)}}' > n-run-lengths.txt</code></pre></center>

                                <p>
                                    You can check how many run there are in total:
                                </p>

                                <center><pre class="cmd"><code>wc -l < n-run-lengths.txt</code></pre></center>

                                <p>
                                    Display a distribution of run lengths:
                                </p>

                                <center><pre class="cmd"><code>echo "# digits in length of run: 1 = 1-9bp, 2 = 10-99bp, 3 = 100-999bp, etc."; printf "%-8s %s\\n" digits count; awk '{{print length($1)}}' n-run-lengths.txt | sort -n | uniq -c | awk '{{printf "%-8s %s\\n", $2, $1}}'</code></pre></center>
                                
                                <p>
                                    And also explicitly display how many are at least 100bp, the pipeline's default
                                    <code class="inline">min_Ns_to_split_by</code>, and so the actual split points it would find:
                                </p>

                                <center><pre class="cmd"><code>awk '$1 >= 100' n-run-lengths.txt | wc -l</code></pre></center>

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
                                We provide a fully commented template, 
                                <a href="https://github.com/phyloacc/phyloacc-workflows/blob/main/config-template.yaml" target="_blank">config-template.yaml</a>. 
                                Copy it from the link above or the internal path below from your local copy of the repository and start
                                filling in the paths and chromosome groups for your project:
                            </p>

                            <center><pre class="cmd"><code>cp config-template.yaml my-config.yaml</code></pre></center>

                            <p>
                                Open <code class="inline">my-config.yaml</code> in an editor. The required inputs from above are all near the top of
                                the file, under a section marked <code class="inline">YOU MUST FILL THESE IN</code>, and map onto the following config
                                keys, along with a few other required settings:
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
                                        <td><code class="inline">ref_fasta</code></td>
                                        <td>Path to the reference genome FASTA file described above.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_fasta_index</code></td>
                                        <td>Path to the reference FASTA's <code class="inline">.fai</code> index described above. This must literally
                                        be <code class="inline">ref_fasta + ".fai"</code>. If blank, the index will be generated with 
                                        <code class="inline">samtools faidx</code></td>
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
                                        <td><code class="inline">sample_file</code></td>
                                        <td>Path to the sample sheet CSV described above.</td>
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

                            <h4>Relevant config keys: <code class="inline">ref_chromosome_groups</code>, <code class="inline">maf_ref_id</code>
                                <code class="inline">maf_ref_chr_joiner</code>, <code class="inline">maf_chr_prefix</code></h4>

                            <p>
                                A common source of early errors is that the reference chromosome/scaffold IDs don't line up between the MAF, the
                                reference FASTA/GFF. The workflow expects the IDs listed in
                                <code class="inline">ref_chromosome_groups</code> to match those in <code class="inline">ref_fasta</code> and
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

                            <p>For example, if the MAF's <code class="inline">src</code> field looks like <code class="inline">Homo_sapiens.chr1</code>,
                            and the GFF/FASTA index also call that chromosome <code class="inline">chr1</code>, you'd set:</p>

                            <pre class="long-cmd"><code>maf_ref_id: "Homo_sapiens"
maf_chr_prefix: ""
maf_ref_chr_joiner: "."</code></pre>

                            <p>But if the MAF instead labels it <code class="inline">Homo_sapiens.chr1</code> while the GFF/FASTA index just call it
                            <code class="inline">1</code>, you'd set:</p>

                            <pre class="long-cmd"><code>maf_ref_id: "Homo_sapiens"
maf_chr_prefix: "chr"
maf_ref_chr_joiner: "."</code></pre>

                            <p>and list <code class="inline">"1"</code> (not <code class="inline">"chr1"</code>) under
                            <code class="inline">ref_chromosome_groups</code>.</p>

                            <a class="internal-link" id="gc-correction"></a>
                            <h3>Optional GC content correction</h3>

                            <h4>Relevant config keys: <code class="inline">use_gc_corrected_models</code>, <code class="inline">sample_file</code></h4>

                            <p>
                                Because the neutral models are estimated from 4-fold degenerate sites and subsequently applied to the whole genome, if
                                those sites have different GC content the models may be inaccurate. The models can be corrected by adjusting for genome-wide
                                GC content.
                            </p>

                            <p>
                                Set <code class="inline">use_gc_corrected_models: true</code> and provide a <code class="inline">sample_file</code> to have 
                                the pipeline correct each chromosome's neutral model for the GC content of the genomes in the alignment.
                            </p>
                            
                            <p>
                                If accessions are provided, the pipeline uses <code class="inline">ncbi-datasets-cli</code> to look up the GC content. If GC
                                values exist in the <code class="inline">gc</code> column of the <code class="inline">sample_file</code>, those values are used instead.
                                Both columns can exist and different samples can use different methods to provide GC content.
                            </p>

                            
                            <p>
                                With the GC content read, the pipeline uses PHAST's <code class="inline">mod_freqs</code> script to adjust neutral models for each chromosome.
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

                            <a class="internal-link" id="rho-estimation"></a>
                            <h3>Estimating rho, or using a global value</h3>

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

                            <a class="internal-link" id="filtering"></a>
                            <h3>Filtering parameters</h3>

                            <h4>Relevant config keys: <code class="inline">filter_threshold_4d</code>, <code class="inline">min_Ns_to_split_by</code>,
                                <code class="inline">min_keep_region_len</code>, <code class="inline">max_gap_pct</code>,
                                <code class="inline">cnee_ces_merge_gap_bp</code>, <code class="inline">cnee_min_len_bp</code></h4>

                            <p>
                                Several thresholds control how aggressively data is filtered at different stages of the pipeline:
                            </p>

                            <ul>
                                <li>
                                    <b>4-fold degenerate sites</b> (<code class="inline">filter_threshold_4d</code>, default
                                    <code class="inline">0.5</code>): sites used to fit the neutral model are dropped if more than this fraction of
                                    sequences are missing at that site.
                                </li>
                                <li>
                                    <b>Alignment chunk splitting</b> (<code class="inline">min_Ns_to_split_by</code>, default
                                    <code class="inline">100</code>; <code class="inline">min_keep_region_len</code>, default
                                    <code class="inline">6</code>): the alignment is split wherever the reference has a run of at least
                                    <code class="inline">min_Ns_to_split_by</code> Ns, and any resulting chunk shorter than
                                    <code class="inline">min_keep_region_len</code> bp is discarded before scoring.
                                </li>
                                <li>
                                    <b>Chunk quality</b> (<code class="inline">max_gap_pct</code>, default <code class="inline">0.9</code>): after
                                    splitting, a chunk is dropped entirely if more than this fraction of its non-reference alignment columns are gaps
                                    &mdash; a proxy for chunks with too little real alignment to score meaningfully.
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
                                Values in the template are based on a benchmark of a 15 species alignment of mammals. The config notes which rules should scale with
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
                                        <td><code class="inline">ref_fasta</code></td>
                                        <td><b>Required</b></td>
                                        <td>Path to the reference genome FASTA file.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">ref_fasta_index</code></td>
                                        <td>Auto-generated if blank</td>
                                        <td>Path to the reference FASTA's <code class="inline">.fai</code> index.</td>
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
                                        <td><code class="inline">accession_header</code></td>
                                        <td><code class="inline">accession</code></td>
                                        <td>Column name in <code class="inline">sample_file</code> holding NCBI assembly accessions.</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">maf_chr_prefix</code></td>
                                        <td><code class="inline">""</code></td>
                                        <td>Prefix on MAF chromosome IDs not present in the GFF/FASTA index (see <a href="workflow.html#chromosome-ids">above</a>).</td>
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
                                        <td><b>Required</b> if <code class="inline">use_gc_corrected_models: true</code></td>
                                        <td>CSV sample sheet used for GC correction (see <a href="workflow.html#gc-correction">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">min_Ns_to_split_by</code></td>
                                        <td><code class="inline">100</code></td>
                                        <td>Minimum run of Ns used as a split point (see <a href="workflow.html#filtering">above</a>).</td>
                                    </tr>
                                    <tr>
                                        <td><code class="inline">min_keep_region_len</code></td>
                                        <td><code class="inline">6</code></td>
                                        <td>Minimum chunk length (bp) to keep (see <a href="workflow.html#filtering">above</a>).</td>
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
                            
                            <center><a class="main-btn" href="https://github.com/phyloacc/phyloacc-workflows/blob/main/phylofit-phastcons-rulgraph.png" target="_blank">Pipeline rulegraph &raquo;</a></center>


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

with open(outfilename, "w", encoding="utf-8") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));
