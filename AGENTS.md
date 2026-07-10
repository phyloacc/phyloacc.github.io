# LLM Agent rules and guardrails

## Project information

- This directory contains the website for the PhyloAcc tool.
- The current project directory is `phyloacc.github.io/`, referred to as `<project directory>` in this file.


## Project directory guardrails

- At the beginning of every session, confirm that you are working in the `<project directory>` listed above.
- In plain text, this is referred to as the "project directory", or one of the synoyms listed below.
- Synonyms for the term project directory include "project directory", "current directory", "working directory", "project workspace", "workspace", "repository", "repo". These all refer to the same directory listed above, and the same guardrails apply to all of these terms.
- Only run commands or modify files within the project directory, and never ever run commands or modify files in parent directories or other locations on the filesystem.
- Treat this project directory as a secure, private, and confidential workspace, and do not share any information about it without explicit user permission.
- Treat this project directory as a completely isolated environment, and do not interact with or affect any other part of the filesystem or external systems without explicit user permission.

## Environment

- Do not install any packages or dependencies and do not modify the environment in any way without explicit user permission. Always ask for permission before installing any packages, and be transparent about what packages are being installed and why they are needed.
- Do not modify any system-level configurations or settings, and do not run any commands that could affect the system or other users without explicit user permission. Always ask for permission before running any commands that could affect the system, and be transparent about what commands are being run and why they are needed.

## Command execution guardrails

Allowed without prompt:
- read files
- list files
- modify scripts
- modify config files

Ask for permission:
- software/package installation
- network access
- git push or pull
- chmod
- API access 
- tool writes
- modification of any non-script or non-config files
- any command that could delete files, or any script that has the potential to delete files

### Specific rules

- Do not run destructive file deletion commands such as `rm`, `find -delete`, or scripted equivalents.
- Do not run git-destructive commands such as `git reset --hard`, `git clean -fd`, or `git checkout --`.
- If deletion is required, ask the user first and wait for explicit confirmation.
- Never ever delete a file without asking permission.

## Coding rules

- Never modify scripts or parts of scripts that are not related to the user's request.
- Never insert silent fallbacks or error handling that could hide errors or issues from the user. Always be transparent about any errors or issues that occur, and do not attempt to handle them without user knowledge and permission.
- Never insert silent fallbacks that do not achieve the stated objective of the code.
- Never hide errors in scripts or workflows. If there is an error the script should fail. Errors are useful and necessary information so it is counterproductive to hide them.

## Data analysis rules

- Never modify notebooks or parts of notebooks that are not related to the user's request.
- Notebooks should contain sections the clearly define all filtering, assumptions, and definitions of terms relevant for understanding the results of the analysis.
- Always be explicit about how data is categorized/binned/clustered by adding text to the notebook or plot. This text should both be plain for interpretation and technical to understand the underlying code.
- Accompanying every plot or analysis should be plain text that aids in the interpretation of said plot or analysis.

## Network access guardrails

- Never send or share any data outside of the project directory, and never share any data with third parties without explicit user permission.
- Never send data via any network, API, or external service without explicit user permission.
- Always ask for permission before sharing any data, and be transparent about what data is being shared.

## Code of conduct

- Never ever make up, mock, simulate, fabricate, or lie about input data or outputs.
- If simulated data is needed, always ask the user for permission to create it, and be transparent about the fact that it is simulated.
- Never hide errors in scripts or workflows. If there is an error the script should fail. Errors are useful and necessary information so it is misleading to hide them.