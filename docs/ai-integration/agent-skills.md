# Agent Skills

eptr2 bundles agent skills that provide specialized guidance for different types of electricity market data queries.

## What are Agent Skills?

Agent Skills are structured knowledge files in the provider-agnostic Agent Skills format — a directory containing a `SKILL.md` file with trigger descriptions plus optional reference files and scripts. Any compatible AI assistant or agent runtime can consume them: when you ask about electricity prices, consumption, or generation, the assistant automatically loads the relevant skill.

## Available Skills

| Skill | Triggers On | Use Case |
|-------|-------------|----------|
| **eptr2-price-analysis** | PTF, SMF, MCP, SMP, electricity prices | Price queries and analysis |
| **eptr2-consumption-data** | UECM, load plan, demand forecast | Consumption tracking |
| **eptr2-generation-tracking** | UEVM, generation, renewables | Generation monitoring |
| **eptr2-imbalance-costs** | KUPST, imbalance, deviation costs | Imbalance calculations |
| **eptr2-market-operations** | GÖP, GİP, DGP, market orders | Market operations data |
| **eptr2-api-discovery** | Available endpoints, API search | Finding the right API |
| **eptr2-convenience-wrappers** | get_* functions, typed wrappers, eptr2.calls | IDE-friendly typed code |

## How Skills Work

Skills are automatically invoked based on your query:

| Your Question | Skill Triggered |
|---------------|-----------------|
| "What are today's electricity prices?" | eptr2-price-analysis |
| "Show me wind generation data" | eptr2-generation-tracking |
| "Calculate imbalance costs for my portfolio" | eptr2-imbalance-costs |
| "What APIs are available for market data?" | eptr2-api-discovery |

## Skill Details

### eptr2-price-analysis

Covers:
- Market Clearing Price (MCP/PTF)
- System Marginal Price (SMP/SMF)
- Weighted Average Price (WAP/AOF)
- Intraday market prices
- Price comparisons and spreads

Example queries:
- "What was the average MCP for July 2024?"
- "Compare PTF and SMF for the last week"
- "Show hourly price distribution"

### eptr2-consumption-data

Covers:
- Real-time consumption
- Settlement consumption (UECM)
- Load plan forecasts
- Consumption patterns

Example queries:
- "What's the current electricity consumption?"
- "Compare forecast vs actual consumption"
- "Show consumption trends by hour"

### eptr2-generation-tracking

Covers:
- Real-time generation by source
- Settlement generation (UEVM)
- Renewable energy output
- Plant-level production

Example queries:
- "How much solar generation right now?"
- "Show wind generation for the past month"
- "What's the generation mix?"

### eptr2-imbalance-costs

Covers:
- Imbalance price calculations
- KUPST (deviation costs)
- Energy surplus/deficit penalties
- DSG tolerance calculations

Example queries:
- "Calculate imbalance cost for 100 MWh deficit"
- "What's the KUPST for yesterday?"
- "Explain imbalance pricing mechanism"

### eptr2-market-operations

Covers:
- Day-Ahead Market (GÖP) operations
- Intraday Market (GİP) trading
- Balancing Power Market (DGP)
- Order books and volumes

Example queries:
- "Show GÖP clearing quantities"
- "What's the GİP trading volume today?"
- "Explain YAL and YAT instructions"

### eptr2-api-discovery

Covers:
- Finding available endpoints
- Understanding API categories
- Parameter requirements
- Call aliases

Example queries:
- "What APIs are available for price data?"
- "How do I get power plant information?"
- "List all consumption-related endpoints"

## Installing Skills

The skills ship inside the pip package — no repository clone needed:

```bash
pip install eptr2
eptr2 install-skills                 # into ./.claude/skills (project)
eptr2 install-skills --dest user     # into ~/.claude/skills
eptr2 install-skills --dest PATH     # anywhere your agent runtime looks for skills
eptr2 install-skills --list          # see what's bundled
```

## Skill Files Location

Inside the package the canonical copies live under `eptr2/assets/skills/`; the repository keeps a synced copy in `.claude/skills/` for repo-local use:

```
eptr2/assets/skills/
├── eptr2-api-discovery/         # SKILL.md + endpoint reference + script
├── eptr2-consumption-data/
├── eptr2-convenience-wrappers/
├── eptr2-generation-tracking/
├── eptr2-imbalance-costs/       # SKILL.md + examples + formulas
├── eptr2-market-operations/
└── eptr2-price-analysis/
```

## Creating Custom Skills

You can create custom skills for your specific use cases:

1. Create a directory in your runtime's skills location (e.g. `.claude/skills/`)
2. Add a `SKILL.md` file with:
   - Skill description
   - Trigger keywords
   - Domain knowledge
   - Example patterns

Example structure:

```markdown
# My Custom Skill

## Description
This skill helps with [specific use case].

## Triggers
- keyword1
- keyword2

## Knowledge
[Domain-specific information]

## Examples
- "Example query 1" → [Expected behavior]
- "Example query 2" → [Expected behavior]
```

## Best Practices

1. **Be specific** - Detailed queries trigger more accurate skill matching
2. **Use Turkish terms** - Skills recognize both English and Turkish terminology
3. **Combine skills** - Complex queries may utilize multiple skills
4. **Iterate** - Follow up with clarifying questions for best results

## Next Steps

- [MCP Server Setup](mcp-server.md)
- [MCP Client Setup](mcp-clients.md)
- [CLI for Agents](cli.md)
