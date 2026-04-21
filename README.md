# bioinformatics-copier-template

Copier template for bootstrapping a bioinformatics analysis project with:

- [Pixi](https://pixi.sh/) for environment and task management
- [Nextflow DSL2](https://www.nextflow.io/) for workflow orchestration
- generation-time executor selection: **local** or **Slurm**
- a Git-friendly starter layout with updateable Copier answers

## Requirements

This template uses a local Copier context hook via `copier_templates_extensions`, so you must:

- run Copier with `--trust`
- have `copier-templates-extensions` installed alongside Copier

A convenient one-shot invocation is:

```bash
uvx --with copier-templates-extensions --from copier copier copy --trust /path/to/bioinformatics-copier-template my-analysis
```

## Example renders

### Local render

```bash
uvx --with copier-templates-extensions --from copier copier copy --trust /path/to/bioinformatics-copier-template my-analysis
cd my-analysis
pixi install
pixi run config
pixi run lint
pixi run run
```

### Slurm render

```bash
uvx --with copier-templates-extensions --from copier copier copy --trust /path/to/bioinformatics-copier-template my-analysis \
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
