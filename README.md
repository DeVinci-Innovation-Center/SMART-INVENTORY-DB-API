# SMART-INVENTORY-DB-API

## Deployment
 1. Download the docker-compose.yml file and edit it to fit your needs :
 ```
 curl -OL https://raw.githubusercontent.com/DeVinci-Innovation-Center/SMART-INVENTORY-DB-API/main/docker-compose.yml
 ```
 2. From the same directory, start the API and DB with :
 ```
 docker-compose up
 ```
## Entity-Relationship Diagram

![ERD](Docs/SI_ERD_Diagram.png)

## Relational Schema
**users** (<ins>uid</ins>, firstname, lastname)

**cabinets** (<ins>id</ins>, description)

**categories** (<ins>id</ins>, title, description, #parent_id)

**items** (<ins>id</ins>, title, description, price, link, #category_id)

**orders_requests** (<ins>id</ins>, date, state, #item_id, #user_id)

**storage_units** (<ins>id</ins>, state, verified, #item_id, #cabinet_id)

**cabinets_unlock_attempts** (<ins>id</ins>, date, granted, #user_id, #cabinet_id) 
