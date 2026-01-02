# Experiment Template Usage Guide

## Creating a New Experiment

Follow these steps to create a new experiment using the template:

### 1. Copy the Template

```bash
cd /workspaces/claude-quickstarts/experiments

# Determine next experiment number (e.g., 03, 04, etc.)
NEXT_NUM=03
CAPABILITY_NAME="capability-name"

# Copy template
cp -r _shared/templates/experiment-template/ ${NEXT_NUM}-${CAPABILITY_NAME}/
```

### 2. Update Placeholders

Replace all template placeholders in the new experiment:

```bash
cd ${NEXT_NUM}-${CAPABILITY_NAME}

# Update README.md
# - Replace "NN" with your experiment number
# - Replace "[Capability Name]" with your capability
# - Fill in Overview section
# - Update metrics and documentation sections

# Update run_experiment.py
# - Replace "NN" with your experiment number
# - Replace "[Capability Name]" with your capability
# - Update help text and descriptions

# Make run_experiment.py executable
chmod +x run_experiment.py
```

### 3. Configure Prompts

Copy or create prompts in `config/prompts/`:

**Required prompts:**
- `spec_librarian_prompt.md` - For deriving requirements
- `spec_reviewer_prompt.md` - For filtering tech details
- `coding_prompt.md` - For implementation
- `phase_constraint.txt` - Experiment constraints

**Optional prompts:**
- `oracle_prompt.md` - For citation-only answers

**Tip**: Copy from existing experiments (01-evidence-detection or 02-key-point-analysis) and modify:

```bash
# Copy from previous experiment
cp ../01-evidence-detection/config/prompts/*.md config/prompts/
cp ../01-evidence-detection/config/prompts/*.txt config/prompts/

# Then customize for your capability
```

### 4. Set Up Configuration

1. **Create .env file** (optional, for API keys):
   ```bash
   # config/.env
   ANTHROPIC_API_KEY=your_key_here
   ```

2. **Update requirements.txt**:
   Add any experiment-specific Python dependencies

### 5. Create Documentation

Create experiment-specific documentation in `notes/`:

**Recommended files:**
- `EXPERIMENT_STRATEGY.md` - Your experiment approach and hypothesis
- `CRITICAL_REQUIREMENTS.md` - Non-negotiable requirements (if any)
- `LESSONS_LEARNED.md` - Document insights as you go

### 6. Run Your First Test

```bash
# Test with limited iterations first
python run_experiment.py \
    --project-dir outputs/runs/test-run \
    --max-iterations 5

# Monitor progress
tail -f outputs/runs/test-run/live.log
```

### 7. Iterate and Document

1. Review results in `outputs/runs/test-run/`
2. Adjust prompts and configuration as needed
3. Document findings in `notes/`
4. Create reports in `outputs/reports/`

## Template Structure

```
experiment-template/
├── README.md                   ← Update with experiment details
├── run_experiment.py          ← Update placeholders, make executable
├── .gitignore                 ← Use as-is (keeps logs, excludes bytecode)
├── config/
│   ├── prompts/              ← Copy from existing experiment and customize
│   │   ├── spec_librarian_prompt.md
│   │   ├── spec_reviewer_prompt.md
│   │   ├── coding_prompt.md
│   │   └── phase_constraint.txt
│   └── requirements.txt      ← Add dependencies
├── outputs/
│   ├── runs/                 ← Generated during experiments (not in template)
│   └── reports/              ← Created manually or by scripts
└── notes/
    ├── EXPERIMENT_STRATEGY.md
    └── ... (other docs)
```

## Quick Checklist

After creating new experiment from template:

- [ ] Updated README.md with experiment details
- [ ] Updated run_experiment.py placeholders
- [ ] Made run_experiment.py executable (`chmod +x`)
- [ ] Copied and customized prompts from existing experiment
- [ ] Created config/.env with API key (or set environment variable)
- [ ] Updated config/requirements.txt with dependencies
- [ ] Created notes/EXPERIMENT_STRATEGY.md
- [ ] Tested with small run (`--max-iterations 5`)
- [ ] Reviewed outputs and adjusted configuration
- [ ] Documented initial findings

## Path References in Prompts

**IMPORTANT**: Update path references in prompts to point to shared data:

```markdown
# OLD (don't use):
../deep-wiki-spec-files/
../reference-files/

# NEW (correct):
../../../_shared/data/deepwiki/
../../../_shared/data/reference-examples/
```

From run directory (`outputs/runs/my-run/`):
- `../../../` goes up to experiment root
- `../_shared/` accesses shared resources
- Full path: `../../../_shared/data/deepwiki/`

## Tips

1. **Start Simple**: Begin with a working experiment (01 or 02) as reference
2. **Test Early**: Run with `--max-iterations 5` first to catch issues quickly
3. **Monitor Logs**: Use `tail -f outputs/runs/*/live.log` to watch progress
4. **Document As You Go**: Update notes/ throughout the experiment
5. **Review Commits**: Check git log in run directories to see agent progress
6. **Iterate Prompts**: Adjust prompts based on agent behavior
7. **Share Learnings**: Document insights for future experiments

## Common Issues

### Issue: "Module not found" errors
**Solution**: Ensure `sys.path.insert(0, str(SHARED_INFRA))` is in run_experiment.py

### Issue: "File not found" errors in agents
**Solution**: Check path references in prompts use correct relative paths

### Issue: Git not initialized in runs
**Solution**: This is handled automatically by shared infrastructure

### Issue: API key not found
**Solution**: Set ANTHROPIC_API_KEY environment variable or create config/.env

## Next Steps

After your experiment completes:

1. **Analyze Results**: Review `outputs/runs/*/feature_list.json` and logs
2. **Create Report**: Document findings in `outputs/reports/YYYY-MM-DD_*.md`
3. **Update README**: Fill in actual metrics and status
4. **Share Insights**: Update notes/ with lessons learned
5. **Plan Next Experiment**: Build on patterns established here

---

Last Updated: 2026-01-02
