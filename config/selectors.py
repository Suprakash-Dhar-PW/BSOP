LINKEDIN_SELECTORS = {
    # The main container for each person in search results
    "candidate_card": [
        "[role='listitem']",
        ".reusable-search__result-container",
        ".entity-result__item"
    ],

    # The name of the candidate
    "name": [
        ".entity-result__title-text a span[aria-hidden='true']",
        "a[href*='/in/'] span[aria-hidden='true']",
        "a[href*='/in/']",
        ".entity-result__title-text"
    ],
    # Their professional headline
    "headline": [
        ".entity-result__primary-subtitle",
        "div.entity-result__primary-subtitle",
        "p.entity-result__primary-subtitle",
        "div:has(> p > span)"
    ],
    # Their location
    "location": [
        ".entity-result__secondary-subtitle",
        "div.entity-result__secondary-subtitle"
    ],
    # Link to their full profile
    "profile_link": [
        "a.app-aware-link",
        "a[href*='/in/']",
        ".entity-result__title-text a"
    ],
    # NOISE REDUCTION
    "promoted_badge": [".entity-result__badge", ".ad-badge"],
    "loading_skeleton": [".artdeco-skeleton", ".skeleton-container"]
}

