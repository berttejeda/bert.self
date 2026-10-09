# Activity

A year-by-year look at my public open-source work, taken from GitHub commit history.

!!! note "About these numbers"
    Yearly figures are GitHub contribution counts. These leave out commits made under
    email addresses that aren't linked to my account, so earlier years are undercounted.
    Lifetime per-repository totals are listed on the [Projects](projects.md) page.
    Data as of October 2026.

## Timeline

| Year | Contributions | Focus |
|---|---:|---|
| **2026** | 188 | **bert.validator** (46 commits), bert.ai (28), bert.finance (26), bert.zsh (22), bert.webterminal (17), bert.slidev (9) |
| **2025** | 186 | **bert.finance** (36), bert.ops-command (33), bert.zsh (32), bert.tasks (16), bert.yamlcli (15), bert.git-cli (14), bert.astro (12) |
| **2024** | 49 | **bert.cheater** Go rewrite (18), bert.yamlcli (7), bert.minecraft (6), bert.zsh (5), bert.tasks (4) |
| **2023** | 11 | bert.bill, bert.cicd, bert.dashboard, bert.ansible.collection.utilities |
| **2022** | 22 | bert.bill launch, bert.ecli, bert.webterminal, bert.cicd |
| **2021** | 13 | bert.config, bert.sshutil, bert.webadapter, bert.lessons |
| **2020** | 37 | ansible-taskrunner (13), bert.ghactions, bert.ansible |
| **2019** | 240 | **ansible-taskrunner** (109 commits, 112 pull requests) |

## How the work has evolved

### 2016–2019: Windows automation and Ansible tooling

My early public work came out of making Windows workstations into real engineering
environments: [supracmd](https://github.com/berttejeda/supracmd),
[bert.docs](https://github.com/berttejeda/bert.docs) (interactive HTA documents) and
portable Ansible on Cygwin. That led to
[ansible-taskrunner](https://github.com/berttejeda/ansible-taskrunner). 2019 was its
biggest year, with more than 100 commits and 112 pull requests as it became a mature,
PyPI-published CLI framework.

### 2021–2023: Reusable libraries and learning platforms

I pulled common pieces out into libraries I could publish, such as
[bert.config](https://github.com/berttejeda/bert.config),
[bert.sshutil](https://github.com/berttejeda/bert.sshutil) and
[bert.ecli](https://github.com/berttejeda/bert.ecli). I also built
[bert.bill](https://github.com/berttejeda/bert.bill) and later
[bert.dashboard](https://github.com/berttejeda/bert.dashboard), React + Flask platforms
for interactive technical lessons with a live web terminal.

### 2024: Moving to Go

I ported my Python tools to Go to get single-binary distribution:
[bert.cheater](https://github.com/berttejeda/bert.cheater),
[bert.tasks](https://github.com/berttejeda/bert.tasks) and the
[bert.yamlcli](https://github.com/berttejeda/bert.yamlcli) library underneath them.

### 2025–present: Operations tooling, AI and data

Output picked up sharply, to more than 350 contributions across two years. The main threads:

- **Operational rigor.** [bert.validator](https://github.com/berttejeda/bert.validator)
  for manifest-driven validation, distributed via Homebrew, and
  [bert.ops-command](https://github.com/berttejeda/bert.ops-command) to standardize team scripts.
- **AI engineering.** Local LLMs, MCP servers and a Grafana AI-analysis plugin in
  [bert.ai](https://github.com/berttejeda/bert.ai).
- **Data and analysis.** Automated financial and market analysis in
  [bert.finance](https://github.com/berttejeda/bert.finance).
- **Developer platform.** GitHub CLI tooling
  ([bert.git-cli](https://github.com/berttejeda/bert.git-cli)), OS keychain integration
  ([bert.credmgr](https://github.com/berttejeda/bert.credmgr)) and continued work on
  [bert.zsh](https://github.com/berttejeda/bert.zsh).

## By the numbers

| Metric | Value |
|---|---|
| GitHub member since | 2014 |
| Original (non-fork) public repositories | 61 |
| PyPI packages | 13 (`ansible-taskrunner`, `bertdotbill`, `btconfig`, `btgitserver`, `btecli`, `btdashboard`, `btwebterminal`, `btweb`, `btssh`, `bt-cheater`, `bt-ghcli`, `bt-credmgr`, `bt-cred-resolver`) |
| Published PyPI releases | 120+ |
| Most-committed project | ansible-taskrunner (440+ commits) |
| Primary languages | Python, Go, Shell, HCL, TypeScript |
