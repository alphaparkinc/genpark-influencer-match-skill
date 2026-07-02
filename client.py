"""
influencer-match-skill: Client SDK
Match products with optimal influencer profiles based on category,
audience fit, engagement rate, and ROI estimation.
"""

from __future__ import annotations
import random
import math
from typing import Literal, Optional

Platform = Literal["instagram", "tiktok", "youtube", "twitter", "all"]
Goal = Literal["awareness", "conversions", "engagement", "traffic"]

INFLUENCER_POOL = {
    "beauty": [
        {"handle": "@glowwithsarah", "platform": "instagram", "followers": 450000, "engagement": 0.042, "niche": "skincare", "avg_cost_usd": 3500},
        {"handle": "@makeupbymia", "platform": "tiktok", "followers": 1200000, "engagement": 0.089, "niche": "makeup tutorials", "avg_cost_usd": 8000},
        {"handle": "@skincarescience", "platform": "youtube", "followers": 320000, "engagement": 0.031, "niche": "dermatology", "avg_cost_usd": 4000},
        {"handle": "@beautywithlena", "platform": "instagram", "followers": 85000, "engagement": 0.068, "niche": "clean beauty", "avg_cost_usd": 800},
    ],
    "fitness": [
        {"handle": "@fitwithmark", "platform": "instagram", "followers": 620000, "engagement": 0.038, "niche": "strength training", "avg_cost_usd": 5000},
        {"handle": "@yogawithjess", "platform": "youtube", "followers": 890000, "engagement": 0.025, "niche": "yoga & wellness", "avg_cost_usd": 6500},
        {"handle": "@runningpro", "platform": "tiktok", "followers": 340000, "engagement": 0.071, "niche": "running", "avg_cost_usd": 2200},
        {"handle": "@nutritionbytom", "platform": "instagram", "followers": 110000, "engagement": 0.055, "niche": "sports nutrition", "avg_cost_usd": 1100},
    ],
    "tech": [
        {"handle": "@techreviewshub", "platform": "youtube", "followers": 2100000, "engagement": 0.028, "niche": "gadget reviews", "avg_cost_usd": 15000},
        {"handle": "@productivitypro", "platform": "twitter", "followers": 180000, "engagement": 0.019, "niche": "productivity tools", "avg_cost_usd": 900},
        {"handle": "@gadgetguru", "platform": "tiktok", "followers": 560000, "engagement": 0.062, "niche": "unboxing", "avg_cost_usd": 3800},
        {"handle": "@devdiary", "platform": "instagram", "followers": 75000, "engagement": 0.044, "niche": "software & apps", "avg_cost_usd": 700},
    ],
    "food": [
        {"handle": "@chefsarah", "platform": "instagram", "followers": 390000, "engagement": 0.051, "niche": "home cooking", "avg_cost_usd": 3000},
        {"handle": "@foodtraveldiaries", "platform": "tiktok", "followers": 870000, "engagement": 0.077, "niche": "food travel", "avg_cost_usd": 6000},
        {"handle": "@healthybites", "platform": "youtube", "followers": 450000, "engagement": 0.033, "niche": "healthy eating", "avg_cost_usd": 3500},
    ],
    "fashion": [
        {"handle": "@stylewithalex", "platform": "instagram", "followers": 720000, "engagement": 0.039, "niche": "streetwear", "avg_cost_usd": 6000},
        {"handle": "@luxurylooks", "platform": "tiktok", "followers": 290000, "engagement": 0.058, "niche": "luxury fashion", "avg_cost_usd": 2000},
        {"handle": "@sustainablestyle", "platform": "instagram", "followers": 130000, "engagement": 0.062, "niche": "eco fashion", "avg_cost_usd": 1200},
    ],
}

GOAL_WEIGHTS = {
    "awareness":   {"followers": 0.50, "engagement": 0.20, "cost_efficiency": 0.30},
    "conversions": {"followers": 0.20, "engagement": 0.50, "cost_efficiency": 0.30},
    "engagement":  {"followers": 0.15, "engagement": 0.65, "cost_efficiency": 0.20},
    "traffic":     {"followers": 0.35, "engagement": 0.35, "cost_efficiency": 0.30},
}

TIER_MAP = [
    ("Nano",  0,      10000,   0.10),
    ("Micro", 10000,  100000,  0.25),
    ("Mid",   100000, 500000,  0.35),
    ("Macro", 500000, 2000000, 0.20),
    ("Mega",  2000000, 99999999, 0.10),
]


class InfluencerMatchClient:
    """
    SDK for matching products with optimal influencer profiles.
    Scores influencers on follower count, engagement rate, and cost efficiency
    weighted by campaign goal. Estimates ROI and generates outreach briefs.
    """

    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)

    def match(
        self,
        product_category: str,
        budget_usd: float,
        campaign_goal: Goal = "conversions",
        platform: Platform = "all",
        target_audience: Optional[dict] = None,
        top_n: int = 5,
    ) -> dict:
        """
        Match a product with influencer profiles.

        Args:
            product_category:  Product category string.
            budget_usd:        Total campaign budget in USD.
            campaign_goal:     Primary goal (awareness/conversions/engagement/traffic).
            platform:          Platform filter or "all".
            target_audience:   Optional dict with age_range, gender, interests.
            top_n:             Number of top matches to return.

        Returns:
            dict with: matches, budget_allocation, campaign_brief
        """
        category = product_category.lower()
        pool = INFLUENCER_POOL.get(category, list(INFLUENCER_POOL.values())[0])

        # Filter by platform
        if platform != "all":
            pool = [i for i in pool if i["platform"] == platform] or pool

        # Score and rank
        weights = GOAL_WEIGHTS.get(campaign_goal, GOAL_WEIGHTS["conversions"])
        scored = []
        for inf in pool:
            if inf["avg_cost_usd"] > budget_usd:
                continue
            score = self._score_influencer(inf, weights, budget_usd)
            roi = self._estimate_roi(inf, campaign_goal, budget_usd)
            tier = self._get_tier(inf["followers"])
            scored.append({
                "handle": inf["handle"],
                "platform": inf["platform"],
                "niche": inf["niche"],
                "followers": inf["followers"],
                "engagement_rate": round(inf["engagement"] * 100, 2),
                "estimated_cost_usd": inf["avg_cost_usd"],
                "tier": tier,
                "fit_score": score,
                "estimated_roi": roi,
            })

        scored.sort(key=lambda x: x["fit_score"], reverse=True)
        matches = scored[:top_n]

        budget_allocation = self._allocate_budget(budget_usd, campaign_goal)
        brief = self._generate_brief(product_category, campaign_goal, budget_usd, matches)

        return {
            "matches": matches,
            "budget_allocation": budget_allocation,
            "campaign_brief": brief,
        }

    def _score_influencer(self, inf: dict, weights: dict, budget: float) -> float:
        max_followers = 2000000
        f_score = min(inf["followers"] / max_followers, 1.0)
        e_score = min(inf["engagement"] / 0.10, 1.0)
        cost_ratio = 1 - (inf["avg_cost_usd"] / budget)
        c_score = max(0, cost_ratio)
        raw = (weights["followers"] * f_score +
               weights["engagement"] * e_score +
               weights["cost_efficiency"] * c_score)
        return round(raw + random.uniform(-0.02, 0.02), 3)

    def _estimate_roi(self, inf: dict, goal: str, budget: float) -> dict:
        reach = int(inf["followers"] * 0.25)
        engagements = int(inf["followers"] * inf["engagement"])
        if goal == "conversions":
            conv_rate = 0.015
        elif goal == "awareness":
            conv_rate = 0.003
        elif goal == "traffic":
            conv_rate = 0.008
        else:
            conv_rate = 0.01
        conversions = int(reach * conv_rate)
        cost_per_conversion = round(inf["avg_cost_usd"] / max(conversions, 1), 2)
        return {
            "estimated_reach": reach,
            "estimated_engagements": engagements,
            "estimated_conversions": conversions,
            "cost_per_conversion_usd": cost_per_conversion,
        }

    @staticmethod
    def _get_tier(followers: int) -> str:
        for name, low, high, _ in TIER_MAP:
            if low <= followers < high:
                return f"{name} Influencer"
        return "Mega Influencer"

    @staticmethod
    def _allocate_budget(budget: float, goal: str) -> dict:
        if goal == "awareness":
            splits = {"Macro/Mega": 0.60, "Mid-tier": 0.30, "Micro/Nano": 0.10}
        elif goal == "conversions":
            splits = {"Micro/Nano": 0.50, "Mid-tier": 0.35, "Macro/Mega": 0.15}
        elif goal == "engagement":
            splits = {"Micro/Nano": 0.45, "Mid-tier": 0.40, "Macro/Mega": 0.15}
        else:  # traffic
            splits = {"Mid-tier": 0.50, "Micro/Nano": 0.30, "Macro/Mega": 0.20}
        return {tier: round(budget * pct, 2) for tier, pct in splits.items()}

    @staticmethod
    def _generate_brief(category: str, goal: str, budget: float, matches: list) -> str:
        handles = ", ".join(m["handle"] for m in matches[:3])
        return f"""INFLUENCER CAMPAIGN BRIEF
========================
Category:  {category.title()}
Goal:      {goal.title()}
Budget:    ${budget:,.0f} USD

Top Recommended Partners: {handles}

Campaign Objectives:
  - Drive {goal} through authentic content partnerships
  - Leverage niche audience alignment for {category} products
  - Prioritize creators with high engagement rates

Content Guidelines:
  - Authentic product demonstrations preferred over hard selling
  - Clear FTC disclosure: #ad or #sponsored
  - Include trackable link or promo code per creator
  - 1-3 posts per creator across 2-week window

KPIs to Track:
  - Reach and impressions
  - Engagement rate (likes, comments, shares)
  - Click-through rate
  - Conversion/promo code redemptions
"""
