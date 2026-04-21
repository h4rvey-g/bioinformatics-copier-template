# bioinformatics-copier-template

Copier template for bootstrapping a bioinformatics analysis project with:

- [Pixi](https://pixi.sh/) for environment and task management
- [Nextflow DSL2](https://www.nextflow.io/) for workflow orchestration
- generation-time executor selection: **local** or **Slurm**
- a Git-friendly starter layout with updateable Copier answers
- automatic `git init` during `copier copy`

## How to use

This template uses a local Copier context hook via `copier_templates_extensions` and a post-copy task to initialize Git, so you must:

- run Copier with `--trust`
- have `copier-templates-extensions` installed alongside Copier

By default, a generated project is automatically initialized as a Git repository during `copier copy`. If you want to skip that behavior, pass `--skip-tasks`.

### Option 1: one-shot usage with `uvx` (recommended)

This is the easiest way to initialize a project from the GitHub template URL:

```bash
uvx --with copier-templates-extensions --from copier copier copy --trust \
  https://github.com/h4rvey-g/bioinformatics-copier-template.git \
  path/to/destination
```

### Option 2: install Copier + extensions together, then use `copier copy`

If you already have Copier and `copier-templates-extensions` installed in the same environment, you can initialize a project directly with:

```bash
copier copy --trust https://github.com/h4rvey-g/bioinformatics-copier-template.git path/to/destination
```

> [!NOTE]
> Make sure `path/to/destination` is an empty directory, or a directory you intentionally want Copier to populate/update.

### Local render example

```bash
uvx --with copier-templates-extensions --from copier copier copy --trust \
  https://github.com/h4rvey-g/bioinformatics-copier-template.git \
  my-analysis
cd my-analysis
git status
pixi install
pixi run config
pixi run lint
pixi run run
```

### Slurm render example

By default, `Primary author or team name` and `Slurm account/project for billing` are prefilled from the current username.

```bash
uvx --with copier-templates-extensions --from copier copier copy --trust \
  https://github.com/h4rvey-g/bioinformatics-copier-template.git \
  my-analysis \
  -d has_slurm=true \
  -d slurm_partition=compute \
  -d slurm_gpu_partition=gpu
```

For Slurm renders, the generated `pixi run run` task uses:

```bash
nextflow run . -profile slurm -resume
```

and the generated Nextflow config enables lenient process caching, which is a safer default on shared HPC filesystems.

## Generated project highlights

A rendered project includes:

- `pixi.toml`
- `main.nf`
- `nextflow.config`
- `conf/base.config`
- `conf/modules.config`
- exactly one executor config: `conf/local.config` or `conf/slurm.config`
- `.copier-answers.yml`
- `AGENTS.md`

The starter workflow reads `assets/samplesheet.csv` and writes small summary files into `results/` for smoke testing.

The rendered project also includes pre-created `data/` and `results/` directories for bulky data and lightweight reviewable outputs, respectively.

## Suggested directory naming rules

For generated projects, prefer these directory conventions:

- keep directories shallow, ideally no more than 3 levels deep
- avoid spaces or special characters; use `_` or `-` when separators help readability
- prefer lowercase names for portability across systems
- consider numeric step prefixes such as `101_raw_data/` and `102_qc/`
- keep step prefixes aligned across code, data, and results for the same stage

The rendered destination is also auto-initialized as a Git repository unless Copier is run with `--skip-tasks`.

## Updating an existing generated project

Copier updates work best if the generated project keeps its `.copier-answers.yml` file committed to Git.

From the generated project directory, run either:

```bash
uvx --with copier-templates-extensions --from copier copier update --trust
```

or, if Copier and `copier-templates-extensions` are already installed together:

```bash
copier update --trust
```

Notes:

- run the command from the root of the generated project
- commit or stash local changes first for a cleaner update experience
- if you do not want Copier tasks to run again during update, add `--skip-tasks`
- review any merge conflicts, then re-run checks such as `pixi run config`, `pixi run lint`, and your workflow smoke test

## Notes for template development

- Use the repository root or an absolute template path when re-running `copier copy`.
- If you validate renders under `/tmp`, watch available disk space after `pixi install`.
- Source plan: `plans/bioinformatics-copier-template-plan.md`
