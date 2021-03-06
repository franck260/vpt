# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, joinedload
from sqlalchemy.orm.session import sessionmaker
from web import config
import web

class SessionFactory(object):
    
    def __init__(self, engine_factory):
        self.engine_factory = engine_factory
        self.sessionmaker = sessionmaker()
    
    def __call__(self):
        engine = self.engine_factory()
        self.sessionmaker.configure(bind=engine)
        session = self.sessionmaker()
        web.debug("[MODEL] Successfully instanciated DB session %s bound to %s" %(session, engine))
        return session
        
def init_orm(engine_factory):
    return scoped_session(SessionFactory(engine_factory))

def init_engine(dsn, echo):
    engine = create_engine(dsn, echo=echo)
    web.debug("[MODEL] Successfully instantiated DB engine (DSN = %s, echo = %s)" %(dsn, echo))
    return engine

# Global shared metadata
metadata = MetaData()

class Base(object):
    """ Parent of all model classes """
    
    @classmethod
    def all(cls, order_by_clause=None, joined_attrs=[]):
        
        # Creation of the query
        query = config.orm.query(cls)

        for joined_attr in joined_attrs:
            query = query.options(joinedload(joined_attr))

        # Takes into account the optional order_by clause
        if order_by_clause is not None :
            query = query.order_by(order_by_clause)
        
        # Runs the query
        return query.all()
    
    @classmethod
    def get(cls, ident, joined_attrs=[]):
        
        query = config.orm.query(cls)
        
        for joined_attr in joined_attrs:
            query = query.options(joinedload(joined_attr))        
        
        return query.get(ident) 