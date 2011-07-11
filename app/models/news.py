# -*- coding: utf-8 -*-

from app.models.meta import metadata, Base
from sqlalchemy import Table, Column, Integer, Date, Text
from sqlalchemy.orm import mapper
from sqlalchemy.sql.expression import desc
import web


news_table = Table("NEWS", metadata,
                   Column("id", Integer, primary_key=True, nullable=False),
                   Column("news", Text, nullable=False),
                   Column("news_dt", Date, nullable=False)
                   )

class News(Base):
    """ Website announcements """
    
    @classmethod
    def all(cls):
        """ Overrides the default all method to guarantee the order by """
        return Base.all.im_func(News, order_by_clause=desc(News.news_dt)) #@UndefinedVariable

    
    def __repr__(self) : 
        return "<News(%s,%s)>" % (self.news, self.news_dt)


mapper(News, news_table)

web.debug("[MODEL] Successfully mapped News class")
