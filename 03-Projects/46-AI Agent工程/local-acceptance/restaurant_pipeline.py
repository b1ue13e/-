"""Local teaching equivalent for Berkeley Lab 01; not official starter code."""

from dataclasses import dataclass
from statistics import fmean


@dataclass(frozen=True)
class Review:
    restaurant: str
    text: str
    score: float


def select_reviews(reviews: list[Review], restaurant: str) -> list[Review]:
    target = restaurant.strip().casefold()
    if not target:
        raise ValueError("restaurant cannot be empty")
    return [review for review in reviews if review.restaurant.casefold() == target]


def aggregate_score(reviews: list[Review]) -> float | None:
    if not reviews:
        return None
    if any(not 1.0 <= review.score <= 5.0 for review in reviews):
        raise ValueError("score must be within [1, 5]")
    return round(fmean(review.score for review in reviews), 2)


def run_pipeline(reviews: list[Review], restaurant: str) -> dict[str, object]:
    evidence = select_reviews(reviews, restaurant)
    return {
        "restaurant": restaurant.strip(),
        "evidence_count": len(evidence),
        "score": aggregate_score(evidence),
        "status": "ok" if evidence else "no_evidence",
    }

