"""Seed 6 safe domains, categories, and domain-scoped companies into the database."""

import asyncio

from slugify import slugify
from sqlalchemy import select

from app.database import AsyncSessionLocal
from app.models import Category, Domain, Company

DOMAINS: list[dict] = [
    {
        "name": "E-Commerce & Online Shopping",
        "icon": "🛒",
        "description": "Fraud and scams on online shopping platforms, fake sellers, and delivery issues.",
        "categories": [
            "Fake / Duplicate Product Received",
            "Damaged or Missing Items",
            "Delivery Delayed or Denied",
            "Refund or Return Refused",
            "Deceptive Pricing / Hidden Charges",
            "Warranty & Service Refusal",
            "Other",
        ],
        "companies": [
            "Amazon India", "Flipkart", "Meesho", "Myntra", "Ajio", "Nykaa", "Tata CLiQ",
            "Blinkit", "Zepto", "Swiggy Instamart", "JioMart", "Snapdeal", "FirstCry", "Croma",
            "Reliance Digital", "Reliance Smart", "BigBasket", "NNNOW", "Shopsy", "Purplle",
            "Lenskart", "Bewakoof", "Pepperfry", "Shopclues", "Ferns N Petals", "Hopscotch",
            "Decathlon", "Shoppers Stop",
        ],
    },
    {
        "name": "Consumer Goods & Services",
        "icon": "📦",
        "description": "Defective products, misleading advertisements, service fraud, and warranty issues.",
        "categories": [
            "Defective Hardware / Product",
            "Poor After-Sales Service or Repair",
            "Subscription or Membership Scam",
            "Misleading Advertising",
            "Food Safety & Hygiene Issues",
            "Unjustified Extra Charges",
            "Other",
        ],
        "companies": [
            "Samsung India", "LG Electronics", "Sony India", "Whirlpool", "Apple India",
            "Xiaomi", "OnePlus", "Boat", "Noise", "Realme", "Vivo", "Oppo", "Dell",
            "HP (Hewlett-Packard)", "Lenovo", "Acer", "Asus", "Urban Company", "JustDial",
            "Zomato", "Swiggy", "BookMyShow", "Paytm Insider", "Ticketmaster",
        ],
    },
    {
        "name": "Travel & Logistics",
        "icon": "✈️",
        "description": "Airline ticket issues, lost baggage, courier delays, missing parcels, and hotel/stay booking disputes.",
        "categories": [
            "Booking Cancelled or Denied at Venue",
            "Refund Refused for Cancellation",
            "Lost, Stolen, or Damaged Baggage/Parcel",
            "Misleading Amenities or Bait-and-Switch",
            "Unjustified Surge Pricing / Extortion",
            "Fake Travel Agent or Package Scam",
            "Other",
        ],
        "companies": [
            "IndiGo", "Air India", "SpiceJet", "Vistara", "Akasa Air", "Air India Express",
            "MakeMyTrip", "Goibibo", "Yatra", "Cleartrip", "EaseMyTrip", "Ixigo", "Oyo Rooms",
            "Agoda", "Booking.com", "Airbnb", "IRCTC", "RedBus", "AbhiBus", "Delhivery",
            "Blue Dart", "DTDC", "Ecom Express", "XpressBees", "Shadowfax",
            "India Post (Speed Post)",
        ],
    },
    {
        "name": "Education & Recruitment",
        "icon": "🎓",
        "description": "Fake institutes, degree mills, job scams, and recruitment fraud.",
        "categories": [
            "Fake Job or Placement Scam",
            "Deceptive Course Promises / Quality",
            "Non-Refundable Fee Scams",
            "Withheld Certificates / Extortion",
            "False Advertising / Fake Institute",
            "Freelance / Contractor Unpaid Dues",
            "Other",
        ],
        "companies": [
            "Byju's", "Unacademy", "Physics Wallah", "Vedantu", "UpGrad", "Simplilearn",
            "Udemy", "Coursera", "Allen Career Institute", "Aakash Educational Services",
            "FIITJEE", "Resonance", "Great Learning", "Scaler Academy", "Masai School",
            "Cuemath", "WhiteHat Jr", "LinkedIn (Recruitment Scams)", "Naukri.com", "Indeed",
            "Foundit (Monster)", "Shine.com", "Apna", "Internshala",
        ],
    },
    {
        "name": "Automobile & Transport",
        "icon": "🚗",
        "description": "Defective vehicles, service center fraud, fake spare parts, and vehicle insurance denied.",
        "categories": [
            "Defective Vehicle / Engine Failure",
            "Service Center Negligence or Extortion",
            "False Range / Mileage Claims (EVs)",
            "Driver Misbehavior or Harassment",
            "Insurance Claim Wrongly Denied",
            "Unsafe / Accident-Prone Vehicle",
            "Other",
        ],
        "companies": [
            "Maruti Suzuki", "Hyundai Motor India", "Tata Motors", "Mahindra & Mahindra",
            "Honda Cars India", "Toyota Kirloskar Motor", "Kia India", "Ola Electric",
            "Ather Energy", "Royal Enfield", "Hero MotoCorp",
            "Honda Motorcycle and Scooter India",
            "TVS Motor Company", "Bajaj Auto", "Skoda India", "Volkswagen India", "Uber",
            "Ola Cabs", "Rapido", "Porter", "Zoomcar", "Revv", "BluSmart", "InDrive",
        ],
    },
    {
        "name": "Other / Miscellaneous",
        "icon": "🌐",
        "description": "Any other complaints that do not fit into the primary verified domains.",
        "categories": [
            "Other",
        ],
        "companies": [],
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

            for company_name in domain_data.get("companies", []):
                result = await session.execute(
                    select(Company).where(Company.name.ilike(company_name))
                )
                company = result.scalar_one_or_none()
                if company:
                    if company.domain_id != domain.id:
                        company.domain_id = domain.id
                        print(f"      ~ Company updated: {company_name} → {domain.name}")
                    else:
                        print(f"      = Company exists: {company_name}")
                else:
                    company = Company(name=company_name, domain_id=domain.id)
                    session.add(company)
                    print(f"      + Company: {company_name}")

        await session.commit()
        print("\nSeeding complete.")


if __name__ == "__main__":
    asyncio.run(seed())
