from sqlalchemy import Integer, String, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

import config

engine = create_async_engine(config.PG_DSN_ALC, echo=True)
Base = declarative_base()
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


class People(Base):

    __tablename__ = 'peoples'

    id = Column(Integer, primary_key=True)
    birth_year = Column(String(15))
    eye_color = Column(String(15))
    films = Column(String(200))
    gender = Column(String(15))
    hair_color = Column(String(30))
    height = Column(String(5))
    homeworld = Column(String(50))
    mass = Column(String(10))
    name = Column(String(50), index=True)
    skin_color = Column(String(30))
    species = Column(String(200))
    starships = Column(String(200))
    vehicles = Column(String(200))


async def get_async_session(
    drop: bool = False, create: bool = False
):

    async with engine.begin() as conn:
        if drop:
            await conn.run_sync(Base.metadata.drop_all)
        if create:
            print('create table')
            await conn.run_sync(Base.metadata.create_all)
    async_session_maker = sessionmaker(
        engine, expire_on_commit=False, class_=AsyncSession
    )

    return async_session_maker


async def save_people_in_db(people):
    async with Session() as session:
        async with session.begin():
            # for people in people_data:
            birth_year = people['birth_year']
            eye_color = people['eye_color']
            films = ",".join(people['films'])
            gender = people['gender']
            hair_color = people['hair_color']
            height = people['height']
            homeworld = people['homeworld']
            mass = people['mass']
            name = people['name']
            skin_color = people['skin_color']
            species = ",".join(people['species'])
            starships = ",".join(people['starships'])
            vehicles = ",".join(people['vehicles'])
            people = People(birth_year=birth_year,
                            eye_color=eye_color,
                            films=films,
                            gender=gender,
                            hair_color=hair_color,
                            height=height,
                            homeworld=homeworld,
                            mass=mass,
                            name=name,
                            skin_color=skin_color,
                            species=species,
                            starships=starships,
                            vehicles=vehicles
                            )
            session.add(people)
