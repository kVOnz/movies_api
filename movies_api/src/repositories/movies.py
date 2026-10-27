from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.movie import Movie
from src.schemas.movie import MovieCreate, MovieUpdate

async def create_movie(session: AsyncSession, movie_data: MovieCreate) -> Movie:
    new_movie = Movie(**movie_data.model_dump())
    session.add(new_movie)
    await session.commit()
    await session.refresh(new_movie)

    return new_movie

async def get_movie_by_id(session: AsyncSession, movie_id: int) -> Movie | None:
    return await session.get(Movie, movie_id)

async def get_all_movies(session: AsyncSession, limit: int = 10, offset: int = 0) -> list[Movie]:
    query = select(Movie).limit(limit).offset(offset)

    result = await session.execute(query)
    return result.scalars().all() # type: ignore

async def update_movie(session: AsyncSession, movie_id: int, movie_data: MovieUpdate) -> Movie | None:
    movie = await session.get(Movie, movie_id)
    if not movie:
        return None
    
    update_data = movie_data.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(movie, field, value)
        
    await session.commit()
    await session.refresh(movie)
    
    return movie

async def delete_movie(session: AsyncSession, movie_id: int) -> bool:
    movie = await session.get(Movie, movie_id)
    if not movie:
        return False

    await session.delete(movie)
    await session.commit()

    return True
