# -*- coding: utf-8 -*-

from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
import web
from web import config

class SessionFactory(object):
    
    def __init__(self, engine_factory):
        self.engine_factory = engine_factory
        self.sessionmaker = sessionmaker()
    
    def __call__(self):
        engine = self.engine_factory()
        self.sessionmaker.configure(bind = engine)
        session = self.sessionmaker()
        # web.debug("[MODEL] Sucessfully instanciated DB session %s bound to %s" %(session, engine))
        return session
        
def init_orm(engine_factory):
    return scoped_session(SessionFactory(engine_factory))

def init_engine(dsn, echo):
    engine = create_engine(dsn, echo = echo)
    web.debug("[MODEL] Successfully instantiated DB engine (DSN = %s, echo = %s)" %(dsn, echo))
    return engine

# Global shared metadata
metadata = MetaData()

class Base(object):
    """ Parent of all model classes """
    
    @classmethod
    def all(cls, order_by_clause = None):
        
        # Fabrication de la query
        query = config.orm.query(cls)
        
        # Ajout de l'éventuel tri à la requête
        if order_by_clause is not None :
            query = query.order_by(order_by_clause)
        
        # Exécution de la requête
        return query.all()
    
    @classmethod
    def get(cls, id):
        return config.orm.query(cls).get(id)   