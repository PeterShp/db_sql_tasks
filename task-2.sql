-- Скріпт 1: Отримання списку фільмів та їх категорій
SELECT title, description, length
FROM public.film;

-- Скріпт 2: Фільми, орендовані певним клієнтом
SELECT c.first_name, c.last_name, f.title, r.rental_period AS rental_start_date
FROM rental r
JOIN inventory i ON r.inventory_id = i.inventory_id
JOIN film f ON i.film_id = f.film_id
JOIN customer c ON r.customer_id = c.customer_id
WHERE c.first_name = 'MARY' AND c.last_name = 'SMITH';

-- Скріпт 3: Популярність фільмів
SELECT f.title, COUNT(r.rental_id) AS rental_count
FROM film f
JOIN inventory i ON f.film_id = i.film_id
JOIN rental r ON i.inventory_id = r.inventory_id
GROUP BY f.film_id, f.title
ORDER BY rental_count DESC
LIMIT 5;

-- Скріпт 4: Додавання нового клієнта
WITH new_city AS (
    INSERT INTO city (city, country_id, last_update)
    VALUES (
        'San Francisco',
        (SELECT country_id FROM country WHERE country = 'United States'),
        NOW()
    )
    RETURNING city_id
),
new_address AS (
    INSERT INTO address (address, address2, district, city_id, postal_code, phone, last_update)
    VALUES (
        '123 Main St',
        '',
        'District 1',
        (SELECT city_id FROM new_city),
        '1234',
        '345-232',
        NOW()
    )
    RETURNING address_id
)
INSERT INTO customer (store_id, first_name, last_name, email, address_id, activebool, create_date, last_update)
VALUES (
    1,
    'ALICE',
    'COOPER',
    'email@mail',
    (SELECT address_id FROM new_address),
    TRUE,
    NOW(),
    NOW()
);

-- Скріпт 5: Оновлення адреси клієнта
UPDATE address a
SET address = '456 Elm St', last_update = NOW()
FROM customer c, city ci
WHERE a.address_id = c.address_id
  AND a.city_id = ci.city_id
  AND c.first_name = 'ALICE' AND c.last_name = 'COOPER'
  AND ci.city = 'San Francisco'
  AND a.address = '123 Main St';

-- Скріпт 6: Видалення клієнта
DELETE FROM customer
WHERE first_name = 'ALICE' AND last_name = 'COOPER';