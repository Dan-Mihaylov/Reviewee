# Reviewee App Documentation
![alt Python](https://www.vectorlogo.zone/logos/python/python-ar21.svg)  ![alt Django](https://www.vectorlogo.zone/logos/djangoproject/djangoproject-ar21.svg)  ![alt Postgres](https://www.vectorlogo.zone/logos/postgresql/postgresql-ar21.svg) <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/celery.png" width=60px/>  ![alt redis](https://www.vectorlogo.zone/logos/redis/redis-ar21.svg)  ![alt Html](https://www.vectorlogo.zone/logos/w3_html5/w3_html5-icon.svg)  <img src='https://www.vectorlogo.zone/logos/w3_css/w3_css-official.svg' width=80px />  ![alt Bootstrap](https://www.vectorlogo.zone/logos/getbootstrap/getbootstrap-icon.svg)    <img src="https://raw.githubusercontent.com/simple-icons/simple-icons/master/icons/mailtrap.svg" width=70px  /> <img src="https://www.vectorlogo.zone/logos/docker/docker-official.svg"  width=80px/>

## Table of content

- [Installation and Setup](#installation)
- [Desktop screenshots](#web-screenshots)
- [Mobile Screenshots](#mobile-screenshots)
- [Summary](#summary)
- [Resources](#resources)

## Overview
The Reviewee App is a Django-based web application designed for creating different businesses, reviewing and creating reservations for those businesses and viewing the reservations of your business, currently the place types available to add, review and book are Hotels and Restaurants.  
  
There are three types of users, regular users, business owners and admins.  
  
Regular users can:
- [x] Edit / Delete their profile / change password
- [x] Add / Remove businesses to their favourites
- [x] Add / Remove / Edit a review to a business
- [x] Add / Remove a vote for a helpfull review

Business Owners can:
- [x] All regular users functionality
- [x] Edit their business information - *they have to be a registered business so they can't delete this information*
- [x] Create / Edit / Delete Restaurants or Hotels
- [x] View the Restaurant / Hotel reservations

## Base Requirements
- Compatable Python version
- Celery
- Redis
- Internet connection (for Bootstrap and JQuery to load)

### Additional Requirements for Running as Is:
- Docker
- Configured Email Backend

## Installation and Setup <a name="installation"><a/>

### 1. Clone the Repository
```bash
git clone https://github.com/Dan-Mihaylov/Reviewee.git
```
### 2. Create a virtual environment
windows  
```
python -m venv venv
```
### 3. Activate the virtual environment
```
.\venv\Sripts\Activate
```
### 4. Install requirements
```
pip install -r requirements.txt
```
### 5. Create .venv file and edit Database and Email backend configurations  
#### In the .venv file you will need to include a variable called DJANGO_SECRET_KEY and let the cat walk throuth the keyboard a couple of times
If you would like to use my configurations you will have to have an account with mailtrap and just configure your api key
You will have to change the database conf because I am using an unorthodox port. Apologies.

### 6. Migrate
```
python manage.py migrate
```

### 6.1 Optional run Redis and Celery to be able to send async email confirmations for each reservation
If you would like to have the full functionality of the web app, you will have to configure your email backend and run Celery and Redis.
- Run the services in the docker-compose.yml file
```
docker-compose up -d
```
- Run Celery worker
```
celery -A reviewee_app worker --loglevel=info
```
*celery has stopped supporting windows in recent years and there is a known issue with tasks being received but not executed ( [Article source](https://celery.school/celery-on-windows) ). If that happens you can use command*
```
celery -A reviewee_app worker --pool=threads --loglevel=info
```
### 7. Create superuser
Create a superuser to be able to:
- view admin page
- create user groups / perhaps review moderators
- give permissions to users
  *The defauls username field is the Email field*
```
python manage.py createsuperuser
```
### 8. Runserver
```
python manage.py runserver
```
You should now have a working app, create users, add places, explore the functionality.

## Screenshots from the application <a name="web-screenshots"><a/>

### ERD Diagram

![alt ERD](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/ERD_diagram.png)  

### Login Page  
![alt Login](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/login_page.png)
  
### Home Page  

![alt Home Page](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/home_page.png)

![alt Home Page](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/home_page_latest_places.png)

### Favourite Places  
![alt Favourite](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/favourite_places_page.png)


### Find Your Reservation Page
You can look for a reservation by email address or by the confirmation code, you recieve after creating the reservation  
In order to manage your reservation, you will have to confirm you are the owner, by submitting the confirmation code.  

![alt Find Booking](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/find_your_reservation_page.png)  

### View Your Places Reservations Page  
![alt Your place reservations](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/manage_place_bookings.png)  


### Place Details Review Page  
![alt Place Details Reviews](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/place_details_reviews.png)  


### Write Edit Reviews Page  
![alt Write Edit Review](https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/write_edit_review_page.png)  


## Screenshots from a mobile device <a name="mobile-screenshots"><a/>  


### Login and Home Page
<img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/login.png" width=300px /> <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/home_page.png" width=300px />


### Profile Information Page
<img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/profile_info.png" width=300px /> <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/business_profile_info.png" width=300px /> <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/my_places.png" width=300px/>

### My Places Booking Page
<img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/places_bookings_1.png" width=300px/> <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/places_bookings_2.png" width=300px/>  


### Place Details and Reviews Page
<img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/place_info.png" width=300px/> <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/photo_reviews.png" width=300px/> <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/reviews.png" width=300px/>


### Create Reservation and Reservation Confirmation Page

<img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/booking_page.png" width=300px/> <img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/booking_confirmation_page.png" width=300px/>


### Confirmation Email
<img src="https://github.com/Dan-Mihaylov/Reviewee/blob/main/screenshots/mobile/booking_confirmation.png" width=300px/>


# Project Summary

## Things I Learned <a name="summary"> <a/>

### Django ORM (Object-Relational Mapping)
- [x] Understanding how Django ORM maps Python objects to database tables.
- [x] Performing CRUD operations using Django ORM.

### Models and Model Relationships
- [x] Creating models to represent database tables.
- [x] Establishing relationships between models (OneToOne, ForeignKey, ManyToMany).
- [x] Utilizing model fields and attributes to define database schema.

### User Model Customization
- [x] Overriding the default Django User model to meet project requirements.
- [x] Extending User model with additional fields and functionalities.

### Model-View-Template (MVT) Architecture
- [x] Grasping the concept of MVT architecture in Django.
- [x] Implementing views and templates to handle user requests and render responses.

### Views and Templates
- [x] Creating views to process HTTP requests and generate responses.
- [x] Utilizing Django templates to render dynamic HTML content.

### Custom Forms
- [x] Designing custom forms using Django's Form class.
- [x] Validating form data and handling form submissions.

### Class-Based Views (CBVs) and Function-Based Views (FBVs)
- [x] Working with both CBVs and FBVs to define view logic.
- [x] Understanding the advantages and disadvantages of each approach.

### Django Template Language
- [x] Learning the syntax and features of Django template language.
- [x] Incorporating template tags and filters to manipulate data in templates.

### Custom Template Tags and Filters
- [x] Creating custom template tags and filters to extend template functionality.
- [x] Enhancing template rendering with custom logic and processing.

### HTML and CSS
- [x] Utilizing HTML and CSS to design and style frontend components.
- [x] Creating responsive layouts and enhancing user experience.

### Celery and Redis
- [x] Implementing Celery for asynchronous task processing.
- [x] Setting up Redis as a message broker for Celery.

### Sending Emails Programmatically
- [x] Configuring Django to send emails programmatically.
- [x] Designing email templates and sending messages to users.

### Mixins
- [x] Using Mixins to encapsulate reusable code and behavior.
- [x] Enhancing view classes with Mixins for modularity and flexibility.

### Permission Control
- [x] Implementing permission control to restrict access to views and resources.
- [x] Defining custom permissions and enforcing authorization rules.

### Session Management
- [x] Working with Django session framework to manage user sessions.
- [x] Storing and retrieving session data securely.

### Django Unit Testing
- [x] Writing unit tests to ensure the correctness of Django applications.
- [x] Using Django's built-in testing framework to create and run tests.

## Conclusion
Throughout the development of this project, I gained valuable insights into various aspects of Django framework and web development. From database modeling to frontend design, from user authentication to asynchronous task processing, I tackled a wide range of challenges and honed my skills along the way. By leveraging Django's powerful features and adhering to best practices, I was able to deliver a robust and scalable application that meets the project requirements. Moving forward, I look forward to applying the knowledge and experience gained from this project to future endeavors in software development.

## Resources Used <a name="resources"><a/>
- [Django Documentation](https://docs.djangoproject.com/en/5.0/) - Official Django Documentation
- [Stackoverflow](https://stackoverflow.com/) - Help from programmers with bugs and issues
- [Icon8](https://icons8.com/) - low resolution free tier pngs
- [Pexels](https://www.pexels.com/) - Free non copyrighted photos you can use anywhere
- [ChatGPT](https://chat.openai.com/)  - AI Language Model
- [Dall-E 3](https://openai.com/dall-e-3) - Image generating AI helped with Profile Pictures
- [Mailtrap](https://mailtrap.io/) - Email delivering platform
- [SoftUni](https://softuni.bg/) - Lectures and learning materials
- [And More](https://upload.wikimedia.org/wikipedia/commons/c/c8/More_and_More.png) - More free resources
  
