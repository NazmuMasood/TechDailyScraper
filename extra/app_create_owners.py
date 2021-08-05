from dtos import OwnerDto
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import Column, ForeignKey, Sequence
from sqlalchemy.sql.sqltypes import DateTime, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker
from bs4 import BeautifulSoup
from models import Owner, Content
from connection import engine
import json
import requests
from connection import api_root_url

### Db connection
# engine = create_engine('mysql+mysqldb://root:@127.0.0.1:3306/techdaily', connect_args={"init_command": "SET SESSION time_zone='+00:00'"}, echo=True)
# engine = create_engine('postgresql+psycopg2://postgres:@127.0.0.1:5432/techdaily', connect_args={"options": "-c timezone=utc"})
# Base.metadata.create_all(bind=engine)

### Creating session to make db queries
# Session = sessionmaker(bind=engine)
# session = Session()

### ----- session code for that particular session goes here -----

# --------!!!!!------ Populating techdaily_owner table -------!!!!!!!!!--------
owner_names = ['Cnet','Beebom', 'Android Authority']
owner_urls = ['https://www.cnet.com', 'https://beebom.com', 'https://www.androidauthority.com']
# for owner_name, owner_url in zip(owner_names, owner_urls):
#     owner = Owner()
#     owner.name = owner_name
#     owner.url = owner_url
#     session.add(owner)
# session.commit()
# session.close()

ownerDtos = []
for owner_name, owner_url in zip(owner_names, owner_urls):
    ownerDto = OwnerDto(name=owner_name, url=owner_url)
    ownerDtos.append(ownerDto)

json_payload = json.dumps([obj.__dict__ for obj in ownerDtos])
# print('\nJSON to send:\n'+json_payload)

if len(ownerDtos)>0:
    headers = {
        'Content-Type': 'application/json'
    }
    url = api_root_url+'owners/createAll/'
    response = requests.request("POST", url, headers=headers, data=json_payload)
    
    print("JSON response:\n"+response.text)
    owners = json.loads(response.text)
    print('\n'+str(len(owners))+' owner(s) successfully created via API')
    # for owner in owners:
    #     print(owner['id'])
    #     print(owner['url']+'\n')
