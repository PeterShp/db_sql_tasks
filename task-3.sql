-- Скріпт 1: Загальна кількість фільмів у кожній категорії
SELECT c.name AS category_name, COUNT(fc.film_id) AS film_count FROM category c JOIN film_category fc ON c.category_id = fc.category_id GROUP BY c.category_id, c.name;

-- Скріпт 2: Середня тривалість фільмів у кожній категорії
SELECT c.name AS category_name, AVG(f.length) AS avg_film_length FROM category c JOIN film_category fc ON c.category_id = fc.category_id JOIN film f ON fc.film_id = f.film_id GROUP BY c.category_id, c.name;

-- Скріпт 3: Мінімальна та максимальна тривалість фільмів
SELECT MIN(length) AS min_film_length, MAX(length) AS max_film_length FROM film;

-- Скріпт 4: Загальна кількість клієнтів
SELECT COUNT(*) AS total_customers FROM customer;

-- Скріпт 5: Сума платежів по кожному клієнту
SELECT c.first_name || ' ' || c.last_name AS customer_name, SUM(p.amount) AS total_payments FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id, c.first_name, c.last_name;

-- Скріпт 6: П'ять клієнтів з найбільшою сумою платежів
SELECT c.first_name || ' ' || c.last_name AS customer_name, SUM(p.amount) AS total_payments FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY total_payments DESC LIMIT 5;

-- Скріпт 7: Загальна кількість орендованих фільмів кожним клієнтом
SELECT c.first_name || ' ' || c.last_name AS customer_name, COUNT(r.rental_id) AS total_rentals FROM customer c JOIN rental r ON c.customer_id = r.customer_id GROUP BY c.customer_id, c.first_name, c.last_name;

-- Скріпт 8: Середній вік фільмів у базі даних
SELECT AVG(EXTRACT(YEAR FROM CURRENT_DATE) - release_year) AS average_film_age FROM film WHERE release_year IS NOT NULL;

-- Скріпт 9: Кількість фільмів, орендованих за певний період
SELECT f.title, COUNT(*) AS rented_films_count FROM rental r JOIN inventory i ON r.inventory_id = i.inventory_id JOIN film f ON i.film_id = f.film_id WHERE rental_period && tsrange('2005-05-30', '2005-06-01') GROUP BY f.film_id, f.title;

-- Скріпт 10: Сума платежів по кожному місяцю
SELECT DATE_TRUNC('month', payment_date) AS month, SUM(amount) AS total_payment FROM payment GROUP BY month ORDER BY month;

-- Скріпт 11: Максимальна сума платежу, здійснена клієнтом
SELECT customer_id, MAX(amount) AS max_payment FROM payment GROUP BY customer_id ORDER BY max_payment DESC;

-- Скріпт 12: Середня сума платежів для кожного клієнта
SELECT c.first_name, c.last_name, AVG(p.amount) AS average_payment FROM customer c JOIN payment p ON c.customer_id = p.customer_id GROUP BY c.customer_id, c.first_name, c.last_name ORDER BY average_payment DESC;

-- Скріпт 13: Кількість фільмів у кожному рейтингу (rating)
SELECT rating, COUNT(*) AS film_count FROM film GROUP BY rating;

-- Скріпт 14: Середня сума платежів по кожному магазину (store)
SELECT s.store_id, AVG(p.amount) AS average_payment FROM staff s JOIN payment p ON s.staff_id = p.staff_id GROUP BY s.store_id;
