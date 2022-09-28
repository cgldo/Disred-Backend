from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

Base = declarative_base()


class PostModel(Base):
    __tablename__ = 'post_table'
 
    id = Column(Integer, primary_key = True)
    title = Column(String)
    author =  Column(String)
    body = Column(String)
    imgUrl = Column(String)
    tags = Column(String)
    
    def __repr__(self):
        return f"{self.title}:{self.author}:{self.body}:{self.imgUrl}:{self.tags}"

class CommentModel(Base):
    __tablename__ = 'comment_table'
 
    id = Column(Integer, primary_key = True)
    author =  Column(String())
    body = Column(String())
    tags = Column(String())
    post_id = Column(ForeignKey(PostModel.id))
 
    def __repr__(self):
        return f"{self.author}:{self.body}:{self.tags}"