from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


engine = create_engine("mysql+pymysql://restoran:csdigital@mysql:3306/restoran", connect_args={'unix_socket': None})
Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()