
SELECT    borrow_date as date, count(`id`) totalCOunt
FROM      borrowed_books
WHERE status = 'borrowed'
GROUP BY  borrow_date
ORDER BY borrow_date DESC
LIMIT 7