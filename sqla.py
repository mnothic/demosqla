from sqlalchemy import create_engine, Column, ForeignKey, Integer, String
from sqlalchemy.orm import sessionmaker, relationship, deferred
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Parent(Base):
    __tablename__ = 'parent'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    children = relationship("Child", backref="parent")

    def __init__(self, name):
        self.name = name


class Child(Base):
    __tablename__ = 'child'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column(Integer, ForeignKey('parent.id'))

    def __init__(self, name, pid):
        self.name = name
        self.parent_id = pid

if __name__ == '__main__':
    clean = False
    # print('::SQLAlchemy Demo meetup python BCN::')
    engine = create_engine('sqlite:///demo.db', echo=False)
    session = sessionmaker(bind=engine)()
    Base.metadata.create_all(engine, checkfirst=True)
    if clean:
        con = engine.connect()
        transaction = con.begin()
        for table in reversed(Base.metadata.sorted_tables):
            con.execute(table.delete())
        transaction.commit()

    p = Parent('prueba')
    session.add(p)
    session.commit()
    q = session.query(Parent).all()
    for x in q:
        c = Child("child", x.id)
        session.add(c)
    session.commit()
    session.refresh(p)
    for x in q:
        print("{}+\n      |".format(x.name))
        for i in x.children:
            print("      +-->{}".format(i.name))