# -*- coding: utf-8 -*-

#TODO: créer un fichier meta.py

#from config import DATABASE
from sqlalchemy import create_engine, MetaData
from sqlalchemy.interfaces import PoolListener
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker
import web


# Définition d'une classe de base (pseudo DAO)
class Base(object):
    
    @classmethod
    def all(cls, order_by_clause = None):
        
        # Fabrication de la query
        query = orm.query(cls)
        
        # Ajout de l'éventuel tri à la requête
        if order_by_clause is not None :
            query = query.order_by(order_by_clause)
        
        # Exécution de la requête
        return query.all()
    
    @classmethod
    def get(cls, id):
        return orm.query(cls).get(id)    

        

# Définition d'un listener de connexion
class ConnListener(PoolListener):
    
    def connect(self, dbapi_con, con_record):
        pass # print "[CONN_LISTENER] Entrée dans connect de %s"  % dbapi_con

    def checkin(self, dbapi_con, con_record):
        pass # print "[CONN_LISTENER] Entrée dans checkin de %s" % dbapi_con
    
    def checkout(self, dbapi_con, con_record, con_proxy):
        pass # print "[CONN_LISTENER] Entrée dans checkout de %s" % dbapi_con
    
    def first_connect(self, dbapi_con, con_record):
        pass # print "[CONN_LISTENER] Entrée dans first_connect de %s" % dbapi_con


# Création d'une sesion "globale"
__sessionmaker = sessionmaker()

# Initialisation de la session
orm = scoped_session(__sessionmaker)

# Paramétrage de la session par les clients
def init_sqlalchemy_session(dsn, echo = True):
    
    # engine = create_engine(dsn, echo = echo, listeners=[ConnListener()])
    engine = create_engine(dsn, echo = echo)
    __sessionmaker.configure(bind = engine)
    web.debug("[MODEL] Armement OK de l'engine BDD avec la DSN %s" %dsn)
    return engine
    

# Binding du metadata global
metadata = MetaData()

# Import différé des enfants pour être accessible via le paquetage models
# Attention aux imports croisés !
from app.models.users import User
from app.models.comments import Comment
from app.models.results import Result
from app.models.tournaments import Tournament
from app.models.seasons import Season
from app.models.sessions import Session


