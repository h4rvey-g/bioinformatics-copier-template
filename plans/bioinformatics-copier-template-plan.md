# Plan: Bioinformatics Analysis Copier Template

## Goal
Create a reusable **Copier** template for bioinformatics analysis projects that generates a project with:

1. **Pixi** for environment and dependency management
2. **Nextflow DSL2** for workflow orchestration
3. **Generation-time executor choice**: Slurm if available, otherwise local
4. **Git-ready** project structure and ignore rules

This plan has been refined using official Copier, Pixi, Nextflow, Bioconda, and nf-core documentation so the scaffold matches current tool conventions more closely.

---

## Documentation-informed decisions

### Copier
- Use a root-level `copier.yml` with **underscore-prefixed settings** such as `_subdirectory`.
- Prefer `_subdirectory: template` so the template repo can keep its own metadata/docs at the repo root while rendering only files from `template/`.
- Use Copier's **advanced question format** for validation and better UX (`type`, `help`, `choices`, `default`, `validator`, `placeholder`, `when`).
- Use a **Copier context hook** via `copier_templates_extensions.TemplateExtensionLoader` to auto-detect host platform details that are not available from prompts alone, especially CPU architecture for Pixi platform defaults.
- Generate and keep `{{ _copier_conf.answers_file }}` in the rendered project so future Copier updates remain possible.
- Avoid post-copy `_tasks` in v1 unless truly necessary; they add trust/execution complexity and are not needed for a clean starter template.

### Pixi
- Use `pixi.toml` with `[workspace]`, `[dependencies]`, and `[tasks]`.
- Use channels in this order: **`conda-forge`, `bioconda`**.
  - Bioconda documentation recommends Pixi with `conda-forge` plus `bioconda`.
  - Pixi's default `channel-priority = "strict"` means channel order matters.
- Use **Bioconda's `nextflow` package** rather than manually installing a launcher script.
  - The Bioconda package already depends on **OpenJDK**.
- Add `requires-pixi` to document the minimum supported Pixi version.
- Use Pixi tasks for common commands like config inspection, the selected executor run command, linting, and cleanup.

### Nextflow
- Use **DSL2 structure** with an explicit `workflow {}` block.
- Do **not** add `nextflow.enable.dsl=2`; current Nextflow docs indicate the old DSL enable flag is no longer needed.
- Keep `main.nf` focused on workflow logic and put most defaults in `nextflow.config` / `conf/*.config`.
- Use profiles activated with `-profile`, but render only one execution profile in the generated project: `slurm` when `has_slurm = true`, otherwise `local`.
- Use `includeConfig` for the chosen executor-specific config file.
- Prefer **stable features only** in v1; avoid preview-only features unless they become necessary.
- Add a `nextflow lint` task because modern Nextflow can lint scripts and config files.

### Slurm
- Configure Slurm with `process.executor = 'slurm'`.
- Keep executor-specific settings in `conf/slurm.config`, while keeping reusable resource tiers in `conf/base.config`.
- Use standard process directives for scheduler resources:
  - `cpus`
  - `memory`
  - `queue` (maps to Slurm partition)
- Treat `time` as optional and leave it unset by default in v1, since the template should not impose walltime limits unless a site wants them.
- Use `executor.account` for Slurm account/project billing when applicable.
- Add nf-core-style process labels such as `process_low`, `process_medium`, `process_high`, and `process_gpu` so modules can request tiers instead of hard-coding resources.
- Avoid mixing `clusterOptions` with standard directives like `queue` and `memory` unless there is a site-specific reason; Nextflow docs warn this can cause undefined behavior.
- For GPU work, assume some Slurm settings may remain cluster-specific, e.g. GPU partition names or `--gres` flags.
- Document that the pipeline must be launched from a node where `sbatch` is available.

### nf-core-inspired structure
Borrow the parts of nf-core structure that are useful without adopting full nf-core complexity:
- `conf/base.config`
- `conf/modules.config`
- `modules/`
- `workflows/`
- `subworkflows/`
- `docs/`

In addition, render exactly one executor config under `conf/`: `slurm.config` or `local.config`.

This gives a familiar layout for bioinformatics users while keeping the template lightweight.

---

## Scope

### In scope
- Copier template contract and prompts
- Template repository layout using `template/`
- Pixi-based runtime/dev environment
- Nextflow DSL2 starter pipeline
- A single execution profile selected at generation time (`slurm` or `local`)
- Resource defaults plus executor-specific config
- Git-friendly project skeleton and docs

### Out of scope for v1
- Full production-grade omics pipeline logic
- Multi-scheduler support beyond Slurm and built-in local execution
- Cloud executors
- Full nf-core compliance/template sync behavior
- Container profiles (`docker`, `apptainer`, `singularity`) in first pass
- CI automation beyond a manual validation checklist

---

## Recommended template repository layout

Use Copier's `_subdirectory` to separate template metadata from rendered project files.

```text
.
├── copier.yml
├── README.md                         # template-repo README
├── plans/
│   └── bioinformatics-copier-template-plan.md
└── template/
    ├── {{ _copier_conf.answers_file }}.jinja
    ├── README.md.jinja
    ├── .gitignore
    ├── .editorconfig
    ├── pixi.toml.jinja
    ├── main.nf.jinja
    ├── nextflow.config.jinja
    ├── conf/
    │   ├── base.config.jinja
    │   ├── modules.config.jinja
    │   └── {{ "slurm" if has_slurm else "local" }}.config.jinja
    ├── workflows/
    │   └── README.md
    ├── modules/
    │   └── local/
    │       └── README.md
    ├── subworkflows/
    │   └── README.md
    ├── bin/
    │   └── README.md
    ├── assets/
    │   └── samplesheet.csv
    ├── examples/
    │   └── README.md
    └── docs/
        ├── development.md
        └── execution.md
```

### Why this layout
- Matches Copier's recommended `_subdirectory` usage.
- Avoids nesting rendered files under `{{ project_slug }}/` inside the destination directory.
- Makes the generated project root correspond directly to the target directory passed to `copier copy`.
- Leaves room for future modules and subworkflows while keeping executor selection simple.

---

## Generated project contract

A rendered project should contain at least:

- `README.md`
- `.copier-answers.yml` (or custom answers file) **committed to Git** if template updates are desired
- `.gitignore`
- `.editorconfig`
- `pixi.toml`
- `main.nf`
- `nextflow.config`
- `conf/base.config`
- `conf/modules.config`
- exactly one executor config: `conf/slurm.config` or `conf/local.config`
- `workflows/`
- `modules/local/`
- `subworkflows/`
- `assets/`
- `examples/`
- `docs/`

---

## Copier design

## Template settings
Use at least:

- `_min_copier_version`
- `_subdirectory: template`
- `_answers_file: .copier-answers.yml`

Optional later:
- `_exclude`
- `_skip_if_exists`

## Prompt set
Keep prompts intentionally small and HPC-focused.

### Required / visible prompts
- `project_name`
- `project_slug`
- `description`
- `author_name`
- `author_email`
- `license`
- `has_slurm` (bool; asks whether the generated project should target Slurm)
- `slurm_partition` (shown only when `has_slurm` is true)
- `slurm_gpu_partition` (optional string; shown only when `has_slurm` is true and may be blank if the cluster uses the same partition or GPU routing is configured later)
- `slurm_account` (optional string; shown only when `has_slurm` is true)
- `pixi_platforms` (multiselect, auto-prefilled from detected host platform)
- `outdir`

### Computed or hidden values
Use `default` + `when: false` for internal values when helpful, e.g.:
- `workflow_name`
- `docs_url_slug`
- normalized IDs derived from `project_slug`
- `detected_host_os`
- `detected_host_arch`
- `detected_pixi_platforms`

### Prompt validation
Use Copier validators for:
- `project_slug`: lowercase, letters/digits/hyphens only
- `author_email`: optional basic email pattern if desired
- partition/account fields: well-formed strings when provided
- `slurm_*` questions should use `when: "{{ has_slurm }}"`

### Example prompt policy
- `project_slug` should be explicitly asked instead of silently derived, because repository/package naming often needs manual control.
- `license` should be a choice list (`MIT`, `Apache-2.0`, `BSD-3-Clause`, `Proprietary/Internal` etc.).
- `has_slurm` should control whether Slurm-specific questions are shown and whether `conf/slurm.config` or `conf/local.config` is rendered.
- `slurm_account` should default to empty string and be rendered conditionally in `slurm.config`.
- `slurm_gpu_partition` should default to empty string and only affect the `process_gpu` label if provided.
- `pixi_platforms` should be a visible multiselect question whose default is auto-generated from host OS/architecture detection, so users can keep the suggested value or override it.
- resource tier values should be template defaults in v1, not Copier prompts.

## Copier update support
Add:

```text
template/{{ _copier_conf.answers_file }}.jinja
```

with content similar to:

```yaml
# Changes here may be overwritten by Copier
{{ _copier_answers | to_nice_yaml }}
```

This preserves answers for future template updates.

---

## Pixi design

## Manifest strategy
Use a single `pixi.toml` workspace for v1.

### `[workspace]`
Include:
- `name`
- `description`
- `authors`
- `channels = ["conda-forge", "bioconda"]`
- `channel-priority = "strict"`
- `platforms`
- `requires-pixi`

### Platform policy
Use Copier to **auto-detect and prefill** the Pixi platforms rather than hard-coding a single default.

Recommended implementation:
- add a Copier context hook that detects host OS and CPU architecture
- map that detection to Pixi platform names
- use the detected value to prefill a visible `pixi_platforms` multiselect question

Recommended default mapping:
- Linux `x86_64` → `['linux-64']`
- Linux `aarch64` / `arm64` → `['linux-aarch64']`
- macOS `x86_64` → `['osx-64', 'linux-64']`
- macOS `arm64` → `['osx-arm64', 'linux-64']`
- Windows or unknown host → `['linux-64']`

Rationale:
- this template targets Slurm, so a Linux platform should usually be present
- users may scaffold from a macOS laptop but still need a Linux lock target for cluster execution
- auto-prefill improves UX while still allowing manual override
- Windows should not be emitted as the default runtime target for this template because Bioconda-based bioinformatics environments are primarily Linux/macOS oriented and the execution target here is HPC Linux

### Context-hook policy
Do not rely only on `_copier_conf.os`, because it does not give enough detail to derive Pixi architecture targets. Use a Copier context hook to expose normalized values such as `detected_host_os`, `detected_host_arch`, and `detected_pixi_platforms`.

## Dependencies
### Required runtime dependencies
- `nextflow`

### Likely useful lightweight dependencies
- `git`
- `python` (only if helper scripts or docs tooling need it)

### Important note
Do **not** add a large set of bioinformatics tools to the base environment in v1.

Rationale:
- tool choice is assay/pipeline specific
- large default envs slow solve/install time
- the base template should stay generic

### Nextflow runtime note
Because the Bioconda `nextflow` package depends on OpenJDK, we should **start without explicitly pinning Java** unless testing reveals a reason to do so.

## Pixi tasks
Use tasks to standardize workflow commands.

Recommended v1 tasks:

- `run`
  - `nextflow run . -profile {{ 'slurm' if has_slurm else 'local' }}`
- `config`
  - `nextflow config . -profile {{ 'slurm' if has_slurm else 'local' }} -flat`
- `lint`
  - `nextflow lint .`
- `clean`
  - remove `work/`, `.nextflow*`, and generated reports/results as appropriate

Optional later:
- explicit `run-slurm` / `run-local` aliases if a team wants them
- `fmt` if `nextflow lint -format` is adopted
- `init-git` helper task, though README instructions may be clearer

---

## Nextflow design

## Language/style choices
- Use **DSL2** conventions only.
- Use an explicit entry `workflow {}` block.
- Keep pipeline parameters in config files instead of scattering defaults inside `main.nf`.
- Keep the initial workflow extremely small but structurally extensible.

## Proposed starter workflow behavior
Use a minimal smoke-test pipeline that is bioinformatics-adjacent but not tied to a specific assay.

### Preferred v1 option
A tiny sample-driven workflow that:
- reads a CSV sample sheet from `assets/samplesheet.csv`
- runs one placeholder process per sample
- writes a small report into `results/`

### Process design options
#### Option A: generic placeholder process
- input: sample ID and file path
- script: simple shell command that copies or summarizes input
- pros: no extra bioinformatics packages
- cons: less domain-flavored

#### Option B: light bioinformatics example
- add one small common tool like `seqkit`
- process: count FASTQ reads / report simple stats
- pros: more realistic for bioinformatics users
- cons: adds a domain dependency to the base env

**Recommendation:** start with **Option A** for v1, then add an optional `seqkit` profile/template variant later if desired.

## File-level structure
### `main.nf`
Should contain:
- entry workflow
- import placeholder for future modules
- sample sheet parsing or simple channel creation
- one example process call
- comments showing where to add real modules/subworkflows

### `workflows/`
Include at least a README or placeholder file describing:
- entry workflow vs named workflows
- where to place assay-specific orchestration logic

### `modules/local/`
Reserve for project-specific DSL2 modules.

### `subworkflows/`
Reserve for reusable multi-step building blocks.

---

## Nextflow config layering

Use a layered configuration model.

## `nextflow.config`
Responsibilities:
- define `params` defaults such as:
  - input/sample sheet path
  - outdir
  - profile name/help text if desired
- include always-loaded configs:
  - `conf/base.config`
  - `conf/modules.config`
- define exactly one execution profile:
  - `slurm` when `has_slurm` is true, with `includeConfig 'conf/slurm.config'`
  - `local` when `has_slurm` is false, with `includeConfig 'conf/local.config'`

This keeps the generated project simple and avoids shipping unused execution profiles.

## `conf/base.config`
Should define executor-independent defaults.

Recommended contents:
- minimal fallback `process` defaults for unlabeled jobs
- nf-core-style labels for resource classes, inspired by common bioinformatics pipelines:
  - `process_low`
  - `process_medium`
  - `process_high`
  - `process_gpu`
- `params.outdir`
- `workDir = 'work'`
- output conventions that treat `results/` as the Git-tracked location for report-like artifacts and `data/` as an ignored location for bulky files if the project later adds them

### Recommended v1 tier table
These should be **starting values only**, easy to edit after generation, and **not** exposed as Copier prompts in v1.

| Label | CPUs | Notes |
| --- | ---: | --- |
| `process_low` | 2 | light QC, parsing, metadata, small transforms |
| `process_medium` | 4 | common single-sample steps |
| `process_high` | 8 | heavier alignment / aggregation steps |
| `process_gpu` | 8 | GPU-enabled jobs; site-specific GPU and memory settings can be added later |

### Why labels are useful
They let users scale resource settings cleanly without hard-coding resources in every process. A process can simply declare `label 'process_medium'`, and cluster tuning then stays centralized in config files.

### Time and memory policy
Do **not** set default `time` or `memory` limits in the v1 tiers. If a site requires walltime or memory limits, they can add them later globally or per label.

## `conf/local.config`
Should define:
- `process.executor = 'local'`
- no scheduler-specific fields
- any lightweight local-only overrides if needed

This file is rendered only when `has_slurm` is false.

## `conf/slurm.config`
Should define:
- `process.executor = 'slurm'`
- `process.queue = '<partition>'` if set
- `executor.account = '<account>'` if non-empty
- optional `withLabel: process_gpu` routing to a GPU partition when `slurm_gpu_partition` is provided
- optional commented placeholders for site-specific GPU requests such as `--gres=gpu:1`
- optional commented placeholders for QoS or other site-specific settings

This file is rendered only when `has_slurm` is true.

### Important restriction
Do not combine `clusterOptions` with standard resource directives unless necessary.
In particular, keep reusable CPU tier definitions in `conf/base.config`, and if users later add memory limits, keep those there as well; reserve `clusterOptions` for site-specific scheduler flags that cannot be expressed otherwise.

## `conf/modules.config`
Can start nearly empty but should exist.

Purpose:
- future per-module overrides
- separation of module-specific tuning from pipeline-wide defaults

---

## Execution profile design details

The generated project should contain exactly one execution profile, selected during `copier copy`.

### If `has_slurm = true`
- render `conf/slurm.config`
- ask for `slurm_partition`, `slurm_account`, and `slurm_gpu_partition`
- expose `-profile slurm`
- point Pixi `run` and `config` tasks at `-profile slurm`

### If `has_slurm = false`
- render `conf/local.config`
- do not ask Slurm-specific questions
- expose `-profile local`
- point Pixi `run` and `config` tasks at `-profile local`

This keeps the generated project smaller and easier to understand because it does not ship an unused executor configuration.

### Slurm-specific assumptions
- user launches from a login node with `sbatch`
- compute nodes share filesystem paths with launch node
- partition name may differ across clusters
- account may be required on some clusters and absent on others

### Minimal Slurm fields to parameterize
- partition (`slurm_partition`)
- account (`slurm_account`)
- optional GPU partition (`slurm_gpu_partition`)

### Resource tier policy
- CPU tier definitions should live in `conf/base.config`, not in Copier prompts.
- v1 should ship `process_low`, `process_medium`, `process_high`, and `process_gpu`.
- v1 should not set walltime or memory limits by default.
- GPU request syntax should remain a commented example because it often varies by cluster.

### Fields to avoid hardcoding in v1
- QoS
- node constraints
- reservation names
- exact GPU request syntax (`--gres=gpu:1`, `--gpus=1`, etc.)
- site-specific `clusterOptions`
- submit throttling / queue sizing

Those should be documented as extension points, not baked into the first template.

---

## Git design

## Repository hygiene for generated project
Generated output should be ready for `git init` and first commit.

### Commit these files
- `pixi.toml`
- `pixi.lock`
- `nextflow.config`
- `conf/*.config`
- `main.nf`
- docs
- assets/example metadata
- `.copier-answers.yml` if template updates are desired
- report-style outputs in `results/`, such as summary tables, plots, small text reports, and other human-consumable artifacts

### Ignore these files/directories
- `.pixi/`
- `.nextflow/`
- `.nextflow*`
- `work/`
- `data/`
- raw or bulky data products if the project later adds them outside `data/`
- editor/temp files

### Git policy for outputs
- Treat `results/` as the Git-tracked location for lightweight analysis outputs that humans review directly.
- Treat `data/` as the default ignored location for large inputs and bulky derived files.
- In v1, the starter workflow should write only small report-type outputs to `results/`.
- If future pipeline steps generate large files such as FASTQ, BAM, CRAM, or other heavy intermediates/finals, route them to `data/` or another ignored path rather than committing them to Git.

### Optional but recommended
- `.editorconfig`
- `.gitattributes` later if syntax highlighting or line-ending normalization becomes useful

## README instructions should explicitly tell users to run
```bash
git init
git add .
git commit -m "Initial commit from Copier template"
```

---

## Concrete file plan

### `copier.yml`
Must define:
- `_min_copier_version`
- `_subdirectory: template`
- `_answers_file`
- all user prompts
- validators for slug/resource fields

Should not rely on post-copy tasks in v1.

### `template/pixi.toml.jinja`
Must define:
- workspace metadata
- channels `conda-forge`, `bioconda`
- strict channel priority
- `platforms` rendered from `pixi_platforms`
- `nextflow` dependency
- tasks for run/config/lint/clean

### `template/nextflow.config.jinja`
Must define:
- default params
- include of `conf/base.config`
- include of `conf/modules.config`
- exactly one profile:
  - `profiles { slurm { includeConfig 'conf/slurm.config' } }` when `has_slurm`
  - `profiles { local { includeConfig 'conf/local.config' } }` otherwise

### `template/conf/base.config.jinja`
Must define:
- executor-independent defaults
- minimal unlabeled defaults
- nf-core-style resource tiers: `process_low`, `process_medium`, `process_high`, `process_gpu`
- no default time or memory limits in v1 tiers
- `workDir`
- output conventions, with `results/` as the default report-style output location

### `template/conf/local.config.jinja`
Must define:
- local executor
- no scheduler-specific settings
- any lightweight local overrides if needed

### `template/conf/slurm.config.jinja`
Must define:
- Slurm executor
- partition/account settings rendered conditionally
- optional GPU partition routing for `process_gpu`
- commented site-specific GPU request examples
- comments for site-specific extension

### `template/conf/modules.config.jinja`
Must exist even if mostly placeholder.

### `template/main.nf.jinja`
Must define:
- entry workflow
- example channel construction
- example process or included local module
- at least one example use of a standard label such as `process_low`
- comments for extension

### `template/README.md.jinja`
Must explain:
- how the project was generated
- Pixi installation/use
- `pixi install`
- `pixi run config`
- `pixi run run`
- whether this generated project targets Slurm or local execution
- Slurm assumptions when applicable
- that `results/` is intended for Git-tracked report artifacts, while `data/` is intended for ignored large inputs/outputs
- how to extend with more modules/processes
- Git init/first commit instructions

---

## Validation plan

## Template-level validation
- [ ] `copier copy` succeeds with default answers
- [ ] `copier copy` succeeds with `has_slurm=true` and `has_slurm=false`
- [ ] rendered paths/names are correct
- [ ] `.copier-answers.yml` is rendered
- [ ] optional empty values such as Slurm account do not create broken config
- [ ] host platform detection prefills `pixi_platforms` correctly
- [ ] exactly one executor config file is rendered in each case

## Generated-project validation
- [ ] `pixi install` succeeds
- [ ] `pixi run config` prints valid resolved config
- [ ] `pixi run lint` passes
- [ ] if generated with `has_slurm=false`, `pixi run run` executes locally
- [ ] local execution creates expected `work/` and `results/` structure
- [ ] `.gitignore` ignores `work/` and `data/` but does not ignore `results/`
- [ ] generated repository is clean and commit-ready

## Slurm-facing validation
At minimum, for `has_slurm=true` renders:
- [ ] Slurm config renders correctly even without account
- [ ] `process.queue` maps to partition as expected
- [ ] `process_gpu` renders sensibly with and without a dedicated GPU partition
- [ ] documentation clearly states that actual cluster-specific GPU flags may need local adjustment

---

## Implementation phases

### Phase 1 — Finalize template contract
- lock prompt set
- add `has_slurm` conditional behavior for executor selection
- choose default resource tiers for `process_low`, `process_medium`, `process_high`, and `process_gpu`
- finalize template repo layout with `_subdirectory: template`
- define host-platform-to-Pixi-platform mapping and context-hook behavior
- decide whether v1 smoke test is generic or lightly bioinformatics-specific

**Deliverable:** stable template contract and layout

### Phase 2 — Scaffold core renderable files
- create `copier.yml`
- create template root files
- create Copier context hook for platform detection
- create `pixi.toml`, `main.nf`, `nextflow.config`
- create `conf/base.config`, `conf/modules.config`, and exactly one executor config template path for `slurm` or `local`

**Deliverable:** Copier can render a project skeleton

### Phase 3 — Make the starter workflow runnable
- add minimal sample data / sample sheet
- implement placeholder process
- verify local execution through Pixi for `has_slurm=false`
- verify `nextflow config -profile ...` behavior for both executor choices

**Deliverable:** generated project runs with its selected execution profile

### Phase 4 — Improve usability and documentation
- expand README
- add docs for project structure and Slurm customization
- add `.editorconfig`
- refine `.gitignore`

**Deliverable:** teammate-friendly starter project

### Phase 5 — Hardening
- test multiple Copier answer combinations
- test both `has_slurm=true` and `has_slurm=false`
- test empty/non-empty Slurm account cases
- test on representative Linux environment
- review version pinning and lockfile behavior

**Deliverable:** v1-ready template

---

## Risks and mitigations

### Risk: Pixi solve issues across channels
- **Mitigation:** use `conda-forge` then `bioconda` with strict channel priority; keep env small.

### Risk: Auto-detected Pixi platforms do not match real deployment target
- **Mitigation:** auto-detect only to prefill defaults, keep `pixi_platforms` user-visible and editable, and bias macOS defaults to also include `linux-64` for Slurm use cases.

### Risk: Git repository gets polluted by large analysis outputs
- **Mitigation:** track `results/` for lightweight report artifacts, ignore `data/` for bulky files, and document that large files should not be published into Git-tracked output paths.

### Risk: Over-opinionated Slurm config
- **Mitigation:** expose only generic partition/account settings, keep default CPU tiers modest, leave memory/time unset by default, and leave site-specific GPU or scheduler flags commented.

### Risk: Smoke test not bioinformatics-relevant enough
- **Mitigation:** ship a structurally correct starter workflow now; add optional bioinformatics example module later.

### Risk: Copier update path breaks
- **Mitigation:** render `.copier-answers.yml` and keep settings/update behavior simple.

### Risk: Nextflow syntax drift over time
- **Mitigation:** use current DSL2 conventions and include `nextflow lint` in validation.

---

## Recommended v1 acceptance criteria

1. A user can generate a project from the Copier template without manual fixes.
2. The generated project installs with Pixi.
3. The generated project exposes exactly one execution profile, selected by the `has_slurm` answer.
4. If generated with `has_slurm=false`, the project runs locally with `pixi run run`.
5. If generated with `has_slurm=true`, the project exposes a Slurm profile via `-profile slurm` and corresponding Pixi tasks.
6. The generated project includes reusable resource labels `process_low`, `process_medium`, `process_high`, and `process_gpu`.
7. The generated project is immediately ready for `git init` and first commit.
8. The generated project keeps `.copier-answers.yml` so template updates remain possible.

---

## Nice-to-have follow-ups
- add optional `seqkit`-based bioinformatics smoke test
- add `nf-test`
- add container profiles (`apptainer`, `docker`)
- add CI to render template and run smoke tests
- add schema/sample sheet validation
- add optional nf-core-style extras only where they remain useful

---

## References used to refine this plan

### Copier
- https://copier.readthedocs.io/en/stable/configuring/
- https://copier.readthedocs.io/en/stable/faq/

### Pixi
- https://pixi.sh/v0.46.0/reference/pixi_manifest/
- https://pixi.sh/v0.22.0/features/advanced_tasks/
- https://pixi.sh/v0.26.0/reference/project_configuration/

### Nextflow
- https://www.nextflow.io/docs/latest/executor.html
- https://www.nextflow.io/docs/latest/reference/config.html
- https://www.nextflow.io/docs/stable/reference/cli.html
- https://www.nextflow.io/docs/latest/your-first-script.html
- https://www.nextflow.io/docs/latest/migrations/dsl1.html
- https://www.nextflow.io/docs/stable/process.html

### Bioconda
- https://bioconda.github.io/
- https://bioconda.github.io/recipes/nextflow/README.html

### nf-core
- https://nf-co.re/docs/contributing/pipelines/pipeline_file_structure
- https://nf-co.re/docs/nf-core-tools/cli/pipelines/create

---

## Immediate next step
Implement **Phase 1 + Phase 2**:
- create `copier.yml`
- create the `template/` subdirectory layout
- scaffold Pixi, Nextflow, and executor config files
- wire up conditional `slurm` or `local` profile rendering so the generated project is runnable and inspectable
