from datetime import datetime

import click
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

from pgsync.base import create_database, pg_engine
from pgsync.helper import teardown
from pgsync.utils import config_loader, get_config

Base = declarative_base()


class Users(Base):
    __tablename__ = "users"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False)


class Projects(Base):
    __tablename__ = "projects"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    slug = sa.Column(sa.String, nullable=False)
    description = sa.Column(sa.String, nullable=True)
    created_at = sa.Column(sa.DateTime, nullable=False)


class UsersProjects(Base):
    __tablename__ = "users_projects"
    project_id = sa.Column(sa.Integer, sa.ForeignKey(Projects.id), primary_key=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey(Users.id), primary_key=True)
    user = sa.orm.relationship(Users, backref=sa.orm.backref("users"))
    project = sa.orm.relationship(Projects, backref=sa.orm.backref("projects"))


class Hashtags(Base):
    __tablename__ = "hashtags"
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, nullable=False)
   


class ProjectsHashtags(Base):
    __tablename__ = "projects_hashtags"
    hashtag_id = sa.Column(sa.Integer, sa.ForeignKey(Hashtags.id), primary_key=True)
    project_id = sa.Column(sa.Integer, sa.ForeignKey(Projects.id), primary_key=True)
    project = sa.orm.relationship(Projects,  backref=sa.orm.backref("projects"),)
    hashtag = sa.orm.relationship(Hashtags, backref=sa.orm.backref("hashtags"))
    


def setup(config: str) -> None:
    for document in config_loader(config):
        database: str = document.get("database", document["index"])
        create_database(database)
        with pg_engine(database) as engine:
            Base.metadata.drop_all(engine)
            Base.metadata.create_all(engine)


@click.command()
@click.option(
    "--config",
    "-c",
    help="Schema config",
    type=click.Path(exists=True),
)
def main(config):
    config: str = get_config(config)
    teardown(config=config)
    setup(config)


if __name__ == "__main__":
    main()
