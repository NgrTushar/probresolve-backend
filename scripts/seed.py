"""Seed 8 domains and 42 categories into the database."""

import asyncio

from slugify import slugify
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Category, Domain

DOMAINS: list[dict] = [
    {
        "name": "E-Commerce & Online Shopping",
        "icon": "🛒",
        "description": "Fraud and scams on online shopping platforms, fake sellers, and delivery issues.",
        "categories": [
            "Fake Product / Wrong Item Delivered",
            "Non-Delivery of Order",
            "Refund Not Processed",
            "Counterfeit / Duplicate Product",
            "Unauthorized Charges",
            "Seller Fraud",
        ],
    },
    {
        "name": "Banking & Financial Services",
        "icon": "🏦",
        "description": "Banking fraud, unauthorized transactions, loan scams, and insurance mis-selling.",
        "categories": [
            "Unauthorized Transaction",
            "Phishing / Account Takeover",
            "Loan Fraud / Predatory Lending",
            "Insurance Mis-selling",
            "Credit Card Fraud",
            "UPI / Mobile Payment Fraud",
        ],
    },
    {
        "name": "Real Estate & Housing",
        "icon": "🏠",
        "description": "Property fraud, builder defaults, rental scams, and land disputes.",
        "categories": [
            "Builder / Developer Fraud",
            "Rental Scam",
            "Land / Property Document Fraud",
            "Broker Fraud",
            "RERA Violation",
            "Possession Delay",
        ],
    },
    {
        "name": "Government Services",
        "icon": "🏛️",
        "description": "Corruption, bribery, impersonation of government officials, and service denial.",
        "categories": [
            "Bribery / Corruption",
            "Impersonation of Government Official",
            "Denial of Entitled Services",
            "Document Forgery",
            "Public Works Fraud",
            "Pension / Welfare Scheme Fraud",
        ],
    },
    {
        "name": "Healthcare & Pharmaceuticals",
        "icon": "🏥",
        "description": "Medical fraud, fake medicines, overcharging, and quackery.",
        "categories": [
            "Fake / Substandard Medicines",
            "Medical Overcharging",
            "Quackery / Unqualified Practitioner",
            "Insurance Claim Fraud",
            "Diagnostic Lab Fraud",
            "Misleading Health Products",
        ],
    },
    {
        "name": "Education & Recruitment",
        "icon": "🎓",
        "description": "Fake institutes, degree mills, job scams, and recruitment fraud.",
        "categories": [
            "Fake Job / Employment Offer",
            "Degree Mill / Fake Institute",
            "Coaching / Tuition Fraud",
            "Internship / Placement Scam",
            "Scholarship Fraud",
            "Immigration / Visa Job Scam",
        ],
    },
    {
        "name": "Telecom & Internet",
        "icon": "📱",
        "description": "SIM swap fraud, fake tech support, internet service issues, and OTT scams.",
        "categories": [
            "SIM Swap / Cloning",
            "Fake Tech Support",
            "Unwanted Subscription / VAS Charges",
            "Internet Service Provider Fraud",
            "OTT Platform Scam",
            "Data Privacy Breach",
        ],
    },
    {
        "name": "Consumer Goods & Services",
        "icon": "📦",
        "description": "Defective products, misleading advertisements, service fraud, and warranty issues.",
        "categories": [
            "Defective Product",
            "Misleading Advertisement",
            "Warranty / After-sales Service Fraud",
            "Subscription / Membership Fraud",
            "Food Safety Violation",
            "Travel & Hospitality Fraud",
        ],
    },
]


async def seed():
    async with AsyncSessionLocal() as session:
        for domain_data in DOMAINS:
            domain_slug = slugify(domain_data["name"])

            # Upsert domain
            result = await session.execute(select(Domain).where(Domain.slug == domain_slug))
            domain = result.scalar_one_or_none()

            if domain is None:
                domain = Domain(
                    name=domain_data["name"],
                    slug=domain_slug,
                    icon=domain_data["icon"],
                    description=domain_data["description"],
                )
                session.add(domain)
                await session.flush()  # get domain.id
                print(f"  + Domain: {domain.name}")
            else:
                print(f"  = Domain exists: {domain.name}")

            for cat_name in domain_data["categories"]:
                cat_slug = slugify(cat_name)
                result = await session.execute(
                    select(Category).where(
                        Category.domain_id == domain.id,
                        Category.slug == cat_slug,
                    )
                )
                cat = result.scalar_one_or_none()

                if cat is None:
                    cat = Category(domain_id=domain.id, name=cat_name, slug=cat_slug)
                    session.add(cat)
                    print(f"      + Category: {cat_name}")
                else:
                    print(f"      = Category exists: {cat_name}")

        await session.commit()
        print("\nSeeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
