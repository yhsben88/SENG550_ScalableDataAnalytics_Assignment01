select * from customers;

select count(*) from orders;

select * from orders o
join customers c on o.customer_id = c.customer_id
where c.name = 'Alice Johnson';

select * from deliveries d
join orders o on d.order_id = o.order_id
where d.status <> 'Delivered';

select c.customer_id, c.name, sum(o.total_amount) as total_spent
from customers c 
join orders o on c.customer_id = o.customer_id 
group by c.customer_id, c.name 
order by total_spent desc;

select o.product_category, count(*)
from orders o
group by product_category;

select c.customer_id, c.name, count(o.order_id) as orders_placed
from customers c
join orders o on c.customer_id = o.customer_id
group by c.customer_id, c.name
having count(o.order_id) > 2;

select product_category, sum(o.total_amount) as sum_total
from orders o 
group by product_category
order by sum_total desc
limit 1;

