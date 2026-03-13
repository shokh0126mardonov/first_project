# first_project

☀
TEXNIK TOPSHIRIQ
Quyosh Panellari Savdo Sayti
Backend Tizimi
Python / Django REST Framework
Hujjat turi
Texnik Topshiriq (TT)
Versiya
1.0
Sana
2025-yil
Platforma
Python 3.11+ / Django 4.2 / PostgreSQL
Holat
Tasdiqlash uchun tayyor



1. UMUMIY MA'LUMOT
1.1. Loyiha maqsadi
Ushbu texnik topshiriq quyosh panellari sotuvchi veb-sayt uchun backend tizimini ishlab chiqish bo'yicha barcha talablarni belgilaydi. Tizim uchta asosiy funksiyani ta'minlaydi:
Admin tomonidan quyosh paneli mahsulotlarini saytga qo'shish, tahrirlash va o'chirish
Ro'yxatdan o'tmagan mijozlarning so'rov (xabar) qoldirishi
Admin tomonidan mijozlar xabarlarini ko'rish va ularga javob berish

1.2. Ishtirokchilar
Rol
Vakolat
Tavsif
Super Admin
To'liq kirish
Tizimni boshqaradi, adminlarni yaratadi
Admin
Mahsulot + Xabarlar
Mahsulot va so'rovlarni boshqaradi
Mijoz (Anonim)
Faqat so'rov
Ro'yxatdan o'tmasdan so'rov qoldiradi


1.3. Texnologiyalar to'plami
Backend: Python 3.11+, Django 4.2, Django REST Framework 3.14
Ma'lumotlar bazasi: PostgreSQL 15
Autentifikatsiya: JWT (djangorestframework-simplejwt)
Rasm saqlash: Django Storages + AWS S3 yoki lokal media
API hujjatlash: drf-spectacular (OpenAPI 3.0 / Swagger UI)
Deploy: Docker + Gunicorn + Nginx
Cache: Redis (ixtiyoriy)

2. TIZIM ARXITEKTURASI
2.1. Umumiy arxitektura
Backend RESTful API arxitekturasida quriladi. Frontend (React yoki Vue) va backend to'liq ajratilgan holda ishlaydi. Barcha ma'lumot almashinuvi JSON formatida HTTP/HTTPS orqali amalga oshiriladi.

2.2. Django ilovalar tuzilmasi
solar_backend/
├── config/              # Loyiha sozlamalari
│   ├── settings/
│   │   ├── base.py      # Umumiy sozlamalar
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── accounts/        # Admin autentifikatsiya
│   ├── products/        # Quyosh paneli mahsulotlari
│   └── inquiries/       # Mijoz so'rovlari
├── media/               # Yuklangan rasmlar
└── static/


2.3. Ma'lumotlar bazasi diagrammasi (asosiy jadvallar)
User (accounts_user)
  id | username | email | password | role | is_active

Product (products_product)
  id | name | description | price | power_watt
  efficiency | warranty_years | image | is_active
  created_at | updated_at | created_by (FK: User)

ProductImage (products_productimage)
  id | product (FK) | image | order

Inquiry (inquiries_inquiry)
  id | full_name | phone | email (nullable)
  message | product (FK, nullable) | status
  admin_note | created_at | viewed_at | responded_at


3. AUTENTIFIKATSIYA VA RUXSATLAR
3.1. JWT autentifikatsiya
Admin paneliga kirish uchun JWT token ishlatiladi. Mijozlar autentifikatsiyasiz API ga murojaat qiladi.

3.2. Ruxsatlar matritsasi
Endpoint
Mijoz (Anonim)
Admin
Super Admin
GET /api/products/
Ha
Ha
Ha
GET /api/products/{id}/
Ha
Ha
Ha
POST /api/products/
Yo'q
Ha
Ha
PUT/PATCH /api/products/{id}/
Yo'q
Ha
Ha
DELETE /api/products/{id}/
Yo'q
Yo'q
Ha
POST /api/inquiries/
Ha
Ha
Ha
GET /api/inquiries/
Yo'q
Ha
Ha
PATCH /api/inquiries/{id}/
Yo'q
Ha
Ha
GET /api/auth/token/
Yo'q
Ha
Ha


3.3. Token sozlamalari
Access token muddati: 60 daqiqa
Refresh token muddati: 7 kun
Token yangilash: POST /api/auth/token/refresh/
Blacklist: Logout qilinganda refresh token o'chiriladi

4. API ENDPOINTLAR
4.1. Mahsulotlar — /api/products/
GET /api/products/ — Mahsulotlar ro'yxati
Faol mahsulotlar ro'yxatini qaytaradi. Pagination va filter qo'llab-quvvatlanadi.
Query parametrlari:
page — Sahifa raqami (standart: 1)
page_size — Sahifadagi elementlar soni (standart: 12, max: 50)
min_price, max_price — Narx bo'yicha filter
min_power, max_power — Quvvat (Watt) bo'yicha filter
ordering — Saralash: price, -price, power_watt, created_at
search — Mahsulot nomi bo'yicha qidiruv

Javob namunasi (200 OK):
{
  "count": 42,
  "next": "https://api.example.com/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "SolarMax Pro 400W",
      "price": "1250000.00",
      "power_watt": 400,
      "efficiency": 21.5,
      "warranty_years": 25,
      "thumbnail": "https://cdn.example.com/products/1/thumb.jpg",
      "is_active": true
    }
  ]
}


GET /api/products/{id}/ — Mahsulot tafsiloti
Bitta mahsulotning to'liq ma'lumotlarini qaytaradi.
{
  "id": 1,
  "name": "SolarMax Pro 400W",
  "description": "Yuqori samarali monokristallin panel...",
  "price": "1250000.00",
  "power_watt": 400,
  "efficiency": 21.5,
  "warranty_years": 25,
  "images": [
    { "id": 1, "image": "https://...", "order": 0 }
  ],
  "created_at": "2025-03-01T10:00:00Z"
}


POST /api/products/ — Mahsulot qo'shish (Admin)
Yangi mahsulot yaratadi. multipart/form-data formatida yuboriladi (rasm yuklash uchun).
Majburiy maydonlar:
name — Mahsulot nomi (max 200 belgi)
description — Tavsif
price — Narx (so'm, 2 kasr)
power_watt — Quvvat (Watt, butun son)
efficiency — Samaradorlik (%, 0.01 - 100.00)
warranty_years — Kafolat muddati (yil)
Ixtiyoriy maydonlar:
images — Rasmlar ro'yxati (max 10 ta, har biri max 5MB)
is_active — Faollik holati (standart: true)

PUT/PATCH /api/products/{id}/ — Mahsulot tahrirlash (Admin)
PATCH — faqat yuborilgan maydonlarni yangilaydi. PUT — barcha maydonlarni yangilaydi.

DELETE /api/products/{id}/ — Mahsulot o'chirish (Super Admin)
Mahsulotni bazadan o'chiradi. Soft delete ishlatish tavsiya etiladi (is_active = false).

4.2. Mijoz so'rovlari — /api/inquiries/
POST /api/inquiries/ — So'rov qoldirish (Anonim)
Ro'yxatdan o'tmagan mijoz so'rov qoldiradi. Spam himoyasi uchun rate limiting qo'llaniladi (1 ta IP dan 5 daqiqada 3 ta so'rovdan ko'p bo'lmasin).
// So'rov tanasi (JSON)
{
  "full_name": "Alisher Karimov",      // Majburiy, max 100 belgi
  "phone": "+998901234567",             // Majburiy, O'zbekiston format
  "email": "alisher@example.com",       // Ixtiyoriy
  "message": "400W panel haqida...",    // Majburiy, min 10 belgi
  "product_id": 1                       // Ixtiyoriy, qaysi mahsulot haqida
}

Muvaffaqiyatli javob (201 Created):
{
  "id": 15,
  "message": "So'rovingiz qabul qilindi. Admin tez orada bog'lanadi.",
  "created_at": "2025-03-01T14:30:00Z"
}


GET /api/inquiries/ — So'rovlar ro'yxati (Admin)
Barcha mijoz so'rovlarini ko'rish. Filter va saralash imkoniyati mavjud.
Query parametrlari:
status — Holat bo'yicha filter: new, viewed, responded
ordering — Saralash: created_at, -created_at
search — Mijoz ismi yoki telefon bo'yicha qidiruv
page, page_size — Pagination

GET /api/inquiries/{id}/ — So'rov tafsiloti (Admin)
So'rov ko'rilganda status avtomatik 'viewed' ga o'zgaradi va viewed_at vaqt belgilanadi.

PATCH /api/inquiries/{id}/ — So'rovni yangilash (Admin)
Admin so'rovga izoh yozadi va statusini yangilaydi.
{
  "status": "responded",
  "admin_note": "Mijoz bilan telefon orqali bog'landim. Kelishuv bo'ldi."
}


4.3. Autentifikatsiya — /api/auth/
POST /api/auth/token/ — Login
// So'rov
{ "username": "admin", "password": "••••••••" }

// Javob (200 OK)
{
  "access": "eyJhbGciOiJIUzI1NiIsInR...",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR...",
  "user": { "id": 1, "username": "admin", "role": "admin" }
}


POST /api/auth/token/refresh/ — Token yangilash
{ "refresh": "eyJhbGciOiJIUzI1NiIsInR..." }
// Javob: { "access": "eyJhbGci..." }

POST /api/auth/logout/ — Chiqish
{ "refresh": "eyJhbGciOiJIUzI1NiIsInR..." }
// Javob: 204 No Content


5. MA'LUMOTLAR MODELLARI
5.1. Product modeli
class Product(models.Model):
    name          = models.CharField(max_length=200)
    description   = models.TextField()
    price         = models.DecimalField(max_digits=12, decimal_places=2)
    power_watt    = models.PositiveIntegerField()  # Watt
    efficiency    = models.DecimalField(max_digits=5, decimal_places=2)  # %
    warranty_years= models.PositiveSmallIntegerField()
    is_active     = models.BooleanField(default=True)
    created_at    = models.DateTimeField(auto_now_add=True)
    updated_at    = models.DateTimeField(auto_now=True)
    created_by    = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['is_active', 'price'])]


5.2. Inquiry modeli
class Inquiry(models.Model):
    STATUS_CHOICES = [
        ('new', 'Yangi'),
        ('viewed', 'Ko\'rilgan'),
        ('responded', 'Javob berilgan'),
    ]
    full_name    = models.CharField(max_length=100)
    phone        = models.CharField(max_length=20)
    email        = models.EmailField(blank=True, null=True)
    message      = models.TextField()
    product      = models.ForeignKey(Product, null=True, blank=True,
                       on_delete=models.SET_NULL)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES,
                       default='new')
    admin_note   = models.TextField(blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    viewed_at    = models.DateTimeField(null=True, blank=True)
    responded_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']


6. VALIDATSIYA QOIDALARI
6.1. Mahsulot validatsiyasi
name: bo'sh bo'lmasin, max 200 belgi, unikal bo'lishi shart emas
price: musbat son, 0 dan katta
power_watt: 1 dan 10000 gacha (Watt)
efficiency: 0.01 dan 100.00 gacha (%)
warranty_years: 1 dan 30 gacha (yil)
images: har biri max 5MB, JPEG/PNG/WEBP formatlar qabul qilinadi

6.2. So'rov validatsiyasi
full_name: min 2, max 100 belgi, faqat harf va bo'shliq
phone: O'zbekiston formati: +998XXXXXXXXX
email: to'g'ri email format (ixtiyoriy)
message: min 10, max 2000 belgi
product_id: agar ko'rsatilsa, mavjud va faol mahsulot bo'lishi kerak

7. XATO KODLARI VA JAVOBLAR
HTTP Kod
Nomi
Sababi
Misol
400
Bad Request
Validatsiya xatosi
Noto'g'ri telefon formati
401
Unauthorized
Token yo'q yoki muddati o'tgan
Authorization header yo'q
403
Forbidden
Ruxsat yo'q
Admin bo'lmagan foydalanuvchi
404
Not Found
Resurs topilmadi
Mahsulot mavjud emas
429
Too Many Requests
Rate limit oshib ketdi
Spam himoyasi
500
Server Error
Ichki xato
DB ulanish xatosi


Barcha xato javoblari quyidagi formatda qaytariladi:
{
  "error": true,
  "code": "VALIDATION_ERROR",
  "message": "Telefon raqami noto'g'ri formatda",
  "details": {
    "phone": ["Telefon +998XXXXXXXXX formatida bo'lishi kerak"]
  }
}


8. XAVFSIZLIK TALABLARI
8.1. Umumiy xavfsizlik
Barcha endpointlar HTTPS orqali ishlaydi
CORS: faqat ruxsat etilgan domenlardan so'rovlar qabul qilinadi
CSRF protection: DRF SessionAuthentication uchun
SQL injection: Django ORM ishlatilganda avtomatik himoyalangan
XSS: javoblar to'g'ri Content-Type header bilan qaytariladi

8.2. Rate Limiting
POST /api/inquiries/: 1 IP dan 5 daqiqada max 3 ta so'rov
POST /api/auth/token/: 1 IP dan 10 daqiqada max 10 ta urinish
Boshqa endpointlar: daqiqada 60 so'rov

8.3. Ma'lumotlar himoyasi
Parollar: Django default PBKDF2 hashing (bcrypt yoki argon2 tavsiya etiladi)
Maxfiy kalitlar .env faylida saqlanadi, kod omborida emas
Media fayllar: S3 yoki xavfsiz lokal saqlash, to'g'ridan-to'g'ri bazaga saqlanmaydi

9. ISHLASH KO'RSATKICHLARI
9.1. Javob vaqti talablari
GET endpointlari (ro'yxat): 95% so'rovlar < 300ms
GET endpointlari (tafsilotar): 95% so'rovlar < 200ms
POST (so'rov yaratish): 95% so'rovlar < 500ms
POST (mahsulot yaratish): 95% so'rovlar < 1000ms (rasm yuklash bilan)

9.2. Pagination
Barcha ro'yxat endpointlari pagination qo'llaydi. Standart sahifa hajmi 12 ta element. Maksimal 50 ta elementga ruxsat beriladi.

9.3. Kesh
Mahsulotlar ro'yxati: Redis da 5 daqiqa keshlanadi
Mahsulot tafsiloti: Redis da 10 daqiqa keshlanadi
Mahsulot yangilanganda kesh tozalanadi

10. DEPLOY VA MUHIT
10.1. Muhit o'zgaruvchilari
# .env fayl namunasi
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=example.com,www.example.com

# Ma'lumotlar bazasi
DATABASE_URL=postgresql://user:password@db:5432/solar_db

# JWT
JWT_ACCESS_LIFETIME=60          # daqiqa
JWT_REFRESH_LIFETIME=10080      # daqiqa (7 kun)

# Media fayl saqlash
USE_S3=True
AWS_BUCKET_NAME=solar-media
AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG

# Email (xabar bildirishnomasi uchun)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=admin@example.com
EMAIL_HOST_PASSWORD=app-password


10.2. Docker sozlamasi
# docker-compose.yml asosiy xizmatlar
services:
  web:
    build: .
    command: gunicorn config.wsgi:application --bind 0.0.0.0:8000
    depends_on: [db, redis]

  db:
    image: postgres:15-alpine
    volumes: [postgres_data:/var/lib/postgresql/data]

  redis:
    image: redis:7-alpine

  nginx:
    image: nginx:alpine
    ports: ['80:80', '443:443']


11. QABUL MEZONLARI
11.1. Funktsional talablar
Admin login/logout qilishi va token olishi mumkin
Admin yangi mahsulot yaratishi, rasm yuklashi mumkin
Admin mavjud mahsulotni tahrirlashi mumkin
Super admin mahsulotni o'chirishi mumkin
Anonim mijoz so'rov qoldira oladi (autentifikatsiyasiz)
Admin barcha so'rovlarni ko'ra oladi va filter qo'llay oladi
Admin so'rovni ko'rganda status avtomatik 'viewed' ga o'zgaradi
Admin so'rovga izoh yoza oladi va statusini yangilay oladi

11.2. Texnik talablar
Barcha endpointlar OpenAPI 3.0 spetsifikatsiyasiga mos hujjatlangan
Unit testlar yozilgan, 80% dan yuqori code coverage
Rasm yuklash ishlaydi (JPEG, PNG, WEBP, max 5MB)
Xato holatlari to'g'ri HTTP kodlari bilan qaytariladi
Rate limiting spam so'rovlarni bloklaydi
PostgreSQL migratsiyalar to'liq yozilgan

11.3. Sinovlar
Unit testlar: Django TestCase yordamida har bir endpoint uchun
Integration testlar: autentifikatsiya oqimi, so'rov yaratish oqimi
Postman Collection yoki Swagger UI orqali qo'lda tekshirish

12. RIVOJLANISH BOSQICHLARI
Sprint 1 (1-hafta): Asos
Django loyihasini sozlash va Docker muhitini tayyorlash
Ma'lumotlar bazasi modellarini yaratish (Product, ProductImage, Inquiry, User)
JWT autentifikatsiya tizimini sozlash

Sprint 2 (2-hafta): Mahsulotlar moduli
Products API: CRUD endpointlari
Rasm yuklash funksiyasini amalga oshirish
Filter, qidiruv va pagination qo'shish

Sprint 3 (3-hafta): So'rovlar moduli
Inquiries API: yaratish va boshqarish endpointlari
Rate limiting va validatsiya
Status o'zgarishi logikasi

Sprint 4 (4-hafta): Yakunlash
Swagger/OpenAPI hujjatlarini yakunlash
Testlarni yozish va code coverage tekshirish
Deploy sozlamalari va xavfsizlik tekshiruvi

Muhim eslatma: Ushbu texnik topshiriq backend tizimi uchun minimum talablarni belgilaydi. Rivojlanish jarayonida yangi talablar yuzaga kelsa, hujjat yangilanib boradi. Barcha o'zgarishlar versiya tarixi orqali kuzatiladi.
