from sqlalchemy import *
from config.db import Base
from sqlalchemy.orm import relationship
from auth.models import User
from sqlalchemy.orm import backref


class Journal(Base):
    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    title = Column(String(50), unique=True)
    description = Column(String(500))
    publish_time = Column(DATETIME)

    file_path = Column(String(500))

    teacher_id = Column(Integer, ForeignKey(User.id), nullable=False)
    teacher = relationship(User, backref= backref('journals', lazy = True) )

    def __str__(self):
        return f"{self.title}"
    
class Tags(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)

    journal_id = Column(Integer, ForeignKey(Journal.id), nullable=False)
    journal = relationship(Journal, backref= backref('tags', lazy = True) )

    student_id = Column(Integer, ForeignKey(User.id), nullable=False)
    student = relationship(User, backref= backref('tags', lazy = True) )
    
    def __str__(self):
        return f"{self.tag}"