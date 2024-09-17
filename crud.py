import asyncio

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from core.models import User, db_helper, Profile, Post


async def create_new_user(session: AsyncSession, username: str) -> User:
    user = User(name=username)
    session.add(user)
    await session.commit()
    return user


async def get_user_by_username(session: AsyncSession, username: str) -> User | None:
    statement = select(User).where(User.name == username)
    # result: Result = await session.execute(statement)
    # user: User | None = result.scalar_one_or_none()
    user = await session.scalar(statement)
    print(user)
    return user


async def create_user_profile(
    session: AsyncSession,
    user_id: int,
    first_name: str | None = None,
    last_name: str | None = None,
    bio: str | None = None,
) -> Profile:
    profile = Profile(
        user_id=user_id, first_name=first_name, last_name=last_name, bio=bio
    )
    session.add(profile)
    await session.commit()
    return profile


async def show_users_with_profiles(session: AsyncSession):
    statement = select(User).options(joinedload(User.profile)).order_by(User.id)
    # result: Result = await session.execute(statement)
    # users = result.scalars().all()
    users = await session.scalars(statement)
    print(users)
    for user in users:
        print(user)


async def create_posts(session: AsyncSession, user_id: int, *posts_titles: str):
    posts = [Post(title=title, user_id=user_id) for title in posts_titles]
    session.add_all(posts)
    await session.commit()
    return posts


async def main():
    async with db_helper.session_factory() as session:
        # await create_new_user(session=session, username="jon")
        # await create_new_user(session=session, username="Dima")
        user_jon = await get_user_by_username(session, "jon")
        user_jonk = await get_user_by_username(session, "jonk")
        # await create_user_profile(
        #     session=session,
        #     user_id=3,
        #     first_name="Dima",
        #     last_name="Pilevich",
        #     bio="I am ",
        # )
        # await create_user_profile(
        #     session=session,
        #     user_id=user_jon.id,
        #     first_name="Jonk",
        #     last_name="Die",
        #     bio="I am man ",
        # )
        await show_users_with_profiles(session=session)

        await create_posts(
            session,
            user_jon.id,
            "SQLA 2.0",
            "SQLA Joins",
        )


if __name__ == "__main__":
    asyncio.run(main())
