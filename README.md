# Library

Description:
Library project includes 2 micro-services: 
* library store - here users can see books, authors, and publishing houses, after authorization they can choose some books and add them to the client's cart, after adding customer's info (email, phone number, etc) they can create an order. Here, in store, client's order will be saved in order story and sent to the warehouse by API, using Celery async task.
* library warehouse - here employees can add books, authors, genres, publishing houses and book instances. At midnight library store will send API requst to library warehouse, by Celery task and sync databases. Also, employees can work with orders, after getting order here in warehouse, they check, are books in stock, or not and send mail about order.

Using Docker I configured PGadmin, Mailhog, Celery, RabbitMQ, Redis caching, Nginx.
