from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func

Base = declarative_base()

### Owner model
class Owner(Base):
    __tablename__ = 'techdaily_owner'
    # id = Column(Integer, Sequence('owner_id_seq'), primary_key=True)
    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    url = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())
    # created_at = Column(DateTime(timezone=True), server_default=func.now())
    # updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return "<Owner(id='%d', name='%s', url='%s', created_at='%s', updated_at='%s')>" % ( 
            self.id, self.name, self.url, self.created_at, self.updated_at)

### Content model
class Content(Base):
    __tablename__ = 'techdaily_content'

    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey('techdaily_owner.id', ondelete="CASCADE"))
    url =  Column(String(300), nullable=False, unique=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=True)
    pub_date = Column(String(50), nullable=True)
    img_url = Column(String(200), nullable=True)   
    created_at = Column(DateTime(), default=func.now())
    updated_at = Column(DateTime(), default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return "<Content(id='%d', owner_id='%d', url='%s', title='%s', author='%s', pub_date='%s', img_url='%s', created_at='%s', updated_at='%s')>" % ( 
            self.id, self.owner_id, self.url, self.title, self.author, self.pub_date, self.img_url, self.created_at, self.updated_at)
