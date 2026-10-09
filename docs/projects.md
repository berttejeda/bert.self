# Projects

A curated selection of my open-source work, grouped by theme. Commit counts are
from each repository's default branch. Every project is on
[GitHub](https://github.com/berttejeda?tab=repositories).

## CLI frameworks & task runners

A recurring theme in my work: describe a command-line interface declaratively in YAML,
and let the tooling generate the CLI, help text and execution plumbing.

| Project | What it does | Stack | Activity |
|---|---|---|---|
| [ansible-taskrunner](https://github.com/berttejeda/ansible-taskrunner) | Wraps `ansible-playbook` and builds a full Click CLI from playbook vars: options, subcommands, help messages and embedded shell functions. On [PyPI](https://pypi.org/project/ansible-taskrunner/). | Python, Click, Ansible | 440+ commits · 33 releases · ★ 17 |
| [bert.tasks](https://github.com/berttejeda/bert.tasks) | A Go rewrite of ansible-taskrunner. | Go | 2024–2025 |
| [bert.yamlcli](https://github.com/berttejeda/bert.yamlcli) | A Go library for defining CLIs in YAML, built on kingpin. | Go | 2024–2025 |
| [bert.ops-command](https://github.com/berttejeda/bert.ops-command) | Discovers a team's scattered scripts and exposes them through a single `ops` entrypoint with dot-notation subcommands. | Bash | 39 commits · 2025–2026 |
| [bert.ecli](https://github.com/berttejeda/bert.ecli) | An extensible, plugin-driven command-line tool. Plugins live in [bert.ecli.plugins](https://github.com/berttejeda/bert.ecli.plugins). On [PyPI](https://pypi.org/project/btecli/). | Python | 8 releases |
| [make-zipapp](https://github.com/berttejeda/make-zipapp) | Generates a self-contained Python zipapp from a script. | Python | ★ 2 |

## Validation, testing & operations

| Project | What it does | Stack | Activity |
|---|---|---|---|
| [bert.validator](https://github.com/berttejeda/bert.validator) | Runs shell-based validation tests from a YAML manifest. Supports Sprig templating, tag filtering, includes, loops, conditions and a run summary. Install with `brew install berttejeda/tap/bert-validator`. | Go | 54 commits · most active in 2026 |
| [bert.observability](https://github.com/berttejeda/bert.observability) | Observability experiments, including a health dashboard built from Mermaid diagrams. | Shell, Mermaid | 2026 |
| [terraform-aws-sentinel](https://github.com/berttejeda/terraform-aws-sentinel) | Terraform for shipping AWS CloudTrail logs to Microsoft Sentinel, with scoped IAM/KMS policies. | Terraform | 2025 |
| [bert.ansible.collection.utilities](https://github.com/berttejeda/bert.ansible.collection.utilities) | An Ansible Galaxy collection with a file-system inventory plugin. | Python, Ansible | 2023–2024 |

## Developer tooling & libraries

| Project | What it does | Stack | Activity |
|---|---|---|---|
| [bert.git-server](https://github.com/berttejeda/bert.git-server) | A Git server over HTTP that serves any repository under configured search paths and creates repos when you first push them. Runs on gunicorn. On [PyPI](https://pypi.org/project/btgitserver/). | Python | 10 releases · ★ 4 |
| [bert.git-cli](https://github.com/berttejeda/bert.git-cli) | `ghpr` and `ghsearch` CLIs for GitHub and GitHub Enterprise: PR management plus repo, code and commit search. On [PyPI](https://pypi.org/project/bt-ghcli/). | Python | 2025–2026 |
| [bert.credmgr](https://github.com/berttejeda/bert.credmgr) | A credential CLI and library across macOS Keychain, Windows Credential Manager and Linux Secret Service. On [PyPI](https://pypi.org/project/bt-credmgr/). | Python | 2026 |
| [bert.cred-resolver](https://github.com/berttejeda/bert.cred-resolver) | Credential-resolution helpers on top of the OS password manager. Now archived. On [PyPI](https://pypi.org/project/bt-cred-resolver/). | Python | 2026 |
| [bert.webadapter](https://github.com/berttejeda/bert.webadapter) | A small wrapper around `requests` for downloading files, reused across my projects. On [PyPI](https://pypi.org/project/btweb/). | Python | 2021–2023 |
| [bert.config](https://github.com/berttejeda/bert.config) | A YAML config reader with dot-notation and wildcard lookups and Jinja templating. On [PyPI](https://pypi.org/project/btconfig/). | Python | 77 commits · 15 releases |
| [bert.sshutil](https://github.com/berttejeda/bert.sshutil) | Edit locally, run remotely: SSH command execution with local-to-remote directory sync. On [PyPI](https://pypi.org/project/btssh/). | Python, Paramiko | 2021–2023 |
| [bert.cheater](https://github.com/berttejeda/bert.cheater) | A keyword-searchable cheatsheet CLI, rewritten in Go from [the Python original](https://github.com/berttejeda/bert.cheater.python) (on [PyPI](https://pypi.org/project/bt-cheater/)). | Go | 2024 |
| [bert.video-stitcher](https://github.com/berttejeda/bert.video-stitcher) | Builds a video from images and clips, driven by YAML, with crossfades, watermarks and background music. Uses FFmpeg. | Python, FFmpeg | 2026 |

## Learning platforms & education

I spend a lot of time helping other engineers get up to speed, so I build tools for that too.

| Project | What it does | Stack | Activity |
|---|---|---|---|
| [bert.dashboard](https://github.com/berttejeda/bert.dashboard) | Interactive lessons written in Markdown and templated with Jinja, plus an embedded web terminal. On [PyPI](https://pypi.org/project/btdashboard/). | React, Flask | 45 commits |
| [bert.bill](https://github.com/berttejeda/bert.bill) | Bert's Interactive Lesson Loader, the predecessor to bert.dashboard. Now archived. On [PyPI](https://pypi.org/project/bertdotbill/). | React, Flask | 105 commits · 34 releases |
| [bert.webterminal](https://github.com/berttejeda/bert.webterminal) | A WebSocket agent that connects xterm.js front ends to a local shell. Shipped as a Docker image and on [PyPI](https://pypi.org/project/btwebterminal/). | Python, Docker | 2022–2026 |
| [bert.lessons](https://github.com/berttejeda/bert.lessons) | Hands-on lessons for Ansible, Kubernetes, Crossplane and Terraform. These power the [Notes](notes.md) section of this site. | Markdown, HCL | 47 commits |
| [bert.slidev](https://github.com/berttejeda/bert.slidev) | Slidev add-ons, including a web-terminal add-on for live demos. | Vue, TypeScript | 2026 |
| [bert.docs](https://github.com/berttejeda/bert.docs) | Interactive HTA documents built from Markdown with Pandoc, with embedded PowerShell and cmd execution. | HTML, PowerShell | ★ 13 |

## AI & data

| Project | What it does | Stack | Activity |
|---|---|---|---|
| [bert.ai](https://github.com/berttejeda/bert.ai) | Hands-on AI work: Ollama and llama.cpp setups, MCP servers, prompt tooling, and a Grafana panel plugin for AI-assisted analysis. | Python, Go, TypeScript | 30 commits · 2026 |
| [bert.finance](https://github.com/berttejeda/bert.finance) | Automated financial analysis: bank-export categorization, stock pattern detection and options analysis, with metrics exported to Grafana. | Python | 61 commits · 2025–2026 |

## Workstation & shell environment

| Project | What it does | Stack | Activity |
|---|---|---|---|
| [bert.zsh](https://github.com/berttejeda/bert.zsh) | My Zsh function library, with a one-line installer. Maintained continuously. | Zsh | 126 commits |
| [bert.bash](https://github.com/berttejeda/bert.bash) | My Bash function library. | Bash | 42 commits |
| [bert.aioc](https://github.com/berttejeda/bert.aioc) | All-In-One Command-line Console, my Windows terminal configuration. | PowerShell | 2023 |
| [bert.autohotkey](https://github.com/berttejeda/bert.autohotkey) | AutoHotkey automation for Windows. | AutoHotkey | 2021 |
| [supracmd](https://github.com/berttejeda/supracmd) | Scripts for a better Windows command line using the Console2 wrapper. | Shell, Batch | 2016–2017 |
