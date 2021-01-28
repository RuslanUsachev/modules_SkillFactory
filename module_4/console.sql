-- 4.1
-- База данных содержит список аэропортов практически всех крупных
-- городов России. В большинстве городов есть только один аэропорт.
-- Исключение составляет:

select a.city,
count(a.city)
from dst_project.airports a
group by a.city
having count(a.city)>1

-- 4.2.1
-- Вопрос 1. Таблица рейсов содержит всю информацию о прошлых, текущих
-- и запланированных рейсах. Сколько всего статусов для рейсов
-- определено в таблице?

select count(distinct f.status)
from dst_project.flights f

-- 4.2.2
-- Вопрос 2. Какое количество самолетов находятся в
-- воздухе на момент среза в базе (статус рейса «самолёт
-- уже вылетел и находится в воздухе»).

select count(f.status)
from dst_project.flights f
where f.status='Delayed'

-- 4.2.3 Вопрос 3. Места определяют схему салона каждой модели.
-- Сколько мест имеет самолет модели  773 (Boeing 777-300)?

select a.model, count(s.seat_no)
from dst_project.seats s
	join dst_project.aircrafts a on a.aircraft_code = s.aircraft_code
where a.model='Boeing 777-300'
group by a.model

-- 4.2.4 Вопрос 4. Сколько состоявшихся (фактических)
-- рейсов было совершено между 1 апреля 2017 года и 1 сентября 2017 года?

select count(flight_id)
from dst_project.flights f
where f.scheduled_arrival between '2017-04-01 00:00:00'
    and '2017-09-01 00:00:00'
  and f.status = 'Arrived';

-- 4.3.1 Вопрос 1. Сколько всего рейсов было отменено по данным базы?

select count(f.status)
from dst_project.flights f 
where f.status='Cancelled'

-- 4.3.2
-- Вопрос 2. Сколько самолетов моделей типа Boeing, Sukhoi Superjet,
-- Airbus находится в базе авиаперевозок?

select 'Boeing' model, count(a.model)
from dst_project.aircrafts a 
where a.model like 'Boeing%'
union all
select 'Sukhoi Superjet' model, count(a.model)
from dst_project.aircrafts a 
where a.model like 'Sukhoi Superjet%'
union all
select 'Airbus' model, count(a.model)
from dst_project.aircrafts a 
where a.model like 'Airbus%'

-- 4.3.3
-- Вопрос 3. В какой части (частях) света находится больше аэропортов?

select 'Europe' tmzm,count(a.city) 
from dst_project.airports a 
where a.timezone like 'Europe%'
union all
select 'Australia' tmzm,count(a.city) 
from dst_project.airports a 
where a.timezone like 'Australia%'
union all
select 'Europe, Asia' tmzm,count(a.city) 
from dst_project.airports a 
where a.timezone like 'Europe, Asia%'
union all
select 'Asia' tmzm,count(a.city) 
from dst_project.airports a 
where a.timezone like 'Asia%'

-- 4.3.4
-- Вопрос 4. У какого рейса была самая большая задержка
-- прибытия за все время сбора данных? Введите id рейса (flight_id).

select f.flight_id, f.actual_arrival-f.scheduled_arrival as time
from dst_project.flights f 
where f.scheduled_arrival is not null and f.actual_arrival is not null
order by 2 desc
limit 1

-- 4.4.1
-- Вопрос 1. Когда был запланирован самый первый вылет, сохраненный в базе данных?

select scheduled_departure
from dst_project.flights
order by 1
limit 1;

-- 4.4.2 Вопрос 2. Сколько минут составляет запланированное время
-- полета в самом длительном рейсе?

select date_part('hour', f.scheduled_arrival-f.scheduled_departure)*60 + date_part('minute', f.scheduled_arrival-f.scheduled_departure)     
from dst_project.flights f 
where f.scheduled_arrival is not null and f.actual_arrival is not null
order by 1 desc
limit 1

-- 4.4.3 Вопрос 3. Между какими аэропортами пролегает самый
-- длительный по времени запланированный рейс?

select date_part('hour', f.scheduled_arrival-f.scheduled_departure)*60 + date_part('minute', f.scheduled_arrival-f.scheduled_departure),
	departure_airport, arrival_airport     
from dst_project.flights f 
where f.scheduled_arrival is not null and f.actual_arrival is not null
order by 1 desc
limit 1

-- 4.4.4 Вопрос 4. Сколько составляет средняя дальность
-- полета среди всех самолетов в минутах? Секунды округляются
-- в меньшую сторону (отбрасываются до минут).

select avg(date_part('hour', scheduled_arrival-scheduled_departure)*60 + date_part('minute', scheduled_arrival-scheduled_departure))
from dst_project.flights 

-- 4.5.1
-- Вопрос 1. Мест какого класса у SU9 больше всего?

select distinct fare_conditions, count(fare_conditions)
from dst_project.seats 
where aircraft_code='SU9'
group by fare_conditions

-- 4.5.2
-- Вопрос 2. Какую самую минимальную стоимость составило бронирование за всю историю?

select min(total_amount)
from dst_project.bookings;

-- 4.5.3
-- Вопрос 3. Какой номер места был у пассажира с id = 4313 788533?

select b.seat_no
from dst_project.boarding_passes b
    join dst_project.tickets t
    on t.ticket_no=b.ticket_no
where t.passenger_id='4313 788533'

-- 5.1.1
-- Вопрос 1. Анапа — курортный город на юге России.
-- Сколько рейсов прибыло в Анапу за 2017 год?

select count(*)
from dst_project.flights 
where (arrival_airport = 'AAQ')
  and (status = 'Arrived')
  and (date_part('year', actual_arrival) = 2017);

-- 5.1.2
-- Вопрос 2. Сколько рейсов из Анапы вылетело зимой 2017 года?

select count(a.city)
from dst_project.airports a
    join dst_project.flights f
    on a.airport_code=f.arrival_airport
where f.departure_airport='AAQ'
  and (date_part('year', actual_departure) = 2017)
  and (date_part('month', actual_departure) in (12, 1, 2))

-- 5.1.3
-- Вопрос 3. Посчитайте количество отмененных рейсов из Анапы за все время.

select f.status, count (f.flight_id)
from dst_project.airports a
    join dst_project.flights f
    on a.airport_code=f.arrival_airport
where f.departure_airport='AAQ'
group by f.status

-- 5.1.4
-- Вопрос 4. Сколько рейсов из Анапы не летают в Москву?

select count (f.flight_id)
from dst_project.airports a
    join dst_project.flights f
    on a.airport_code=f.arrival_airport
where f.departure_airport='AAQ' and a.city!='Moscow'

-- 5.1.5
-- Вопрос 5. Какая модель самолета летящего на рейсах из Анапы имеет больше всего мест?

select a.model, count(distinct s.seat_no)
from dst_project.aircrafts a
    join dst_project.seats s
    on a.aircraft_code=s.aircraft_code
    join dst_project.flights f
    on f.aircraft_code=a.aircraft_code
where departure_airport='AAQ'
group by a.model
order by 2 desc

-- Запрос по всей базе данных

with countSold (flight_id, sold_seats, total_amount) as
         (select f.flight_id,
                 count(t.ticket_no) over (partition by f.flight_id),
                 sum(t.amount) over (partition by f.flight_id)
          from dst_project.flights f
                   join dst_project.ticket_flights t on f.flight_id = t.flight_id),
     countSeats
         (availableSeats, model)
         as (select count(s.seat_no) over (partition by ar.model),
                    ar.model
             from dst_project.seats s
                      join dst_project.aircrafts ar on s.aircraft_code = ar.aircraft_code)
select f.flight_id,
       sold_seats,
       scheduled_departure,
       scheduled_arrival,
       t.total_amount,
       a.latitude,
       a.longitude,
       a.airport_code,
       ar.model,
       c.availableSeats,
f.departure_airport
from dst_project.flights f
         join countSold t on f.flight_id = t.flight_id
         join dst_project.airports a on a.airport_code = f.arrival_airport
         join dst_project.aircrafts ar on ar.aircraft_code = f.aircraft_code
         join countSeats c on c.model = ar.model
where f.departure_airport = 'AAQ'
  and (date_trunc('month', f.scheduled_departure) IN ('2017-01-01',
                                                      '2017-02-01',
                                                      '2017-12-01'))
  and f.status not in ('Cancelled')
group by 1, t.sold_seats, t.total_amount, a.latitude, a.longitude, a.airport_code, c.availableSeats, ar.model
order by 1;

-- Координаты аэропорта Анапы

select longitude, latitude
from dst_project.airports
where airport_code= 'AAQ';
