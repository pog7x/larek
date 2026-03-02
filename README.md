<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="staticfiles/assets/img/logo-light.svg">
    <source media="(prefers-color-scheme: light)" srcset="staticfiles/assets/img/logo.svg">
    <img src="staticfiles/assets/img/logo.svg" alt="Larek Logo" width="340">
  </picture>
  <p><strong>Open-source Django marketplace — from catalog to checkout</strong></p>
  <p>
    <img src="https://img.shields.io/badge/Python-3.13-blue?logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Django-6.0-green?logo=django&logoColor=white" alt="Django">
    <img src="https://img.shields.io/badge/PostgreSQL-14-blue?logo=postgresql&logoColor=white" alt="PostgreSQL">
    <img src="https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker&logoColor=white" alt="Docker">
    <img src="https://img.shields.io/badge/HTMX-1.27-orange" alt="HTMX">
    <img src="https://img.shields.io/badge/Celery-5.6-brightgreen?logo=celery&logoColor=white" alt="Celery">
  </p>
</div>

---

## What is Larek?

Larek is a full-featured marketplace web application built with Django. It covers the complete e-commerce flow — product discovery, cart management, order placement, and async payment processing — all in a server-rendered architecture powered by HTMX for snappy, SPA-like interactions without a separate frontend.

---

## Features

- **Product catalog** — filter by price range, category, and availability; sort by popularity, rating, newest, and price; paginated results
- **Multi-seller support** — each product can have multiple sellers with independent prices and stock levels
- **Shopping cart** — add, update, and remove items with real-time header/total updates via HTMX
- **Order & payment flow** — atomic order creation, UUID-keyed payments, and async payment confirmation via Celery
- **Browsing history** — tracks per-user product views and uses them for popularity ranking
- **User accounts** — registration, login, profile editing (avatar, phone, address), password change and reset
- **Reviews** — authenticated users can leave reviews on products
- **Banners** — homepage slider with configurable promotional sections (limited offers, popular goods, limited edition)
- **Admin panel** — full Django admin for managing all entities

---

## Tech Stack

| Layer            | Technology                            |
| ---------------- | ------------------------------------- |
| Backend          | Django 6.0, Python 3.13               |
| Database         | PostgreSQL 14                         |
| Async tasks      | Celery 5.6 + RabbitMQ 3.11            |
| Frontend         | HTMX, Bootstrap 5, Swiper, noUiSlider |
| Static files     | WhiteNoise                            |
| Containerization | Docker + Docker Compose               |

---

## Quick Start

**Prerequisites:** Docker & Docker Compose installed.

```bash
# Clone the repository
git clone https://github.com/your-username/larek.git
cd larek

# Start all services (app, PostgreSQL, RabbitMQ)
docker-compose up --build
```

The app will be available at [http://localhost:8000](http://localhost:8000).

To load sample data:

```bash
docker-compose exec app python manage.py loaddata fixtures/sample
```

---

## Development

### Make migrations

```bash
python manage.py makemigrations user --no-header && python manage.py makemigrations --no-header
```

### Clear all migrations

```bash
python clear_migrations.py
```

### Dump database to fixtures

```bash
python manage.py dumpdata banner cart catalog_category delivery order payment product product_seller review seller user views_history \
  --format json --indent 4 --verbosity 1 \
  -o fixtures/sample.json \
  -e admin
```

---

## Project Structure

```
larek/
├── larek/
│   ├── apps/
│   │   ├── banner/          # Homepage banners
│   │   ├── cart/            # Cart management
│   │   ├── catalog_category/# Product categories
│   │   ├── delivery/        # Delivery options
│   │   ├── discount/        # Discounts (WIP)
│   │   ├── order/           # Order management
│   │   ├── payment/         # Async payment processing
│   │   ├── product/         # Product catalog & images
│   │   ├── product_seller/  # Seller-product pricing
│   │   ├── review/          # Product reviews
│   │   ├── seller/          # Seller profiles
│   │   ├── user/            # Custom user model
│   │   └── views_history/   # Browsing history & popularity
│   ├── settings.py
│   └── urls.py
├── templates/
├── staticfiles/
├── docker-compose.yml
└── requirements.txt
```

---

If Larek saves you time or sparks ideas, consider leaving a star. It helps a lot.
