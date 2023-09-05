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

 <a class="internal-link" name="install"></a>
    <div class="row" id="body-row">
        <div class="col-4-24" id="side-nav-cont">
            <div id="side-nav">
                <span id="side-header">Page contents</span>
                <ul>
                    <li><a href="readme.html#install">Installation</a></li>
                    <li><a href="readme.html#inputs">Inputs</a></li>
                    <li><a href="readme.html#usage">Usage</a></li>
                    <ol>
                        <li><a href="readme.html#st">Species tree model</a></li>
                        <li><a href="readme.html#gt">Gene tree model</a></li>
                        <li><a href="readme.html#adaptive">Adaptive model</a></li>
                        <li><a href="readme.html#snakemake">Executing snakemake</a></li>
                        <li><a href="readme.html#gather">Gather outputs</a></li>
                    </ol>
                    <li><a href="readme.html#output">Output</a></li>
                    <ol>
                        <li><a href="readme.html#elem_lik">elem_lik.txt</a></li>
                        <!-- <li><a href="readme.html#id-key">id_key.txt</a></li> -->
                        <li><a href="readme.html#elem_z">elem_z.txt</a></li>
                        <li><a href="readme.html#rate_postZ">rate_postZ_M*.txt</a></li>
                    </ol>
                    <li><a href="readme.html#options">Options</a></li>
                    <ol>
                        <li><a href="readme.html#io">Input/output</a></li>
                        <li><a href="readme.html#mcmc">MCMC</a></li>
                        <li><a href="readme.html#scf">sCF</a></li>
                        <li><a href="readme.html#batch">Batching</a></li>
                        <li><a href="readme.html#cluster">Cluster</a></li>
                        <li><a href="readme.html#phyloacc">PhyloAcc</a></li>
                        <li><a href="readme.html#misc">Miscellaneous</a></li>
                    </ol>
                </ul>
            </div>
        </div>

        <div class="col-20-24" id="main-content-col-page">

            <div class="row" id="top-row-cont">
                <div class="col-24-24" id="top-row"></div>
            </div>

            <div class="header">
                PhyloAcc README
            </div>

            <center>
                <h3>This page contains all info about the PhyloAcc program including its inputs, options, and outputs.</h3>
            </center>
            

            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Installation</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                With Anaconda already setup, Phyloacc can be installed with the command <code class="inline">conda install phyloacc</code>.
                                For more detailed installation instructions, see the <a href="">install page</a>.
                            </p>

                            <p>
                                Note that PhyloAcc is currently only compatible on Linux and OSX operating systems.
                            </p>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>


            <a class="internal-link" name="inputs"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Inputs</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                You will need the following data to perform an analysis with PhyloAcc
                            </p>

                            <ol>
                                <li>
                                    A set of <b>alignments</b> for a set of species from the regions you wish to estimate substitution rates for (e.g. CNEEs).
                                </li>

                                <li>
                                    A phylogenetic tree in Newick format from the same set of species with branch lengths estimated in terms of relative
                                    number of substitutions corresponding to neutral/background substitution rates.
                                </li>

                                <li>
                                    A transition rate matrix for bases in the neutral/background model.
                                </li>

                                <p>
                                    (2) and (3) can be obtained running <a href="http://compgen.cshl.edu/phast/phyloFit-tutorial.php" target="_blank">phyloFit</a> on alignments
                                    of likely neutrally evolving sites (e.g. 4-fold degenerate sites in genes) and will be given in a single .mod file output from that program.
                                </p>

                                <li>
                                    For running the gene tree model, a phylogenetic tree with the same topology as the one provided in (2), but with branch lengths in 
                                    coalescent units. This can be obtained from species tree inference methods like
                                    <a href="http://faculty.franklin.uga.edu/lliu/mp-est" target="_blank">MP-EST</a> or 
                                    <a href="https://github.com/smirarab/ASTRAL" target="_blank">ASTRAL</a>. 
                                    PhyloAcc has the capability to to estimate this directly from the input alignments with the <code class="inline">--theta</code> option,  
                                    by building locus trees using
                                    <a href="http://www.iqtree.org/" target="_blank">IQ-TREE</a> 
                                    and then using those as input to 
                                    <a href="https://github.com/smirarab/ASTRAL" target="_blank">ASTRAL</a>. This will be done for at most the 5000 longest alignments that are
                                    longer than 100bp and have at least 20% informative sites. These requirements are to ensure there is phylogenetic signal to infer this tree
                                    given that some inputs to PhyloAcc may be conserved and have few variable sites.
                                    However, you must be sure the alignments you are estimating rates for with PhyloAcc are also suitable for tree inference if you use this
                                    option. Also note that using the <code class="inline">--theta</code> option may significantly add to the runtime of the workflow.
                                </li>
                            </ol>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>



            <a class="internal-link" name="usage"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Usage</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                PhyloAcc version 2 now facilitates parallelization on computing clusters by using Python to batch loci and Snakemake
                                to submit those batches to the cluster. This results in a three-step process to run PhyloAcc:
                            </p>

                            <ol>
                                <li>
                                    Process and batch input alignments with the PhyloAcc interface (<code class="inline">phyloacc.py</code>).
                                </li>
                                <li>
                                    Submit the batches as jobs on the SLURM cluster (<code class="inline">snakemake [generated snakefile]</code>).
                                </li>
                                <li>
                                    Gather outputs from batches into single files (<code class="inline">phyloacc-post.py</code>).
                                </li>
                            </ol>

                            <p>
                                Below we outline several ways to batch loci ("Setting up batches") as well as examples of how to submit the snakefile
                                and gather the outputs.
                            </p>

<!--
                            <div class="section-sub-header">Setting up batches of loci for the species tree model with a concatenated alignment:</div>
                            <pre class="long-cmd"><code>phyloacc.py \\
    -a [nucleotide alignment file in FASTA format] \\
    -b [bed file with coordinates for loci in the alignment file] \\
    -m [mod file from phyloFit with input tree and neutral rate matrix] \\
    -o [desired output directory] \\
    -t "[semi-colon separated list of target branches in the species tree]" \\
    -j [number of jobs/batches to split the input alignments into]" \\
    -p [processes to use per job/batch of alignments] \\
    -batch [number of alignments per job/batch] \\
    -part "[comma separated list of SLURM partitions to submit batches to as jobs]"</code></pre>
-->
                            <a class="internal-link" name="st"></a>
                            <div class="section-sub-header">Setting up batches of loci for the species tree model with a directory of alignments:</div>
                            <pre class="long-cmd"><code>phyloacc.py \\
    -d [directory containing multiple FASTA formatted nucleotide alignments] \\
    -m [mod file from phyloFit with input tree and neutral rate matrix] \\
    -o [desired output directory] \\
    -t "[semi-colon separated list of target branches in the species tree]" \\
    -j [number of jobs/batches to split the input alignments into] \\
    -p [processes to use per job/batch of alignments] \\
    -batch [number of alignments per job/batch] \\
    -part "[comma separated list of SLURM partitions to submit batches to as jobs]"</code></pre>

                            <a class="internal-link" name="gt"></a>
                            <div class="section-sub-header">Setting up batches of loci for the gene tree model with a directory of alignments and a provided tree with branch lengths in coalescent units:</div>
                            <pre class="long-cmd"><code>phyloacc.py \\
    -d [directory containing multiple FASTA formatted nucleotide alignments] \\
    -m [mod file from phyloFit with input tree and neutral rate matrix] \\
    -r gt \\
    -l [file with Newick formatted species tree with branch lengths in coalescent units] \\
    -o [desired output directory] \\
    -t "[semi-colon separated list of target branches in the species tree]" \\
    -j [number of jobs/batches to split the input alignments into] \\
    -p [processes to use per job/batch of alignments] \\
    -batch [number of alignments per job/batch] \\
    -part "[comma separated list of SLURM partitions to submit batches to as jobs]"</code></pre>

<!--
                            <div class="section-sub-header">Setting up batches of loci for the gene tree model with a directory of alignments and --theta to estimate a species tree with branch lengths in coalescent units:</div>
                            <pre class="long-cmd"><code>phyloacc.py \\
    -d [directory containing multiple FASTA formatted nucleotide alignments] \\
    -m [mod file from phyloFit with input tree and neutral rate matrix] \\
    -r gt \\
    --theta \\
    -o [desired output directory] \\
    -t "[semi-colon separated list of target branches in the species tree]" \\
    -j [number of jobs/batches to split the input alignments into] \\
    -p [processes to use per job/batch of alignments] \\
    -batch [number of alignments per job/batch] \\
    -part "[comma separated list of SLURM partitions to submit batches to as jobs]"</code></pre>
-->

                            <a class="internal-link" name="adaptive"></a>
                            <div class="section-sub-header">Setting up batches of loci with the model determined by sCF cutoffs, with a directory of alignments, and with a provided tree with branch lengths in coalescent units:</div>
                            <pre class="long-cmd"><code>phyloacc.py \\
    -d [directory containing multiple FASTA formatted nucleotide alignments] \\
    -m [mod file from phyloFit with input tree and neutral rate matrix] \\
    -r adaptive \\
    -l [file with Newick formatted species tree with branch lengths in coalescent units] \\
    -o [desired output directory] \\
    -t "[semi-colon separated list of target branches in the species tree]" \\
    -j [number of jobs/batches to split the input alignments into] \\
    -p [processes to use per job/batch of alignments] \\
    -batch [number of alignments per job/batch] \\
    -part "[comma separated list of SLURM partitions to submit batches to as jobs]"</code></pre>

                            <a class="internal-link" name="snakemake"></a>
                            <div class="section-sub-header">Executing a generated snakefile to submit jobs to the cluster:</div>
<pre class="long-cmd"><code>snakemake -p -s \\
    [path to snakefile.smk] \\
    [path to config file] \\
    [path to cluster profile] \\
    --dryrun</code></pre>

                            <p>
                                Note that all files for the snakemake command are automatically generated when running 
                                <code class="inline">phyloacc.py</code> and the exact command to run will be printed to the screen and
                                written to the log and summary files.
                            </p>

                            <div id="msg_cont">
                                <div id="msg">
                                    <div id="rec_banner">Tip - Always check snakefiles with <code class="inline">--dryrun</code> before executing</div>
                                    <div id="rec_text">
                                        <p>
                                            Always try to run the <code class="inline">snakemake</code> command with the <code class="inline">--dryrun</code>
                                            option to catch any errors before the jobs are submitted. After the dry run has completed successfully, remove
                                            <code class="inline">--dryrun</code> from the command to execute the workflow and start job submission to the
                                            cluster.
                                        </p>
                                        <p></p>
                                    </div>
                                </div>
                            </div>
                            </br>

                            <a class="internal-link" name="gather"></a>
                            <div class="section-sub-header">Gather outputs after all snakemake jobs are completed:</div>
<pre class="long-cmd"><code>phyloacc_post.py \\
    -i [path output directory specified when running phyloacc.py]</code></pre>

                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

            <a class="internal-link" name="output"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Output</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">
                            <p>
                                After running <code class="inline">phyloacc_post.py</code>, outputs from each batch will be combined and a summary
                                HTML file will be created with some preliminary summaries of results. This file will be found in the main output
                                directory from the <code class="inline">phyloacc.py</code> command (specified with the <code class="inline">-o</code>
                                option).
                            </p>

                            <p>
                                Raw output files are also available in the output directory specified with <code class="inline">phyloacc_post.py</code>,
                                with the default directory name being <code class="inline">results/</code>.
                            </p>

                            <p>The raw files are tab delimited and described below.</p>

                            <a class="internal-link" name="elem_lik"></a>
                            <div class="section-sub-header">elem_lik.txt</div>

                            <p>
                                Marginal log-likelihood for all models (integrating out parameters and latent states), Bayes factors, rates, and states for each locus.
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Column header</th>
                                        <th>Column description</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            phyloacc.id
                                        </td>
                                        <td>
                                            The number assigned to this locus by PhyloAcc, with the format [batch number]-[locus number]
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            original.id
                                        </td>
                                        <td>
                                            The ID of the locus provided in the input (bed file or fasta file)
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            best.fit.model
                                        </td>
                                        <td>
                                            The model (M0, M1, or M2) that best fits the data for this locus given the specified Bayes Factor cutoffs
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            marginal.likelihood.m0
                                        </td>
                                        <td>
                                            Marginal log-likelihood under the null model (M0)
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            marginal.likelihood.m1
                                        </td>
                                        <td>
                                            Marginal log-likelihood under target model (M1)
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            marginal.likelihood.m2
                                        </td>
                                        <td>
                                            Marginal log-likelihood under the unrestricted full model (M2)
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            logbf1
                                        </td>
                                        <td>
                                            log Bayes factor between null (M0) and target (M1) models
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            logbf2
                                        </td>
                                        <td>
                                            log Bayes factor between target (M1) and full (M2) models
                                        </td>
                                    </tr>   
                                    <tr>
                                        <td>
                                            logbf3
                                        </td>
                                        <td>
                                            log Bayes factor between full (M2) and null (M0) models
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            conserved.rate.m0
                                        </td>
                                        <td>
                                            The posterior median of the conserved substitution rate under M0
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            accel.rate.m0
                                        </td>
                                        <td>
                                            The posterior median of the accelerated substitution rate under M0
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            conserved.rate.m1
                                        </td>
                                        <td>
                                            The posterior median of the conserved substitution rate under M1
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            accel.rate.m1
                                        </td>
                                        <td>
                                            The posterior median of the accelerated substitution rate under M1
                                        </td>
                                    </tr>                                                                                                            
                                    <tr>
                                        <td>
                                            conserved.rate.m2
                                        </td>
                                        <td>
                                            The posterior median of the conserved substitution rate under M2
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            accel.rate.m2
                                        </td>
                                        <td>
                                            The posterior median of the accelerated substitution rate under M2
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            num.accel.m1
                                        </td>
                                        <td>
                                            The number of lineages inferred to be accelerated under M1
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            num.accel.m2
                                        </td>
                                        <td>
                                            The number of lineages inferred to be accelerated under M2
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            conserved.lineages.m1
                                        </td>
                                        <td>
                                            A comma separated list of the conserved lineages under M1
                                        </td>
                                    </tr>                                                                                                                                                                                    
                                    <tr>
                                        <td>
                                            accel.lineages.m1
                                        </td>
                                        <td>
                                            A comma separated list of the accelerated lineages under M1
                                        </td>
                                    </tr> 
                                    <tr>
                                        <td>
                                            conserved.lineages.m2
                                        </td>
                                        <td>
                                            A comma separated list of the conserved lineages under M2
                                        </td>
                                    </tr> 
                                    <tr>
                                        <td>
                                            accel.lineages.m1
                                        </td>
                                        <td>
                                            A comma separated list of the accelerated lineages under M1
                                        </td>
                                    </tr> 

                                    <!--                                                                                                                                                                                                                                          
                                    <tr>
                                        <td>
                                            loglik_Max_M0, loglik_Max_M1, loglik_Max_M2 
                                        </td>
                                        <td>
                                            Maximum joint likelihood of \(Y\) (observed sequences) and 
                                            \(r\) (substitution rates) 
                                            given \(Z\) (latent states) under 
                                            null (<span class="math">\(M_0\)</span>),
                                            accelerated (<span class="math">\(M_1\)</span>), and
                                            full (<span class="math">\(M_2\)</span>) models: e.g. \( \max_{{r, Z}} P(Y, r|Z)\)
                                        </td>
                                    </tr>
                                    -->    
                                </table>
                            </div>


                            <!--
                            <a class="internal-link" name="id-key"></a>
                            <div class="section-sub-header">id-key.txt</div>

                            <p>
                                Links PhyloAcc job IDs back to original locus IDs if provided
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Column number</th>
                                        <th>Column description</th>
                                    </tr>
                                    <tr>
                                        <td>
                                            1
                                        </td>
                                        <td>
                                            [batch number]-[locus number]
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            2
                                        </td>
                                        <td>
                                            Original locus ID from 4th column of input bed file or input file name
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            3
                                        </td>
                                        <td>
                                            The most likely model for that locus
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            4
                                        </td>
                                        <td>
                                            The likelihood of the most likely model for that locus
                                        </td>
                                    </tr>    
                                </table>
                            </div>
                            -->

                            <a class="internal-link" name="elem_z"></a>
                            <div class="section-sub-header">[prefix]_M*_elem_Z.txt</div>

                            <p>
                                Maximum log-likelihood configurations of latent state Z under null, accelerated and full model, 
                                with Z=-1 (if the element is 'missing' in the branches of outgroup species), 
                                0 (background), 1 (conserved), 2 (accelerated).
                            </p>

                            <p>
                                Each row corresponds to an input element and each column a branch in the tree. If an element is 
                                filtered because of too many alignment gaps all the columns will be zero.
                            </p>


                            <a class="internal-link" name="rate_postZ"></a>
                            <div class="section-sub-header">[prefix]_rate_postZ_M*.txt</div>

                            <p>
                                Posterior median of conserved rate, accelerated rate, probability of gain and loss conservation 
                                (and \(\\beta = P(Z=1\\rightarrow Z=2)\)), and posterior probability of being in each latent state on each branch for each element.
                            </p>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Column header</th>
                                        <th>Column description</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            Locus ID 
                                        </td>
                                        <td>
                                            [batch number]-[locus number]
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            n_rate
                                        </td>
                                        <td>
                                            Posterior median of accelerated substitution rate
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            c_rate
                                        </td>
                                        <td>
                                            Posterior median of conserved substitution rate
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            g_rate
                                        </td>
                                        <td>
                                            Posterior median of \( \\alpha \)
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            l_rate
                                        </td>
                                        <td>
                                            Posterior median of \( \\beta \)
                                        </td>
                                    </tr>
                                    <tr>
                                        <td>
                                            l2_rate
                                        </td>
                                        <td>
                                            Posterior median of \( \\beta_2 = P(Z = 0 \\rightarrow Z = 2) \), which is 0 in current implementation
                                        </td>
                                    </tr>                                                                          
                                </table>
                            </div>

                            <p>
                                From the 7th column and on, there are four columns for each branch in the tree: *_0 indicates whether it's "missing"; 
                                *_1, *_2 and *_3 are the posterior probability in the background, conserved and accelerated state respectively. 
                                The algorithm will prune "missing" branches within outgroup and set the latent states of them to -1 so that the three 
                                posterior probabilities are all zero. Column names indicate the branch and the order of the branch is the same as that in prefix_elem_Z.txt.
                            </p>


                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>


            <a class="internal-link" name="options"></a>
            <div class="row" id="section-header-cont">
                <div class="col-24-24" id="section-header-row">
                    <div id="section-header">Options</div>
                </div>
            </div>

            <div class="row" id="section-cont">
                <div class="col-24-24" id="section-col">
                    <div class="row" id="section-row">
                        <div class="col-2-24" id="inner-margin"></div>
                        <div class="col-20-24" id="section-content">

                            <a class="internal-link" name="io"></a>
                            <div class="section-sub-header">Input/Output options</div>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Option</th>
                                        <th>Description</th>
                                        <th>Default value</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-a [FASTA FILE]</code>
                                        </td>
                                        <td>
                                            An alignment file with all loci concatenated. <code class="inline">-b</code> must also be specified. 
                                            Expected as FASTA format for now.
                                        </td>
                                        <td>
                                             One of <code class="inline">-a</code>/<code class="inline">-b</code> or <code class="inline">-d</code> is <b>REQUIRED</b>.
                                        </td>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-b [BED FILE]</code>
                                        </td>
                                        <td>
                                            A bed file with coordinates for the loci in the concatenated alignment file. 
                                            <code class="inline">-a</code> must also be specified.
                                        </td>
                                        <td>
                                             One of <code class="inline">-a</code>/<code class="inline">-b</code> or <code class="inline">-d</code> is <b>REQUIRED</b>.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-i [TEXT FILE]</code>
                                        </td>
                                        <td>
                                            A text file with locus names, one per line, corresponding to regions in the input bed file. If provided,
                                            PhyloAcc will only be run on these loci. 
                                        </td>
                                        <td>
                                            Optional. <code class="inline">-a</code> and <code class="inline">-b</code> must also be specified.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-d [DIRECTORY]</code>
                                        </td>
                                        <td>
                                            A directory containing individual alignment files for each locus. 
                                            Expected as FASTA format for now.
                                        </td>
                                        <td>
                                             One of <code class="inline">-a</code>/<code class="inline">-b</code> or <code class="inline">-d</code> is <b>REQUIRED</b>.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-m [MOD FILE]</code>
                                        </td>
                                        <td>
                                            A file with a background transition rate matrix and 
                                            phylogenetic tree with branch lengths as output from phyloFit.
                                        </td>
                                        <td>
                                            <b>REQUIRED</b>.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-o [DIRECTORY]</code>
                                        </td>
                                        <td>
                                            Desired output directory. This will be created for you if it doesn't exist.
                                        </td>
                                        <td>
                                             phyloacc-[date]-[time]
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-t "[STRING]"</code>
                                        </td>
                                        <td>
                                            Tip labels in the input tree to be used as target species. 
                                            Enter multiple labels separated by semi-colons (;).
                                        </td>
                                        <td>
                                            <b>REQUIRED</b>.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-c "[STRING]"</code>
                                        </td>
                                        <td>
                                            Tip labels in the input tree to be used as conserved species. 
                                            Enter multiple labels separated by semi-colons (;). 
                                        </td>
                                        <td>
                                            Optional. Any species not specified in <code class="inline">-t</code> or <code class="inline">-g</code> will be inferred as conserved.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-g "[STRING]"</code>
                                        </td>
                                        <td>
                                            Tip labels in the input tree to be used as outgroup species. 
                                            Enter multiple labels separated by semi-colons (;).
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-l [NEWICK FILE]</code>
                                        </td>
                                        <td>
                                            A file containing a rooted, Newick formatted tree with the same topology as the species tree in the mod file (<code class="inline">-m</code>), 
                                            but with branch lengths in coalescent units.
                                        </td>
                                        <td>
                                            When the gene tree model is used, one of <code class="inline">-l</code> or <code class="inline">--theta</code> must be set.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">--theta</code>
                                        </td>
                                        <td>
                                            Set this to add gene tree estimation with IQ-tree and species estimation with ASTRAL for estimation 
                                            of the theta prior. Note that a species tree with branch lengths in units of substitutions per site 
                                            is still required with <code class="inline">-m</code>. Also note that this may add substantial runtime to the pipeline.
                                        </td>
                                        <td>
                                            When the gene tree model is used, one of <code class="inline">-l</code> or <code class="inline">--theta</code> must be set.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-r [STRING]</code>
                                        </td>
                                        <td>
                                            Determines which version of PhyloAcc will be used. 
                                            gt: use the gene tree model for all loci, 
                                            st: use the species tree model for all loci, 
                                            adaptive: use the gene tree model on loci with many branches with low sCF and species tree model 
                                            on all other loci.
                                        </td>
                                        <td>
                                            st
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">-n [INT]</code>
                                        </td>
                                        <td>
                                            The number of processes that this script should use.
                                        </td>
                                        <td>
                                            1
                                        </td>                                        
                                    </tr>

                                </table>
                            </div>

                            <a class="internal-link" name="mcmc"></a>
                            <div class="section-sub-header">MCMC options</div>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Option</th>
                                        <th>Description</th>
                                        <th>Default value</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-burnin [INT]</code>
                                        </td>
                                        <td>
                                            The number of steps to be discarded in the Markov chain as burnin.
                                        </td>
                                        <td>
                                            500
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-mcmc [INT]</code>
                                        </td>
                                        <td>
                                            The total number of steps in the Markov chain.
                                        </td>
                                        <td>
                                            1000
                                        </td>                                        
                                    </tr>

                                </table>
                            </div>

                            <a class="internal-link" name="scf"></a>
                            <div class="section-sub-header">sCF options</div>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Option</th>
                                        <th>Description</th>
                                        <th>Default value</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-scf [FLOAT]</code>
                                        </td>
                                        <td>
                                            The value of sCF to consider as low for any given branch or locus. Must be between 0 and 1.
                                        </td>
                                        <td>
                                            0.5
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-s [FLOAT]</code>
                                        </td>
                                        <td>
                                            A value between 0 and 1. If provided, this proportion of branches must have sCF below <code class="inline">-scf</code> 
                                            to be considered for the gene tree model. Otherwise, branch sCF values will be averaged for each locus.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>

                                </table>
                            </div>

                            <a class="internal-link" name="batch"></a>
                            <div class="section-sub-header">Batching options</div>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Option</th>
                                        <th>Description</th>
                                        <th>Default value</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-p [INT]</code>
                                        </td>
                                        <td>
                                            The number of processes to use for each batch of PhyloAcc.
                                        </td>
                                        <td>
                                            1
                                        </td>
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">-j [INT]</code>
                                        </td>
                                        <td>
                                            The number of jobs (batches) to run in parallel.
                                        </td>
                                        <td>
                                            1
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">-batch [INT]</code>
                                        </td>
                                        <td>
                                            The number of loci to run per batch.
                                        </td>
                                        <td>
                                            50
                                        </td>                                        
                                    </tr>
                                </table>
                            </div>

                            <a class="internal-link" name="cluster"></a>
                            <div class="section-sub-header">Cluster options</div>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Option</th>
                                        <th>Description</th>
                                        <th>Default value</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-part "[STRING]"</code>
                                        </td>
                                        <td>
                                            The SLURM partition or list of partitions (separated by commas) on which to run PhyloAcc jobs.
                                        </td>
                                        <td>
                                            <b>REQUIRED</b>.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">-nodes [INT]</code>
                                        </td>
                                        <td>
                                            The number of nodes on the specified partition to submit jobs to.
                                        </td>
                                        <td>
                                            1
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">-mem [INT]</code>
                                        </td>
                                        <td>
                                            The max memory for each job in GB.
                                        </td>
                                        <td>
                                            4
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">-time [INT]</code>
                                        </td>
                                        <td>
                                            The time in hours to give each job.
                                        </td>
                                        <td>
                                            1
                                        </td>                                        
                                    </tr>

                                </table>
                            </div>

                            <a class="internal-link" name="phyloacc"></a>
                            <div class="section-sub-header">Other PhyloAcc options</div>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Option</th>
                                        <th>Description</th>
                                        <th>Default value</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-st-path [STRING]</code>
                                        </td>
                                        <td>
                                            The path to the PhyloAcc-ST binary.
                                        </td>
                                        <td>
                                            <code class="inline">PhyloAcc-ST</code>
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-gt-path [STRING]</code>
                                        </td>
                                        <td>
                                            The path to the PhyloAcc-GT binary if <code class="inline">-r gt</code> or <code class="inline">-r adaptive</code> are set.
                                        </td>
                                        <td>
                                            <code class="inline">PhyloAcc-GT</code>
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-phyloacc "[STRING]"</code>
                                        </td>
                                        <td>
                                            A catch-all option for other PhyloAcc parameters. 
                                            Enter as a semi-colon delimited list of options: 'OPT1 value;OPT2 value'
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">--options</code>
                                        </td>
                                        <td>
                                            Print the full list of PhyloAcc options that can be specified with <code class="inline">-phyloacc</code> and exit.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>

                                </table>
                            </div>

                            <a class="internal-link" name="misc"></a>
                            <div class="section-sub-header">Miscellaneous options</div>

                            <div class="table-container">
                                <table class="table-content">
                                    <tr>
                                        <th>Option</th>
                                        <th>Description</th>
                                        <th>Default value</th>
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-iqtree-path "[STRING]"</code>
                                        </td>
                                        <td>
                                            When <code class="inline">--theta</code> is set, gene trees will be inferred from some loci with <a href="http://www.iqtree.org/" target="_blank">IQ-TREE</a>.
                                            You can provide the path to your <code class="inline">iqtree</code> executable with this option
                                        </td>
                                        <td>
                                            <code class="inline">iqtree</code>
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-coal-path "[STRING]"</code>
                                        </td>
                                        <td>
                                            When <code class="inline">--theta</code> is set, branch lengths on your species tree will be estimated in coalescent units with an external program. Currently
                                            <a href="https://github.com/smirarab/ASTRAL" target="_blank">ASTRAL</a> With this option you can provide the <b>command</b> to execute your <code class="inline">astral.jar</code> file, 
                                            including any java options. For example, "<code class="inline">java -Xmx8g -jar astral.jar</code>" would be a valid command to specify, provided you had a jar file called <code class="inline">astral.jar</code>.
                                        </td>
                                        <td>
                                            <code class="inline">java -jar astral.jar</code>
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">--labeltree</code>
                                        </td>
                                        <td>
                                            Simply reads the tree from the input mod file (<code class="inline">-m</code>), labels the internal nodes, and exits.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">--overwrite</code>
                                        </td>
                                        <td>
                                            Set this to overwrite existing files.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">--appendlog</code>
                                        </td>
                                        <td>
                                            Set this to keep the old log file even if <code class="inline">--overwrite</code> is specified. 
                                            New log information will instead be appended to the previous log file.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">--summarize</code>
                                        </td>
                                        <td>
                                            Only generate the input summary plots and page. Do not write or overwrite batch job files.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">--info</code>
                                        </td>
                                        <td>
                                            Print some meta information about the program and exit. No other options required.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">--depcheck</code>
                                        </td>
                                        <td>
                                            Run this to check that all dependencies are installed at the provided path. 
                                            No other options necessary.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">--version</code>
                                        </td>
                                        <td>
                                            Simply print the version and exit. Can also be called as <code class="inline">-version</code>, <code class="inline">-v</code>, or <code class="inline">--v</code>.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>
                                    
                                    <tr>
                                        <td>
                                            <code class="inline">--quiet</code>
                                        </td>
                                        <td>
                                            Set this flag to prevent PhyloAcc from reporting detailed information about each step.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>

                                    <tr>
                                        <td>
                                            <code class="inline">-h</code>
                                        </td>
                                        <td>
                                            Print a help menu and exit. Can also be called as <code class="inline">--help</code>.
                                        </td>
                                        <td>
                                            Optional.
                                        </td>                                        
                                    </tr>

                                </table>
                            </div>
                                    
                        </div>
                        <div class="col-2-24" id="inner-margin"></div>
                    </div>
                </div>
            </div>

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
pagefile = "readme.html";
print("Generating " + pagefile + "...");
title = "PhyloAcc - README"
page_style = "file";

head = RC.readHead(title, page_style);
nav = RC.readNav(pagefile);
footer = RC.readFooter();

outfilename = "../../" + pagefile;

with open(outfilename, "w") as outfile:
    outfile.write(html_template.format(head=head, nav=nav, footer=footer));