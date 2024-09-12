class DevelopmentConfig:
  SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:password@localhost/factory_management_db'
  CACHE_TYPE = 'SimpleCache'
  DEBUG = True