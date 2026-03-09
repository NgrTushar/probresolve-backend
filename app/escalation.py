"""
Domain slug → escalation portals.
Each entry: (portal_name, url, one_line_description)
Slugs match what python-slugify generates from seed.py domain names.
"""

from typing import TypeAlias

EscalationEntry: TypeAlias = tuple[str, str, str]

ESCALATION_MAP: dict[str, list[EscalationEntry]] = {
    "e-commerce-online-shopping": [
        (
            "National Consumer Helpline",
            "https://consumerhelpline.gov.in",
            "Call 1800-11-4000 (toll-free) or file online complaint",
        ),
        (
            "eDaakhil — Consumer Forum",
            "https://edaakhil.nic.in",
            "File a formal case with the District Consumer Forum",
        ),
        (
            "Cyber Crime Portal",
            "https://cybercrime.gov.in",
            "Report online fraud, phishing, and financial crimes",
        ),
    ],
    "banking-financial-services": [
        (
            "RBI Ombudsman (CMS)",
            "https://cms.rbi.org.in",
            "Complaint Management System for banking and NBFC grievances",
        ),
        (
            "NPCI Dispute Resolution",
            "https://www.npci.org.in/what-we-do/upi/dispute-redressal-mechanism",
            "Raise UPI / IMPS payment disputes with NPCI",
        ),
        (
            "Cyber Crime Portal",
            "https://cybercrime.gov.in",
            "Report financial fraud — also call 1930 (National Cyber Crime Helpline)",
        ),
    ],
    "real-estate-housing": [
        (
            "RERA — Your State Portal",
            "https://rera.gov.in",
            "Find your state RERA authority and file a complaint against builders",
        ),
        (
            "National Consumer Helpline",
            "https://consumerhelpline.gov.in",
            "Call 1800-11-4000 or file online for builder / broker disputes",
        ),
        (
            "eDaakhil — Consumer Forum",
            "https://edaakhil.nic.in",
            "File a formal consumer complaint for possession delays or defects",
        ),
    ],
    "government-services": [
        (
            "RTI Online",
            "https://rtionline.gov.in",
            "File a Right to Information request to get answers from any government body",
        ),
        (
            "CPGRAMS (PM Portal)",
            "https://pgportal.gov.in",
            "Centralised Public Grievance Redress — complaints against central govt depts",
        ),
        (
            "National Consumer Helpline",
            "https://consumerhelpline.gov.in",
            "For public utility complaints (electricity, water, etc.)",
        ),
    ],
    "healthcare-pharmaceuticals": [
        (
            "National Medical Commission",
            "https://www.nmc.org.in",
            "Complaints against registered medical practitioners",
        ),
        (
            "CDSCO — Drug Complaint",
            "https://cdscoonline.gov.in/CDSCO/Drugs",
            "Report fake, substandard, or spurious medicines to the Central Drugs authority",
        ),
        (
            "National Consumer Helpline",
            "https://consumerhelpline.gov.in",
            "For medical overcharging and hospital service complaints",
        ),
    ],
    "education-recruitment": [
        (
            "Cyber Crime Portal",
            "https://cybercrime.gov.in",
            "Report fake job offers, degree mills, and online recruitment fraud",
        ),
        (
            "Shram Suvidha — Labour Dept",
            "https://shramsuvidha.gov.in",
            "Grievances related to employment, wages, and labour law violations",
        ),
        (
            "National Consumer Helpline",
            "https://consumerhelpline.gov.in",
            "For coaching / tuition fraud and misleading admission offers",
        ),
    ],
    "telecom-internet": [
        (
            "TRAI",
            "https://www.trai.gov.in/consumer-corner/complaint",
            "Complaints against telecom operators for service quality and billing",
        ),
        (
            "SANCHAR SAATHI — DoT",
            "https://sancharsaathi.gov.in",
            "Report SIM fraud, lost/stolen phone blocking, and fake calls",
        ),
        (
            "Cyber Crime Portal",
            "https://cybercrime.gov.in",
            "Report SIM swap fraud, OTP theft, and data privacy breaches",
        ),
    ],
    "consumer-goods-services": [
        (
            "National Consumer Helpline",
            "https://consumerhelpline.gov.in",
            "Call 1800-11-4000 for defective products, misleading ads, warranty issues",
        ),
        (
            "eDaakhil — Consumer Forum",
            "https://edaakhil.nic.in",
            "File a formal consumer case for compensation",
        ),
        (
            "FSSAI — Food Safety",
            "https://foscos.fssai.gov.in",
            "Report food safety violations and adulterated food products",
        ),
    ],
}

FALLBACK_ESCALATION: list[EscalationEntry] = [
    (
        "National Consumer Helpline",
        "https://consumerhelpline.gov.in",
        "Call 1800-11-4000 (toll-free) or file an online complaint",
    ),
    (
        "Cyber Crime Portal",
        "https://cybercrime.gov.in",
        "Report online fraud — call 1930 (National Cyber Crime Helpline)",
    ),
]
