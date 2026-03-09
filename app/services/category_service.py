import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Category, Domain


async def get_all_domains(db: AsyncSession) -> list[Domain]:
    result = await db.execute(select(Domain).order_by(Domain.name))
    return list(result.scalars().all())


async def get_categories_for_domain(db: AsyncSession, domain_id: uuid.UUID) -> list[Category]:
    result = await db.execute(
        select(Category)
        .where(Category.domain_id == domain_id)
        .order_by(Category.name)
    )
    return list(result.scalars().all())
