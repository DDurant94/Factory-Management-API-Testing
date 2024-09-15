from flask import Flask
from database import db
from schema import ma
from limiter import limiter
from caching import cache
from flask_cors import CORS

from models.customer import Customer
from models.order import Order
from models.product import Product
from models.employee import Employee
from models.production import Production
from models.orderProduct import OrderProducts
from models.role import Role
from models.userManagementRole import UserManagementRole
from models.user import User

from routes.customerBP import customer_blueprint
from routes.orderBP import order_blueprint
from routes.productBP import product_blueprint
from routes.employeeBP import employee_blueprint
from routes.productionBP import production_blueprint
from routes.rolesBP import role_blueprint
from routes.userBP import user_blueprint

def create_app(config_name):
  app = Flask(__name__)
  
  app.config.from_object(f'config.{config_name}')
  db.init_app(app)
  ma.init_app(app)
  cache.init_app(app)
  limiter.init_app(app)
  CORS(app)
  
  return app


def blue_print_config(app):
  app.register_blueprint(customer_blueprint, url_prefix='/customers')
  app.register_blueprint(order_blueprint,url_prefix='/orders')
  app.register_blueprint(product_blueprint,url_prefix='/products')
  app.register_blueprint(employee_blueprint,url_prefix='/employees')
  app.register_blueprint(production_blueprint,url_prefix='/production')
  app.register_blueprint(role_blueprint,url_prefix='/roles')
  app.register_blueprint(user_blueprint,url_prefix='/users')

def configure_rate_limit():
  limiter.limit("5000/minute")(customer_blueprint)
  limiter.limit("10000/second")(product_blueprint)
  limiter.limit("10000/second")(order_blueprint)
  limiter.limit("300/minute")(employee_blueprint)
  limiter.limit("20/minute")(production_blueprint)

if __name__ == '__main__':
  app = create_app('DevelopmentConfig')
  
  blue_print_config(app)
  configure_rate_limit()
  
  with app.app_context():  
    db.create_all()
    
  app.run(debug=True)