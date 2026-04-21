# bioinformatics-copier-template

Copier template for bootstrapping a bioinformatics analysis project with:

- [Pixi](https://pixi.sh/) for environment and task management
- [Nextflow DSL2](https://www.nextflow.io/) for workflow orchestration
- generation-time executor selection: **local** or **Slurm**
- a Git-friendly starter layout with updateable Copier answers

## How to use

This template uses a local Copier context hook via `copier_templates_extensions`, so you must:

- run Copier with `--trust`
- have `copier-templates-extensions` installed alongside Copier

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
pixi install
pixi run config
pixi run lint
pixi run run
```

### Slurm render example

```bash
uvx --with copier-templates-extensions --from copier copier copy --trust \
  https://github.com/h4rvey-g/bioinformatics-copier-template.git \
  my-analysis \
  -d has_slurm=true \
  -d slurm_partition=compute \
  -d slurm_gpu_partition=gpu \
  -d slurm_account=my-lab
```

## Generated project highlights

A rendered project includes:

- `pixi.toml`
- `main.nf`
- `nextflow.config`
- `conf/base.config`
- `conf/modules.config`
- exactly one executor config: `conf/local.config` or `conf/slurm.config`
- `.copier-answers.yml`

The starter workflow reads `assets/samplesheet.csv` and writes small summary files into `results/` for smoke testing.

## Notes for template development

- Use the repository root or an absolute template path when re-running `copier copy`.
- If you validate renders under `/tmp`, watch available disk space after `pixi install`.
- Source plan: `plans/bioinformatics-copier-template-plan.md`
