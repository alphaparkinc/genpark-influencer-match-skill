# genpark-influencer-match-skill

> **GenPark AI Agent Skill** — Match products with optimal influencer profiles based on category, audience fit, engagement rate, and ROI estimation.

## Features

- Category-based influencer pool (beauty, fitness, tech, food, fashion)
- Goal-weighted scoring: awareness, conversions, engagement, traffic
- Influencer tier classification (Nano/Micro/Mid/Macro/Mega)
- ROI estimation per influencer (reach, engagements, conversions, CPC)
- Budget allocation recommendations by tier
- Auto-generated campaign brief for outreach

## Quick Start

```python
from client import InfluencerMatchClient

client = InfluencerMatchClient()
result = client.match(
    product_category="beauty",
    budget_usd=5000,
    campaign_goal="conversions",
    top_n=5,
)
for m in result["matches"]:
    print(f"{m['handle']} | Fit: {m['fit_score']} | Est. Conversions: {m['estimated_roi']['estimated_conversions']}")
print(result["campaign_brief"])
```

## Installation

```bash
python example_usage.py  # No external dependencies
```

---
Built by [GenPark](https://genpark.ai) | [alphaparkinc](https://github.com/alphaparkinc)
