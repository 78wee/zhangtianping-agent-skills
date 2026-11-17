---
name: siemens-eq300-manual
description: Use when Codex needs to answer questions about the Siemens EQ300 TF30 Chinese manual, including first setup, water hardness, BRITA/Siemens water filter setup, drink strength, Americano/espresso settings, grinder adjustment, cup volume, milk frothing, cleaning, Calc'nClean, maintenance, accessories, troubleshooting display messages, or technical specs for the EQ300 fully automatic coffee machine.
---

# Siemens EQ300 Manual

Use this skill to give practical, manual-grounded help for the Siemens EQ300 TF30 fully automatic coffee machine.

## Workflow

1. Identify the user's task: setup, water/filter, drink tuning, grinder, cleaning, Calc'nClean, fault message, or specs.
2. Read `references/eq300_quick_reference.md` for the relevant section.
3. If the user needs exact wording, page context, or a rare issue, search `references/eq300_manual_zh_extracted.txt`.
4. Give concise, step-by-step guidance in Chinese by default.
5. Mention safety limits when relevant, especially grinder adjustment, descaling products, dishwasher-safe parts, voltage, hot milk/frother, or electric shock risk.

## Resource Guide

- `references/eq300_quick_reference.md`: start here for page map, settings, water hardness, drink tuning, cleaning, Calc'nClean, faults, and specs.
- `references/eq300_manual_zh_extracted.txt`: full extracted text from the Chinese PDF. Use `rg` to locate exact terms like `W. hardness`, `Calc'nClean`, `Fill water tank`, `研磨度`, `咖啡过苦`, or `萃取单元`.
- `assets/eq300_manual_zh.pdf`: original Chinese manual PDF for visual checking when extracted text drops button icons or diagrams.

## Common Guidance

Water hardness:

- The Chinese manual says to ask the local water utility and set `W. hardness`.
- Choose `Water filter` when using a water filter.
- Choose `H2O-Softener` when the home has a water softening system.
- If asked to map numeric hardness, use the BSH/Siemens cross-model guidance in the quick reference and label it as practical guidance, because the Chinese PDF itself does not print the mapping table.

Grinder:

- Only adjust while the grinder is running.
- Move one small step at a time.
- New grinder settings show clearly after the second coffee.
- Counterclockwise means finer; clockwise means coarser.
- Sour/thin/fast/low crema usually means finer. Bitter/burnt/dripping/slow usually means coarser.

Drink tuning:

- Strength applies to all coffee-containing drinks.
- Espresso cup volume range is 25-60 ml.
- Long coffee range is 80-200 ml.
- For Americano-style drinking, prefer a 35-40 ml espresso diluted with hot water, or keep long coffee moderate, rather than over-extracting to a huge cup.

Cleaning:

- Do not use vinegar, pure citric acid, phosphoric-acid descaler, abrasive cleaners, alcohol/benzene cleaners, steam cleaners, or pressure washers.
- Use Siemens/BSH cleaning and descaling tablets.
- Brew unit is not dishwasher-safe and should not be cleaned with detergent.
