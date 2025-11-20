# Django Marketplace Project 🚀

A full-featured Django REST API for a marketplace platform with users, offers, orders, profiles, and reviews, supporting role-based permissions, filtering, search, and token authentication.

## Features ✨

   - Authentication: Token-based login/registration for customers and business users.
   - Offers: CRUD operations, nested offer details (basic, standard, premium), filtering, ordering, pagination.
   - Orders: Customers can order offers, track status (in_progress, completed, cancelled), and count endpoints for business.
   - Profiles: Separate customer and business profiles with editable fields.
   - Reviews: Customers can rate and review businesses (1–5 stars), prevent duplicate reviews, full CRUD with permissions.
   - Permissions: Role-based and object-level (owner) permissions.

## Tech Stack 🛠️

   - Python 3.11+
   - Django 4.x
   - Django REST Framework
   - SQLite/PostgreSQL (configurable)
   - Token authentication via DRF

## Quick Start ⚡

1. Clone the repository
```bash
git clone https://github.com/Takoua852/Coderr.git
cd Coderr
```

2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows
```

3. Install dependencies 
```bash
pip install -r requirements.txt
```
    
4. Apply migrations
```bash
python manage.py migrate
```

5. Create superuser
```bash
python manage.py createsuperuser
```
6. Run server
```bash
python manage.py runserver
```

## API Endpoints 📦
   
   ### Authentication
   - POST /api/registration/ – Register a user
   - POST /api/login/ – Login and receive token
   
   ### Offers
   - GET/POST /api/offers/ – List or create offers
   - GET/PUT/PATCH/DELETE /api/offers/<id>/ – Offer detail
   - GET /api/offerdetails/<id>/ – Offer detail info

   ### Orders
   - GET/POST /api/orders/ – List or create orders
   - GET/PATCH/DELETE /api/orders/<id>/ – Order detail
   - GET /api/order-count/<business_user_id>/ – In-progress order count
   - GET /api/completed-order-count/<business_user_id>/ – Completed order count

   ### Profiles
   - GET/PATCH /api/profile/<id>/ – Retrieve or update profile
   - GET /api/profiles/<type>/ – List profiles by type (customer or business)

   ### Reviews

   - GET/POST /api/reviews/ – List or create reviews
   - GET/PATCH/PUT/DELETE /api/reviews/<id>/ – Review detail

## Folder Structure 📂
```bash
project/
├─ auth_app/        # User auth & custom user model
├─ offers_app/      # Offers & offer details
├─ orders_app/      # Orders management
├─ profiles_app/    # Profiles
├─ reviews_app/     # Reviews & ratings
├─ core/         # Django settings
└─ manage.py
```

## 📜 License

This project is licensed under the [MIT License](LICENSE).








      
