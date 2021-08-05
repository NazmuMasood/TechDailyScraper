from sqlalchemy import create_engine, select

# engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/techdaily', connect_args={"init_command": "SET SESSION time_zone='+00:00'"}, echo=True)
engine = create_engine('postgresql+psycopg2://postgres:@127.0.0.1:5432/techdailyapi', connect_args={"options": "-c timezone=utc"}, echo=True)

api_root_url = 'https://techdailyapi.herokuapp.com/'
# api_root_url = 'http://127.0.0.1:8000'