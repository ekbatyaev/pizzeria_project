-- Менеджер пиццерии
CREATE TABLE Менеджер_пиццерии (
    id_менеджера INT UNIQUE PRIMARY KEY,
    уровень_менеджера VARCHAR(50) NOT NULL,
    дата_начала_работы DATE NOT NULL
);

-- Пиццерия
CREATE TABLE Пиццерия (
    id_пиццерии INT UNIQUE PRIMARY KEY,
    id_менеджера INT UNIQUE REFERENCES Менеджер_пиццерии(id_менеджера) ON DELETE CASCADE,
    адрес VARCHAR(255) NOT NULL,
    стоимость_доставки INT NOT NULL,
    количество_заказов INT DEFAULT 0
);

-- Покупатель
CREATE TABLE Покупатель (
    id_покупателя BIGINT UNIQUE PRIMARY KEY,
    имя VARCHAR(100) NOT NULL,
    телефон VARCHAR(20) NOT NULL UNIQUE
);

-- Курьер
CREATE TABLE Курьер (
    id_курьера INT UNIQUE PRIMARY KEY,
    количество_доставляемых_заказов INT DEFAULT 0,
    количество_выполненных_заказов INT DEFAULT 0
);

-- Продукт
CREATE TABLE Продукт (
    id_продукта INT UNIQUE PRIMARY KEY,
    название VARCHAR(100) NOT NULL,
    описание TEXT,
    стоимость NUMERIC(10, 2) NOT NULL
);

-- Ингредиенты
CREATE TABLE Ингредиенты (
    id_ингредиента INT UNIQUE PRIMARY KEY,
    id_пиццерии INT REFERENCES Пиццерия(id_пиццерии) ON DELETE CASCADE,
    наименование VARCHAR(100) NOT NULL,
    количество INT NOT NULL
);

-- Заказ
CREATE TABLE Заказ (
    id_заказа BIGINT UNIQUE PRIMARY KEY,
    стоимость_заказа NUMERIC(10, 2) NOT NULL,
    адрес_доставки VARCHAR(255) NOT NULL,
    id_заказчика BIGINT REFERENCES Покупатель(id_покупателя) ON DELETE CASCADE,
    id_пиццерии INT REFERENCES Пиццерия(id_пиццерии) ON DELETE CASCADE,
    id_курьера INT REFERENCES Курьер(id_курьера) ON DELETE SET NULL,
    статус_заказа VARCHAR(50) NOT NULL
);

-- Состав заказа
CREATE TABLE Состав_заказа (
    id_заказа INT REFERENCES Заказ(id_заказа) ON DELETE CASCADE,
    id_продукта INT REFERENCES Продукт(id_продукта) ON DELETE CASCADE,
    количество INT NOT NULL,
    PRIMARY KEY (id_заказа, id_продукта)
);

-- Состав продукта
CREATE TABLE Состав_продукта (
    id_продукта BIGINT REFERENCES Продукт(id_продукта) ON DELETE CASCADE,
    id_ингредиента INT REFERENCES Ингредиенты(id_ингредиента) ON DELETE CASCADE,
    количество INT NOT NULL,
    PRIMARY KEY (id_продукта, id_ингредиента)
);

-- Сотрудники
CREATE TABLE Сотрудники (
    id_сотрудника INT UNIQUE PRIMARY KEY,
    имя VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    телефон VARCHAR(20) NOT NULL UNIQUE,
    пароль VARCHAR(255) NOT NULL
);

--Информация про менеджеров пиццерии
INSERT INTO Менеджер_пиццерии (id_менеджера, уровень_менеджера, дата_начала_работы) VALUES
(5201, 'Старший менеджер', '2020-01-15'),
(5202, 'Менеджер смены', '2021-06-01'),
(5203, 'Старший менеджер', '2019-09-10'),
(5204, 'Менеджер смены', '2022-03-05'),
(5205, 'Старший менеджер', '2018-11-20'),
(5206, 'Менеджер смены', '2023-01-10');

--Информация про пиццерии
INSERT INTO Пиццерия (id_пиццерии, id_менеджера, адрес, стоимость_доставки, количество_заказов) VALUES
(1, 5201, 'ул. Белинского, 110', 150, 0),
(2, 5202, 'ул. Родионова, 192', 200, 0),
(3, 5203, 'ул. Ошарская, 38', 150, 0),
(4, 5204, 'ул. Горького, 226', 180, 0),
(5, 5205, 'пр. Гагарина, 99', 200, 0),
(6, 5206, 'ул. Ларина, 13', 250, 0);

--Информация про сотрудников
INSERT INTO Сотрудники (id_сотрудника, имя, email, телефон, пароль) VALUES
(5201, 'Иван Иванов', 'ivanov@mail.com', '+79012345678', 'password123'),
(5202, 'Анна Смирнова', 'smirnova@mail.com', '+79087654321', 'securepass'),
(5203, 'Петр Петров', 'petrov@mail.com', '+79123456789', 'mypassword'),
(5204, 'Елена Кузнецова', 'kuznecova@mail.com', '+79109876543', 'pass1234'),
(5205, 'Максим Орлов', 'orlov@mail.com', '+79213456789', 'qwerty'),
(5206, 'Ольга Соколова', 'sokolova@mail.com', '+79209876543', '123456'),
(1127, 'Дмитрий Васильев', 'vasilev@mail.com', '+79099911223', 'dmitriypass'),
(1128, 'Мария Волкова', 'volkova@mail.com', '+79181114455', 'volkova123'),
(1129, 'Алексей Федоров', 'fedorov@mail.com', '+79217778899', 'alexpass'),
(1110, 'Татьяна Боровикова', 'borovikova@mail.com', '+79263335577', 'tatyana456'),
(1111, 'Егор Синицын', 'sinitsin@mail.com', '+79120003344', 'egorpassword'),
(1112, 'Светлана Никифорова', 'nikiforova@mail.com', '+79153332211', 'sveta123'),
(1113, 'Николай Семенов', 'semenov@mail.com', '+79229998866', 'kolyaqwerty'),
(1114, 'Алина Зайцева', 'zaitseva@mail.com', '+79044455667', 'alinasecure'),
(1115, 'Григорий Иванов', 'grivanov@mail.com', '+79217766554', 'grigpassword'),
(1116, 'Ксения Белова', 'belova@mail.com', '+79035566789', 'kseniyapass'),
(1117, 'Виктор Ковалев', 'kovalev@mail.com', '+79167778811', 'viktor123');

--Информация про курьеров
INSERT INTO Курьер (id_курьера, количество_доставляемых_заказов, количество_выполненных_заказов) VALUES
(1127, 0, 0),
(1129, 0, 0),
(1110, 0, 0),
(1111, 0, 0),
(1112, 0, 0),
(1113, 0, 0),
(1114, 0, 0),
(1115, 0, 0),
(1116, 0, 0),
(1117, 0, 0),
(1128, 0, 0);

--Информация про ингредиенты
INSERT INTO Продукт (id_продукта, название, описание, стоимость) VALUES
(1, 'Пицца Маргарита', 'Классическая пицца с томатным соусом, моцареллой и свежими листьями базилика', 400.00),
(2, 'Пицца Пепперони', 'Пицца с пикантной пепперони, сыром моцарелла и фирменным томатным соусом', 450.00),
(3, 'Пицца Четыре сыра', 'Гурманская пицца с сыром моцарелла, горгонзолой, пармезаном и бри', 500.00),
(4, 'Пицца Гавайская', 'Сочетание ананасов, ветчины и моцареллы на нежном тесте', 480.00),
(5, 'Овощная пицца', 'Легкая пицца с болгарским перцем, грибами, оливками и томатами', 420.00),
(6, 'Шаурма Классическая', 'Шаурма с курицей, свежими овощами, соусом и лавашем', 250.00),
(7, 'Шаурма Острая', 'Шаурма с курицей, острым соусом, овощами и хрустящим лавашем', 270.00),
(8, 'Шаурма Сырная', 'Шаурма с дополнительным слоем плавленого сыра и сливочным соусом', 290.00),
(9, 'Лимонад Цитрус-микс', 'Ручной лимонад с апельсином, лимоном, мятой и газированной водой', 150.00),
(10, 'Лимонад Малина-лайм', 'Напиток с натуральным сиропом малины, лаймом и свежей мятой', 160.00),
(11, 'Домашний квас', 'Традиционный квас, приготовленный по старинному рецепту', 120.00),
(12, 'Имбирный лимонад', 'Освежающий напиток с имбирем, лимоном и мёдом', 170.00);

--Ингредиенты
INSERT INTO Ингредиенты (id_ингредиента, id_пиццерии, наименование, количество) VALUES
(1, 1, 'Моцарелла', 1000),
(2, 1, 'Томатный соус', 500),
(3, 1, 'Базилик', 200),
(4, 1, 'Пепперони', 300),
(5, 1, 'Горгонзола', 150),
(6, 1, 'Пармезан', 150),
(7, 1, 'Бри', 150),
(8, 1, 'Ветчина', 400),
(9, 1, 'Ананасы', 200),
(10, 1, 'Болгарский перец', 300),
(11, 1, 'Грибы', 300),
(12, 1, 'Оливки', 200),
(13, 2, 'Курица', 1000),
(14, 2, 'Лаваш', 500),
(15, 2, 'Овощи свежие', 700),
(16, 2, 'Острый соус', 300),
(17, 2, 'Сыр плавленый', 300),
(18, 3, 'Апельсины', 200),
(19, 3, 'Лимоны', 200),
(20, 3, 'Мята', 100),
(21, 3, 'Газированная вода', 500),
(22, 3, 'Малиновый сироп', 150),
(23, 3, 'Лаймы', 150),
(24, 3, 'Имбирь', 100),
(25, 3, 'Мед', 50),
(26, 'Хлеб (ржаной или белый)', 300),
(27, 'Сахар', 100),
(28, 'Дрожжи', 5),
(29, 'Вода', 1000);

--Состав продуктов
INSERT INTO Состав_продукта (id_продукта, id_ингредиента, количество) VALUES
(1, 1, 200),
(1, 2, 100),
(1, 3, 10),
(2, 1, 200),
(2, 2, 100),
(2, 4, 50),
(3, 1, 150),
(3, 5, 50),
(3, 6, 50),
(3, 7, 50),
(4, 1, 200),
(4, 2, 100),
(4, 8, 50),
(4, 9, 50),
(5, 1, 150),
(5, 2, 100),
(5, 10, 50),
(5, 11, 50),
(5, 12, 30),
(6, 13, 100),
(6, 14, 50),
(6, 15, 70),
(7, 13, 100),
(7, 14, 50),
(7, 15, 70),
(7, 16, 20),
(8, 13, 100),
(8, 14, 50),
(8, 15, 70),
(8, 17, 30),
(9, 18, 50),
(9, 19, 50),
(9, 20, 10),
(9, 21, 200),
(10, 22, 30),
(10, 23, 20),
(10, 20, 10),
(10, 21, 200),
(11, 26, 300),
(11, 27, 100),
(11, 28, 5),
(11, 29, 1000),
(12, 24, 20),
(12, 19, 30),
(12, 25, 10),
(12, 21, 200);

--Функция по проверке наличия продуктов
CREATE OR REPLACE FUNCTION get_available_products_by_pizzeria(pizzeria_id INT)
RETURNS TABLE (id_продукта INT, название VARCHAR, описание TEXT, стоимость NUMERIC) AS $$
BEGIN
    RETURN QUERY
    SELECT p.id_продукта, p.название, p.описание, p.стоимость
    FROM Продукт p
    JOIN Состав_продукта pc ON p.id_продукта = pc.id_продукта
    JOIN Ингредиенты i ON pc.id_ингредиента = i.id_ингредиента
    WHERE i.id_пиццерии = pizzeria_id
    GROUP BY p.id_продукта, p.название, p.описание, p.стоимость
    HAVING COUNT(pc.id_ингредиента) =
        (SELECT COUNT(*) FROM Состав_продукта pc2
         JOIN Ингредиенты i2 ON pc2.id_ингредиента = i2.id_ингредиента
         WHERE pc2.id_продукта = p.id_продукта AND i2.id_пиццерии = pizzeria_id
         AND i2.количество >= pc2.количество);
END;
$$ LANGUAGE plpgsql;

--Процедура вычитания продуктов из таблицы ингредиенты
CREATE OR REPLACE PROCEDURE distract_ingridients(
    p_product_id INT,
    p_pizzeria_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Проверяем, существует ли продукт в таблице Состав_продукта
    IF NOT EXISTS (
        SELECT 1
        FROM Состав_продукта
        WHERE id_продукта = p_product_id
    ) THEN
        RAISE EXCEPTION 'Продукт с ID % не найден в таблице Состав_продукта.', p_product_id;
    END IF;

    -- Проверяем, существует ли пиццерия
    IF NOT EXISTS (
        SELECT 1
        FROM Ингредиенты
        WHERE id_пиццерии = p_pizzeria_id
    ) THEN
        RAISE EXCEPTION 'Пиццерия с ID % не найдена.', p_pizzeria_id;
    END IF;

    -- Проверяем, хватает ли ингредиентов на складе
    IF EXISTS (
        SELECT 1
        FROM Ингредиенты ing
        JOIN Состав_продукта sp ON ing.id_ингредиента = sp.id_ингредиента
        WHERE sp.id_продукта = p_product_id
          AND ing.id_пиццерии = p_pizzeria_id
          AND ing.количество < sp.количество
    ) THEN
        RAISE EXCEPTION 'Недостаточно ингредиентов на складе пиццерии с ID % для продукта %.', p_pizzeria_id, p_product_id;
    END IF;

    -- Вычитаем ингредиенты для продукта
    UPDATE Ингредиенты ing
    SET количество = ing.количество - sp.количество
    FROM Состав_продукта sp
    WHERE
        ing.id_пиццерии = p_pizzeria_id
        AND ing.id_ингредиента = sp.id_ингредиента
        AND sp.id_продукта = p_product_id;

    -- Уведомление об успешном выполнении
    RAISE NOTICE 'Ингредиенты для продукта с ID % успешно вычтены из склада пиццерии с ID %.', p_product_id, p_pizzeria_id;
END;
$$;

--Функция для получения массивов продуктов по индексам
CREATE OR REPLACE FUNCTION get_products_by_ids(product_ids INT[])
RETURNS TABLE (
    номер_позиции INT,
    id_продукта INT,
    название VARCHAR(100),
    описание TEXT,
    стоимость NUMERIC(10, 2)
) AS $$
BEGIN
    RETURN QUERY
    WITH product_list AS (
        SELECT unnest(product_ids) AS id_продукта, generate_series(1, array_length(product_ids, 1)) AS номер_позиции
    )
    SELECT pl.номер_позиции, p.id_продукта, p.название, p.описание, p.стоимость
    FROM product_list pl
    JOIN Продукт p ON pl.id_продукта = p.id_продукта
    ORDER BY pl.номер_позиции;
END;
$$ LANGUAGE plpgsql;

--Процедура для возвращения ингредиентов заготовленных на продукт
CREATE OR REPLACE FUNCTION return_ingredients_to_stock(product_id INT)
RETURNS VOID AS $$
BEGIN
    UPDATE Ингредиенты
    SET количество = Ингредиенты.количество + subquery.количество
    FROM (
        SELECT id_ингредиента, количество
        FROM Состав_продукта
        WHERE id_продукта = product_id
    ) AS subquery
    WHERE Ингредиенты.id_ингредиента = subquery.id_ингредиента;
    RAISE NOTICE 'Ингредиенты для продукта % возвращены на склад.', product_id;
END;
$$ LANGUAGE plpgsql;

--Процедура для создания заказа

CREATE OR REPLACE FUNCTION add_order(
    id_заказа BIGINT,
    order_composition JSONB,
    customer_name VARCHAR(100),  -- Изменено имя переменной
    customer_phone VARCHAR(20),  -- Изменено имя переменной
    адрес VARCHAR(255),
    id_пиццерии INT,
    order_summ NUMERIC(10, 2)
) RETURNS VOID AS $$
DECLARE
    id_заказчика BIGINT;  -- Переменная для id заказчика
    id_курьера INT;
    product_id INT;       -- Изменена переменная на product_id
    название VARCHAR(100);  -- Переменная для названия продукта
    количество INT := 1;
BEGIN
    -- Определить id_заказчика по имени и телефону
    SELECT id_покупателя INTO id_заказчика
    FROM Покупатель
    WHERE Покупатель.имя = customer_name AND Покупатель.телефон = customer_phone;

    -- Если покупатель не найден, выбросить ошибку
    IF id_заказчика IS NULL THEN
        RAISE EXCEPTION 'Покупатель с именем % и телефоном % не найден', customer_name, customer_phone;
    END IF;

    -- Вставить данные в таблицу Заказ
    INSERT INTO Заказ (
        id_заказа, стоимость_заказа, адрес_доставки, id_заказчика, id_пиццерии, id_курьера, статус_заказа
    ) VALUES (
        id_заказа, order_summ, адрес, id_заказчика, id_пиццерии, NULL, 'Готовится'
    );

    -- Обход массива order_composition для вставки данных в таблицу Состав_заказа
    FOR product_id IN SELECT (jsonb_array_elements_text(order_composition))::INT LOOP
        -- Получить название продукта из таблицы Продукт
        SELECT Продукт.название INTO название
        FROM Продукт
        WHERE Продукт.id_продукта = product_id;

        -- Вставить данные в таблицу Состав_заказа
        INSERT INTO Состав_заказа (
            id_заказа, id_продукта, наименование_позиции, количество
        ) VALUES (
            id_заказа, product_id, название, количество
        );
    END LOOP;
END;
$$ LANGUAGE plpgsql;

--Процедура для создания и проверки существования покупателя

CREATE OR REPLACE FUNCTION add_customer(
    id_customer BIGINT,  -- Изменили тип с INT на BIGINT
    customer_name VARCHAR(100),
    customer_number VARCHAR(20)
)
RETURNS BIGINT AS $$  -- Возвращаем BIGINT, так как id_покупателя теперь BIGINT
DECLARE
    v_id_customer BIGINT;  -- Переменная теперь BIGINT
BEGIN
    -- Ищем покупателя по имени и телефону
    SELECT id_покупателя INTO v_id_customer
    FROM Покупатель
    WHERE имя = customer_name AND телефон = customer_number;

    -- Если покупатель найден, возвращаем его id
    IF FOUND THEN
        RETURN v_id_customer;
    ELSE
        -- Если покупатель не найден, вставляем новый и возвращаем id
        -- Вставляем с заданным id, если передан id покупателя
        INSERT INTO Покупатель (id_покупателя, имя, телефон)
        VALUES (id_customer, customer_name, customer_number)
        ON CONFLICT (id_покупателя) DO NOTHING  -- Предотвращаем ошибку, если такой id уже существует
        RETURNING id_покупателя INTO v_id_customer;

        RETURN v_id_customer;
    END IF;
END;
$$ LANGUAGE plpgsql;

--Функция для получения списка заказов по айди покупателя

CREATE OR REPLACE FUNCTION get_orders_by_customer_id(customer_id BIGINT)
RETURNS TABLE(
    id_заказа BIGINT,
    стоимость_заказа NUMERIC(10, 2),
    адрес_доставки VARCHAR(255),
    id_заказчика BIGINT,
    id_пиццерии INT,
    id_курьера INT,
    статус_заказа VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT z.id_заказа, z.стоимость_заказа, z.адрес_доставки, z.id_заказчика,
           z.id_пиццерии, z.id_курьера, z.статус_заказа
    FROM Заказ z
    WHERE z.id_заказчика = customer_id;

    -- Проверяем, найдены ли записи
    IF NOT FOUND THEN
        RAISE EXCEPTION 'No orders found for customer with ID %', customer_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

--Функция для вывода состава заказ по айди заказа

CREATE OR REPLACE FUNCTION get_order_details(order_id BIGINT)
RETURNS TABLE(
    номер_позиции BIGINT,  -- Изменено с INT на BIGINT
    название VARCHAR(100),
    описание TEXT,
    стоимость_руб NUMERIC
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        ROW_NUMBER() OVER (ORDER BY sa.id_продукта) AS номер_позиции,
        sa.наименование_позиции AS название,
        p.описание,
        p.стоимость AS стоимость_руб
    FROM
        Состав_заказа sa
    INNER JOIN
        Продукт p ON sa.id_продукта = p.id_продукта
    WHERE
        sa.id_заказа = order_id;
END;
$$ LANGUAGE plpgsql;

--Функция для подсчета заказов по id_пиццерии

CREATE OR REPLACE FUNCTION update_order_count(pizzeria_id INT)
RETURNS VOID AS $$
BEGIN
    UPDATE Пиццерия
    SET количество_заказов = (
        SELECT COUNT(*)
        FROM Заказ
        WHERE id_пиццерии = pizzeria_id
    )
    WHERE id_пиццерии = pizzeria_id;
END;
$$ LANGUAGE plpgsql;

--Триггерная функция для работы функции подсчета заказов

CREATE OR REPLACE FUNCTION order_count_trigger()
RETURNS TRIGGER AS $$
BEGIN
    -- Обновляем количество заказов для пиццерии
    IF (TG_OP = 'INSERT' OR TG_OP = 'UPDATE') THEN
        PERFORM update_order_count(NEW.id_пиццерии);
    ELSIF (TG_OP = 'DELETE') THEN
        PERFORM update_order_count(OLD.id_пиццерии);
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;

--Триггер для отслеживания изменений

CREATE TRIGGER trigger_update_order_count
AFTER INSERT OR UPDATE OR DELETE
ON Заказ
FOR EACH ROW
EXECUTE FUNCTION order_count_trigger();

--Функция для получения списка заказов по id пиццерии

CREATE OR REPLACE FUNCTION get_list_of_orders_by_pizzeria(pizzeria_id INT)
RETURNS TABLE(
    id_заказа BIGINT,
    стоимость_заказа NUMERIC(10, 2),
    адрес_доставки VARCHAR(255),
    id_заказчика BIGINT,
    id_курьера INT,
    статус_заказа VARCHAR(50)
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        Заказ.id_заказа,
        Заказ.стоимость_заказа,
        Заказ.адрес_доставки,
        Заказ.id_заказчика,
        Заказ.id_курьера,
        Заказ.статус_заказа
    FROM Заказ
    WHERE Заказ.id_пиццерии = pizzeria_id;
END;
$$ LANGUAGE plpgsql;

--Функция для обновления статуса заказа
CREATE OR REPLACE FUNCTION update_order_status(
    order_id BIGINT,
    new_status_order VARCHAR(50)
)
RETURNS VOID AS $$
BEGIN
    UPDATE Заказ
    SET статус_заказа = new_status_order
    WHERE id_заказа = order_id;

    -- Проверка, что заказ был обновлен
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order with ID % does not exist', order_id;
    END IF;
END;
$$ LANGUAGE plpgsql;

--Функция для предоставления курьеру готовящихся заказов
CREATE OR REPLACE PROCEDURE assign_courier_to_order(
    p_order_id BIGINT,
    p_courier_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Обновляем id_курьера и статус заказа в таблице Заказ
    UPDATE Заказ
    SET id_курьера = p_courier_id,
        статус_заказа = 'В доставке'
    WHERE id_заказа = p_order_id;

    -- Проверяем, обновилось ли значение
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order with ID % does not exist.', p_order_id;
    END IF;

    -- Увеличиваем количество доставляемых заказов у курьера
    UPDATE Курьер
    SET количество_доставляемых_заказов = количество_доставляемых_заказов + 1
    WHERE id_курьера = p_courier_id;

    -- Проверяем, обновилось ли значение
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Courier with ID % does not exist.', p_courier_id;
    END IF;
END;
$$;

--Функция обновляющая таблицу заказа
CREATE OR REPLACE PROCEDURE assign_courier_to_order(
    p_order_id BIGINT,
    p_courier_id INT
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- Обновляем id_курьера и статус заказа в таблице Заказ
    UPDATE Заказ
    SET id_курьера = p_courier_id,
        статус_заказа = 'В доставке'
    WHERE id_заказа = p_order_id;

    -- Проверяем, обновилось ли значение
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Order with ID % does not exist.', p_order_id;
    END IF;

    -- Увеличиваем количество доставляемых заказов у курьера
    UPDATE Курьер
    SET количество_доставляемых_заказов = количество_доставляемых_заказов + 1
    WHERE id_курьера = p_courier_id;

    -- Проверяем, обновилось ли значение
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Courier with ID % does not exist.', p_courier_id;
    END IF;
END;
$$;

--Функция для увеличения количества выполненных заказов у курьера

CREATE OR REPLACE FUNCTION increment_completed_orders(p_courier_id INT)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
    -- Увеличиваем количество выполненных заказов
    UPDATE Курьер
    SET количество_выполненных_заказов = количество_выполненных_заказов + 1
    WHERE id_курьера = p_courier_id;

    -- Проверяем, обновилась ли строка
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Courier with ID % does not exist.', p_courier_id;
    END IF;
END;
$$;
