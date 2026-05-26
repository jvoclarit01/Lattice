---
name: skill-integration-protocol
description: Lattice skill integration protocol. Governs the explicit invocation contracts, inputs, outputs, and enforcements for external wired-in skills.
---

# Skill Integration Protocol

Lattice integrates and orchestrates external specialized skills to guide project setup, design enforcement, code quality, and codebase discovery.

## 1. UI/UX Pro Max (`ui-ux-pro-max:ui-ux-pro-max`)

The design system provider. It runs once per project initialization containing UI elements, or when a major UI theme reset is requested.

- **Trigger**: Run once on project init when a user request involves frontend/UI.
- **Inputs**:
  - `product_type`: type of web application (e.g., dashboard, marketing, SaaS, mobile-web).
  - `intent`: core objective of the UI (e.g., speed, clarity, premium conversion, data density).
  - `stack`: chosen frontend technologies (e.g., Next.js + CSS Modules, React + Tailwind).
  - `industry_tags`: domain context tags (e.g., fintech, developer-tools, healthtech).
  - `brand_anchors`: core aesthetic keywords (e.g., minimal, glassmorphism, high-contrast, dark-tech).
- **Outputs**:
  - `.lattice/design-system/MASTER.md`: Master design system rules.
  - `.lattice/design-system/tokens.json`: Specific design tokens (spacing, palette HSL, fonts).
  - `.lattice/design-system/anti_patterns.yaml`: Visual patterns banned for the project.
- **Binding**: A mandatory prompt fragment referencing `.lattice/design-system/MASTER.md` is appended to all subsequent subagents or tasks doing UI work.

---

## 2. Design Taste Frontend (`design-taste-frontend`)

The design system enforcer. Auto-activates on every UI file write to prevent generic AI design patterns.

- **Trigger**: Automatically active on file changes matching frontend extensions (`.css`, `.html`, `.js`, `.jsx`, `.ts`, `.tsx`, `.vue`, `.svelte`).
- **Dials**: Configures visual parameters using three numeric dials (`0-10` scale):
  1. `DESIGN_VARIANCE` (Default: `8`): Spacing, asymmetric layout, and layout randomness intensity.
  2. `MOTION_INTENSITY` (Default: `6`): Speed, curves, and volume of micro-animations/transitions.
  3. `VISUAL_DENSITY` (Default: `4`): Information/element density per viewport.
- **Overrides**: Parameters can be overridden per route or component inside the project's root config `lattice.toml`:
  ```toml
  [design_taste.overrides."/dashboard"]
  visual_density = 8
  motion_intensity = 2
  ```
- **Violation Surface**: Compiles lint-like styling violations. Any file write triggering a design violation must be corrected before proceeding past the VERIFY phase.

---

## 3. Karpathy Guidelines (`andrej-karpathy-skills:karpathy-guidelines`)

The code quality invariant. Always active during tasks involving script or application code writing.

- **Trigger**: Always-on for any file creation, editing, or refactoring task.
- **The Four Pillars (Lattice Invariants)**:
  1. **Think Before Coding**: Analyze the code flow, state propagation, and side effects in thinking blocks before typing.
  2. **Simplicity First**: Reject over-engineering. Favor readable, explicit code paths over clever abstractions.
  3. **Surgical Changes**: Make precise edits. Do not refactor unrelated code blocks or delete comments/documentation.
  4. **Goal-Driven Execution**: Align every line written directly to the current task item in the plan.
- **Enforcement**: Prior to saving code, self-assess against the four pillars.

---

## 4. Graphify (`graphify`)

The codebase discovery tool. Invoked on demand or automatically at the start of work on a large, unfamiliar project.

- **Trigger**: Triggered at project start for unfamiliar structures, or user-invoked via the `/graphify` slash command.
- **Output**: Writes codebase relationship maps, schemas, and import trees to the `graphify-out/` directory.
- **Usage**: Used to seed `RESEARCH.md` during the planning phase.

---

## 5. Understand-Anything (`understand-anything`)

The software codebase mapping and domain flow extraction tool. Invoked automatically at project start in `project-lattice` mode, or on demand for codebases.

- **Trigger**: Triggered at project start for software repositories in `project-lattice` mode, or user-invoked via the `/understand` slash command.
- **Inputs**: None.
- **Output**: Writes codebase knowledge-graph schemas, architecture layer classifications (`api`, `service`, `data`, `ui`, `utility`), and guided onboarding tours to the `.understand-anything/` directory.
- **Usage**: Used to seed `RESEARCH.md` and define component boundaries in planning.
