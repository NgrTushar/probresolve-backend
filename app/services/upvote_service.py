import hashlib
import uuid

from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Problem, Upvote


def compute_fingerprint(ip: str, user_agent: str) -> str:
    raw = f"{ip}:{user_agent}"
    return hashlib.sha256(raw.encode()).hexdigest()[:64]


async def has_voted(db: AsyncSession, problem_id: uuid.UUID, fingerprint: str) -> bool:
    result = await db.execute(
        select(Upvote).where(
            Upvote.problem_id == problem_id,
            Upvote.fingerprint == fingerprint,
        )
    )
    return result.scalar_one_or_none() is not None


async def _get_upvote_count(db: AsyncSession, problem_id: uuid.UUID) -> int:
    result = await db.execute(select(Problem.upvote_count).where(Problem.id == problem_id))
    return result.scalar_one_or_none() or 0


async def upvote(
    db: AsyncSession, problem_id: uuid.UUID, fingerprint: str
) -> tuple[int, bool]:
    """Return (upvote_count, already_voted)."""
    already = await has_voted(db, problem_id, fingerprint)
    if already:
        return await _get_upvote_count(db, problem_id), True

    vote = Upvote(problem_id=problem_id, fingerprint=fingerprint)
    db.add(vote)
    try:
        await db.flush()
    except IntegrityError:
        await db.rollback()
        return await _get_upvote_count(db, problem_id), True

    await db.execute(
        update(Problem)
        .where(Problem.id == problem_id)
        .values(upvote_count=Problem.upvote_count + 1)
    )
    await db.commit()

    return await _get_upvote_count(db, problem_id), True  # vote was just cast — user has now voted
