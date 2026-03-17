# question_bank.py
# ------------------------------------------------
# All quiz questions about Real Estate - Property Listings
# Each question has: id, topic, difficulty, question text,
# 4 options (A-D), correct answer key, and a brief hint
# for the LLM to use when generating explanations.
# ------------------------------------------------

QUESTIONS = [
    # ── MLS & LISTING BASICS ──────────────────────────────────────────────
    {
        "id": 1,
        "topic": "MLS & Listing Basics",
        "difficulty": "beginner",
        "question": "What does MLS stand for in real estate?",
        "options": {
            "A": "Multiple Listing Service",
            "B": "Market Listing System",
            "C": "Managed Listing Service",
            "D": "Multiple Leasing Standard"
        },
        "correct": "A",
        "hint": "MLS is a cooperative database agents use to share listing data with each other."
    },
    {
        "id": 2,
        "topic": "MLS & Listing Basics",
        "difficulty": "beginner",
        "question": "Which of the following is typically NOT included in a standard MLS property listing?",
        "options": {
            "A": "Square footage",
            "B": "Number of bedrooms",
            "C": "Seller's mortgage balance",
            "D": "Year built"
        },
        "correct": "C",
        "hint": "The seller's mortgage balance is private financial information and is not disclosed in MLS listings."
    },
    {
        "id": 3,
        "topic": "MLS & Listing Basics",
        "difficulty": "intermediate",
        "question": "What is the term for the period a property has been available on the market?",
        "options": {
            "A": "Listing Age",
            "B": "Days on Market (DOM)",
            "C": "Market Exposure Period",
            "D": "Active Listing Duration"
        },
        "correct": "B",
        "hint": "DOM is a key metric — a high DOM can signal overpricing or issues with the property."
    },
    {
        "id": 4,
        "topic": "MLS & Listing Basics",
        "difficulty": "intermediate",
        "question": "A property listed as 'contingent' means:",
        "options": {
            "A": "The property has been sold",
            "B": "An offer has been accepted but conditions must be met",
            "C": "The property is available for backup offers only",
            "D": "The listing has expired"
        },
        "correct": "B",
        "hint": "Common contingencies include home inspection, financing approval, and appraisal."
    },

    # ── LISTING AGREEMENTS ────────────────────────────────────────────────
    {
        "id": 5,
        "topic": "Listing Agreements",
        "difficulty": "beginner",
        "question": "Which listing agreement gives ONE broker the exclusive right to earn a commission regardless of who sells the property?",
        "options": {
            "A": "Open listing",
            "B": "Exclusive agency listing",
            "C": "Exclusive right-to-sell listing",
            "D": "Net listing"
        },
        "correct": "C",
        "hint": "Even if the seller finds the buyer themselves, the broker still earns a commission under this agreement."
    },
    {
        "id": 6,
        "topic": "Listing Agreements",
        "difficulty": "intermediate",
        "question": "Under an 'Open Listing' agreement, who earns the commission?",
        "options": {
            "A": "The listing broker always",
            "B": "Only the seller's attorney",
            "C": "The broker who procures the buyer",
            "D": "Both the listing and buyer's broker equally"
        },
        "correct": "C",
        "hint": "Open listings are non-exclusive — multiple brokers can compete, but only the one who brings the buyer gets paid."
    },
    {
        "id": 7,
        "topic": "Listing Agreements",
        "difficulty": "advanced",
        "question": "A 'Net Listing' is considered unethical and illegal in many states primarily because:",
        "options": {
            "A": "It requires the seller to pay both sides of the commission",
            "B": "It creates a conflict of interest where the agent benefits from a higher sale price",
            "C": "It prevents the property from being listed on MLS",
            "D": "It ties the commission to the appraisal value"
        },
        "correct": "B",
        "hint": "In a net listing, the agent keeps everything above a set minimum — incentivizing them to inflate the price."
    },

    # ── PROPERTY VALUATION ────────────────────────────────────────────────
    {
        "id": 8,
        "topic": "Property Valuation",
        "difficulty": "beginner",
        "question": "What is a 'Comparative Market Analysis' (CMA) used for?",
        "options": {
            "A": "Calculating property taxes",
            "B": "Estimating a property's market value using recent similar sales",
            "C": "Determining construction costs",
            "D": "Evaluating the neighborhood crime rate"
        },
        "correct": "B",
        "hint": "Agents use CMAs (not formal appraisals) to help sellers price their home competitively."
    },
    {
        "id": 9,
        "topic": "Property Valuation",
        "difficulty": "intermediate",
        "question": "Properties used in a CMA are called:",
        "options": {
            "A": "Benchmarks",
            "B": "Comparables or 'comps'",
            "C": "Reference properties",
            "D": "Anchor listings"
        },
        "correct": "B",
        "hint": "Comps should be similar in size, location, age, and condition — ideally sold within the last 3-6 months."
    },
    {
        "id": 10,
        "topic": "Property Valuation",
        "difficulty": "advanced",
        "question": "When a property appraises BELOW the agreed purchase price, what typically happens?",
        "options": {
            "A": "The sale automatically cancels",
            "B": "The buyer must pay the full purchase price in cash",
            "C": "The buyer, seller, or both must renegotiate, or the buyer can walk away if there's an appraisal contingency",
            "D": "The lender automatically approves the full loan amount"
        },
        "correct": "C",
        "hint": "Lenders will only loan based on the appraised value — a low appraisal creates a 'gap' the deal must bridge."
    },

    # ── DISCLOSURES ───────────────────────────────────────────────────────
    {
        "id": 11,
        "topic": "Disclosures",
        "difficulty": "beginner",
        "question": "A seller disclosure statement primarily protects:",
        "options": {
            "A": "The listing agent from lawsuits",
            "B": "Both the buyer (from hidden defects) and the seller (from future claims)",
            "C": "Only the buyer",
            "D": "The mortgage lender"
        },
        "correct": "B",
        "hint": "Disclosure creates a documented record that the buyer was informed of known issues before purchase."
    },
    {
        "id": 12,
        "topic": "Disclosures",
        "difficulty": "intermediate",
        "question": "Which federal law requires sellers to disclose known lead-based paint hazards in homes built before 1978?",
        "options": {
            "A": "The Fair Housing Act",
            "B": "RESPA",
            "C": "The Residential Lead-Based Paint Hazard Reduction Act",
            "D": "The Clean Air Act"
        },
        "correct": "C",
        "hint": "This law also requires buyers to be given an EPA pamphlet and a 10-day period to conduct lead inspections."
    },
    {
        "id": 13,
        "topic": "Disclosures",
        "difficulty": "advanced",
        "question": "Which of these typically does NOT need to be disclosed by a seller?",
        "options": {
            "A": "Roof leaks repaired 2 years ago",
            "B": "A death that occurred in the property (in most states)",
            "C": "Active termite infestation",
            "D": "Foundation cracks"
        },
        "correct": "B",
        "hint": "Disclosure laws vary by state — most states do not require sellers to disclose deaths, though some do."
    },

    # ── LISTING PRICE & STRATEGY ──────────────────────────────────────────
    {
        "id": 14,
        "topic": "Listing Price & Strategy",
        "difficulty": "beginner",
        "question": "What is 'overpricing' a listing most likely to cause?",
        "options": {
            "A": "Faster sale with a higher profit",
            "B": "Property sitting on market longer, eventually selling for less",
            "C": "Immediate multiple offers",
            "D": "Automatic reduction in property taxes"
        },
        "correct": "B",
        "hint": "Overpriced listings accumulate DOM (Days on Market), making buyers suspicious something is wrong."
    },
    {
        "id": 15,
        "topic": "Listing Price & Strategy",
        "difficulty": "intermediate",
        "question": "What does 'price per square foot' primarily help buyers and agents do?",
        "options": {
            "A": "Calculate mortgage payments",
            "B": "Compare the relative value of different-sized properties in the same area",
            "C": "Determine property tax rates",
            "D": "Estimate renovation costs"
        },
        "correct": "B",
        "hint": "Price/sqft normalizes size differences — a 1,000 sqft home at $300k and a 2,000 sqft at $500k have very different values per sqft."
    },
    {
        "id": 16,
        "topic": "Listing Price & Strategy",
        "difficulty": "advanced",
        "question": "A seller receives multiple offers above asking price. What is the agent's ethical obligation?",
        "options": {
            "A": "Accept the highest offer immediately",
            "B": "Present all offers to the seller and let the seller decide",
            "C": "Only present the first offer received",
            "D": "Negotiate with buyers without telling the seller"
        },
        "correct": "B",
        "hint": "Agents have a fiduciary duty to present all offers — withholding offers is a serious ethical and legal violation."
    },

    # ── PROPERTY TYPES & ZONING ───────────────────────────────────────────
    {
        "id": 17,
        "topic": "Property Types & Zoning",
        "difficulty": "beginner",
        "question": "What does 'single-family residential' zoning typically mean?",
        "options": {
            "A": "Only one person can live in the home",
            "B": "The land is zoned for one detached dwelling unit",
            "C": "The home cannot be sold to families with children",
            "D": "The property must be owner-occupied"
        },
        "correct": "B",
        "hint": "Zoning refers to land use regulations — single-family zones restrict building multi-unit structures."
    },
    {
        "id": 18,
        "topic": "Property Types & Zoning",
        "difficulty": "intermediate",
        "question": "What is an 'easement' on a property listing?",
        "options": {
            "A": "A discount offered to first-time buyers",
            "B": "A legal right for someone else to use part of the property for a specific purpose",
            "C": "A type of home warranty",
            "D": "A clause allowing the seller to stay after closing"
        },
        "correct": "B",
        "hint": "Common easements include utility easements (wires/pipes) and right-of-way for neighboring properties."
    },

    # ── LISTING DESCRIPTIONS & MARKETING ──────────────────────────────────
    {
        "id": 19,
        "topic": "Listing Descriptions & Marketing",
        "difficulty": "beginner",
        "question": "Which phrase in a listing description is most likely to violate Fair Housing laws?",
        "options": {
            "A": "\"Newly renovated kitchen\"",
            "B": "\"Perfect for families with children\"",
            "C": "\"Hardwood floors throughout\"",
            "D": "\"Walking distance to shops\""
        },
        "correct": "B",
        "hint": "Fair Housing prohibits marketing that shows preference for or against any protected class, including families/children."
    },
    {
        "id": 20,
        "topic": "Listing Descriptions & Marketing",
        "difficulty": "intermediate",
        "question": "In listing photos, staging a home primarily aims to:",
        "options": {
            "A": "Hide structural defects from buyers",
            "B": "Help buyers emotionally connect with the space and visualize living there",
            "C": "Increase the official appraised value",
            "D": "Satisfy MLS photo requirements"
        },
        "correct": "B",
        "hint": "Studies show staged homes sell faster and often for more — the goal is emotional resonance, not deception."
    },
]

TOPICS = list(set(q["topic"] for q in QUESTIONS))
DIFFICULTIES = ["beginner", "intermediate", "advanced"]
