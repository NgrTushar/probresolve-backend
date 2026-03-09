import uuid

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Report


async def has_reported(db: AsyncSession, problem_id: uuid.UUID, fingerprint: str) -> bool:
    result = await db.execute(
        select(Report).where(
            Report.problem_id == problem_id,
            Report.fingerprint == fingerprint,
        )
    )
    return result.scalar_one_or_none() is not None


async def report_problem(
    db: AsyncSession,
    problem_id: uuid.UUID,
    fingerprint: str,
    reason: str,
) -> tuple[int, bool]:
    """Return (report_count, is_new). is_new=False if already reported."""
    already = await has_reported(db, problem_id, fingerprint)
    if already:
        result = await db.execute(
            select(func.count(Report.id)).where(Report.problem_id == problem_id)
        )
        return result.scalar_one() or 0, False

    report = Report(problem_id=problem_id, fingerprint=fingerprint, reason=reason)
    db.add(report)
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        result = await db.execute(
            select(func.count(Report.id)).where(Report.problem_id == problem_id)
        )
        return result.scalar_one() or 0, False

    await db.commit()
    result = await db.execute(
        select(func.count(Report.id)).where(Report.problem_id == problem_id)
    )
    return result.scalar_one() or 0, True
