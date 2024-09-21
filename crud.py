import asyncio

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload, relationship

from core.models import User, db_helper, Profile, Post, Order, Product


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


async def users_with_posts(session: AsyncSession):
    statement = (
        select(User).options(selectinload(User.posts)).order_by(User.id)
    )  # selectinload используется при подключении 1 к многим ,нет необходимости использовать unique
    result: Result = await session.execute(
        statement
    )  # joinload используется при подключении 1 к 1 или 1 к многим,для избежания повторов необходим unique
    users = result.scalars()
    for user in users:
        print("**" * 10)
        print(user)
        for post in user.posts:
            print(post)


async def posts_with_authors(session: AsyncSession):
    statement = select(Post).options(joinedload(Post.user)).order_by(Post.user_id)
    posts = await session.scalars(statement)
    for post in posts:
        print("Post:", post)
        print("Author:", post.user)


async def get_users_with_posts_and_profiles(
    session: AsyncSession,
):
    stmt = (
        select(User)
        .options(
            joinedload(User.profile),
            selectinload(User.posts),
        )
        .order_by(User.id)
    )
    users = await session.scalars(stmt)

    for user in users:  # type: User
        print("**" * 10)
        print(user, user.profile and user.profile.first_name)
        for post in user.posts:
            print("-", post.title)


async def create_order(
    session: AsyncSession,
    promocode: str | None = None,
) -> Order:
    order = Order(promocode=promocode)

    session.add(order)
    await session.commit()

    return order


async def create_product(
    session: AsyncSession,
    name: str,
    description: str,
    price: int,
) -> Product:
    product = Product(
        name=name,
        description=description,
        price=price,
    )
    session.add(product)
    await session.commit()
    return product


async def demo_m2m(session: AsyncSession):
    order_one = await create_order(session)
    order_promo = await create_order(session, promocode="promo")

    mouse = await create_product(
        session,
        "Mouse",
        "Great gaming mouse",
        price=123,
    )
    keyboard = await create_product(
        session,
        "Keyboard",
        "Great gaming keyboard",
        price=149,
    )
    display = await create_product(
        session,
        "Display",
        "Office display",
        price=299,
    )

    order_one = await session.scalar(
        select(Order)
        .where(Order.id == order_one.id)
        .options(
            selectinload(Order.products),
        ),
    )
    order_promo = await session.scalar(
        select(Order)
        .where(Order.id == order_promo.id)
        .options(
            selectinload(Order.products),
        ),
    )

    order_one.products.append(mouse)
    order_one.products.append(keyboard)
    # order_promo.products.append(keyboard)
    # order_promo.products.append(display)

    order_promo.products = [keyboard, display]

    await session.commit()


# async def main_rel():
# async with db_helper.session_factory() as session:
#     # await create_new_user(session=session, username="jon")
#     # await create_new_user(session=session, username="Dima")
#     # user_jon = await get_user_by_username(session, "jon")
#     # user_jonk = await get_user_by_username(session, "jonk")
#     # await create_user_profile(
#     #     session=session,
#     #     user_id=3,
#     #     first_name="Dima",
#     #     last_name="Pilevich",
#     #     bio="I am ",
#     # )
#     # await create_user_profile(
#     #     session=session,
#     #     user_id=user_jon.id,
#     #     first_name="Jonk",
#     #     last_name="Die",
#     #     bio="I am man ",
#     # )
#     # await show_users_with_profiles(session=session)
#     #
#     # await create_posts(
#     #     session,
#     #     3,
#     #     "posgres",
#     # )
#     # await users_with_posts(session=session)
#     # await posts_with_authors(session=session)
#     await get_users_with_posts_and_profiles(session=session)


async def main():
    async with db_helper.session_factory() as session:
        await demo_m2m(session)


if __name__ == "__main__":
    asyncio.run(main())
