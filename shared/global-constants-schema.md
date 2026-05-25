# Global Constants Schema

Global Constants are captured during Phase 1 of whichever mode is active. They are passed into every domain skill invoked. Never overridden silently — conflicts are flagged explicitly.

## Schema

```yaml
global_constants:
  # project-lattice
  language: "TypeScript" | "Python" | "JavaScript" | "Go" | "Rust" | ...
  framework: "Next.js" | "React" | "Express" | "Django" | "FastAPI" | ...
  style_guide: "Airbnb" | "Google" | "Standard" | "Prettier" | ...
  ui_library: "shadcn/ui" | "Tailwind" | "Material-UI" | "Chakra" | ...

  # model-lattice
  modality: "text" | "image" | "tabular" | "multimodal" | "time-series"
  compute_budget: "local" | "cloud" | "hybrid"
  data_situation: "clean" | "messy" | "from_scratch" | "existing"
  ml_framework: "scikit-learn" | "PyTorch" | "TensorFlow" | "XGBoost" | ...

  # thesis-lattice
  citation_style: "APA" | "MLA" | "Chicago" | "IEEE" | "Harvard" | ...
  academic_level: "undergraduate" | "graduate" | "phd" | "postdoc"
  target_audience: "peers" | "general" | "committee" | "industry"
  document_type: "thesis" | "journal" | "conference" | "report" | ...
```

## Rules

1. **Never override silently** — If a new value conflicts with an existing constant, flag it explicitly and ask for confirmation
2. **Document the reasoning** — For each constant, explain why it was chosen
3. **Update only with user confirmation** — Never change a constant without asking first
4. **Pass to all domain skills** — Every domain skill receives the full set of Global Constants

## Example

```yaml
global_constants:
  language: "TypeScript"
  framework: "Next.js"
  style_guide: "Prettier"
  ui_library: "shadcn/ui"
  reasoning: "Chosen for type safety, modern React patterns, and excellent developer experience"
```

## When to Capture

Global Constants are captured during **Phase 1** of the active mode:
- **project-lattice** → Phase 2: Consultative Stack Selection
- **model-lattice** → Phase 2: Consultative Approach & Stack Selection
- **thesis-lattice** → Phase 1: Research Framing & Project Brief

## The Principle

Global Constants are the **project's configuration**. They ensure consistency across all domain skills and prevent drift. Treat them like environment variables — set once, use everywhere.
