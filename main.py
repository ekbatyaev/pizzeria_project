import json
import sqlalchemy
import tkinter as tk
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Numeric, text, Date
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from time import strftime
from re import fullmatch
from tkinter import messagebox,ttk

Base = declarative_base()

# Таблицы
class Pizzeria_Manager(Base):
    __tablename__ = 'Менеджер_пиццерии'
    id = Column('id_менеджера', Integer, primary_key=True, unique=True)
    level = Column('уровень_менеджера', String, nullable=False)
    start_date = Column('дата_начала_работы', Date, nullable=False)

class Employee(Base):
    __tablename__ = 'Сотрудники'
    id = Column('id_сотрудника', Integer, primary_key=True, unique=True)
    name = Column('имя', String, nullable=False)
    email = Column('email', String, unique=True, nullable=False)
    phone = Column('телефон', String, unique=True, nullable=False)
    password = Column('пароль', String, nullable=False)

class Pizzeria(Base):
    __tablename__ = 'Пиццерия'
    id = Column('id_пиццерии', Integer, primary_key=True)
    address = Column('адрес', String)
    manager_id = Column('id_менеджера', Integer)
    delivery_cost = Column('стоимость_доставки', Integer)
    orders_count = Column('количество_заказов', Integer, default=0)
    orders = relationship("Order", back_populates="pizzeria")

class Order(Base):
    __tablename__ = 'Заказ'
    id = Column('id_заказа', Integer, primary_key=True)
    pizzeria_id = Column('id_пиццерии', Integer, ForeignKey('Пиццерия.id_пиццерии'))
    total_cost = Column('стоимость_заказа', Numeric(10, 2))
    delivery_address = Column('адрес_доставки', String)
    customer_id = Column('id_заказчика', Integer)
    courier_id = Column('id_курьера', Integer)
    status_order = Column('статус_заказа', String)
    pizzeria = relationship("Pizzeria", back_populates="orders")

class Buyer(Base):
    __tablename__ = 'Покупатель'
    id = Column('id_покупателя', Integer, primary_key=True)
    name = Column('имя', String)
    phone = Column('телефон', String)


# Подключение к базе данных
engine = create_engine("postgresql+psycopg2://pizzeria_owner:pizza@localhost:5433/pizza_time")
Session = sessionmaker(bind=engine)
session = Session()

# Настройка GUI
class PizzaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pizza Management System")
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        self.root.geometry("600x500")
        tk.Label(self.root, text="  Добро пожаловать!", font=("Arial", 25)).pack(pady=30)
        tk.Button(self.root, text="Сделать заказ", command=self.make_order, font=("Arial", 14), width=50, height=5).pack(pady=10)
        tk.Button(self.root, text="Просмотр заказов", command=self.list_of_orders, font=("Arial", 14), width=50,
                  height=5).pack(pady=10)
        tk.Button(self.root, text="Войти в систему", command=self.login, font=("Arial", 14), width=50, height=5).pack(pady=10)

    def list_of_orders(self):
        dialog = tk.Toplevel(self.root)  # Создание окна
        dialog.title("Требуется ввод данных")
        dialog.geometry("500x300")

        tk.Label(dialog, text="Введите ID покупателя:", font=("Arial", 14)).pack(pady=10)
        customer_id_entry = tk.Entry(dialog, font=("Arial", 14), width=20)
        customer_id_entry.pack(pady=10)

        def confirm_selection():
            try:
                customer_id = int(customer_id_entry.get())
                order = session.execute(
                    text("SELECT * FROM get_orders_by_customer_id(:customer_id)"),
                    {"customer_id": customer_id}
                )
                orders = order.fetchall()
                print(orders, len(orders))
                if orders:
                    dialog.destroy()
                    self.orders_list(orders)
                else:
                    messagebox.showinfo("Уведомление", "Для данного ID покупателя заказы не найдены.")
            except ValueError:
                messagebox.showerror("Ошибка", "ID покупателя не сущетствует или введено неверно.")
            except sqlalchemy.exc.InternalError as e:
                if "No orders found for customer" in str(e):
                    messagebox.showinfo("Уведомление", "Для данного ID покупателя заказы не найдены.")
                else:
                    messagebox.showerror("Ошибка", "Произошла ошибка при выполнении запроса.")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Неизвестная ошибка: {e}")

        tk.Button(dialog, text="Подтвердить", command=confirm_selection, font=("Arial", 14), width=15).pack(pady=10)
        tk.Button(dialog, text="Отмена", command=dialog.destroy, font=("Arial", 14), width=15).pack(pady=10)

    def orders_list(self, orders):
        orders_window = tk.Toplevel(self.root)
        orders_window.title("Cписок заказов")
        orders_window.geometry("1200x600")

        # Создаем контейнер для Treeview
        tree_frame = tk.Frame(orders_window)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        columns = ["Номер заказа", "Стоимость заказа", "Адрес доставки", "id_пиццерии", "Статус заказа"]
        tree = ttk.Treeview(tree_frame, columns=columns, show="headings", style="Treeview")

        # Настраиваем колонки
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col in ["Адрес доставки", "Статус заказа"] else 100)
        tree.column("Адрес доставки", anchor="center", width=400)

        # Размещаем Treeview
        tree.pack(fill=tk.BOTH, expand=True)

        # Добавляем данные в Treeview
        ids = [item[0] for item in orders]
        print(ids)
        for index, order in enumerate(orders, start=1):
            tree.insert("", "end", values=(index, order[1], order[2], order[4], order[6]))

        # Добавляем дополнительные кнопки
        self.add_buttons_order_list(orders_window, ids)

    def add_buttons_order_list(self, window, ids):
        """Добавление элементов управления (кнопки) в окно"""

        # Создаем фрейм для кнопок и других элементов управления
        button_frame = tk.Frame(window)
        button_frame.pack(fill=tk.X, pady=10)

        # Добавляем текстовый виджет для ввода
        label = tk.Label(button_frame, text="Введите номер заказа, который хотите просмотреть подробнее:")
        label.pack(side=tk.LEFT, padx=5)

        # Поле для ввода номера заказа
        position_entry = tk.Entry(button_frame, width=5)
        position_entry.pack(side=tk.LEFT, padx=5)

        # Кнопка "Подтвердить"
        confirm_button = tk.Button(
            button_frame,
            text="Подтвердить",
            command=lambda: self.show_order_addition(ids[int(position_entry.get()) - 1]),
            bg="lightgreen"
        )
        confirm_button.pack(side=tk.LEFT, padx=5)

        # Кнопка "Назад"
        back_button = tk.Button(button_frame, text="Назад", command=window.destroy, bg="lightgray")
        back_button.pack(side=tk.LEFT, padx=10)

    def show_order_addition(self, order_id):
        # Создаем новое окно для просмотра состава заказа
        order_viewing_window = tk.Toplevel(self.root)
        order_viewing_window .title("Cостав заказа")
        order_viewing_window .geometry("1200x300")

        # Выполнение SQL запроса для получения продуктов по ID
        result = session.execute(
            text("""
                        SELECT *
                        FROM get_order_details(:order_id)
                    """),
            {'order_id': order_id}
        )
        order_details = result.fetchall()
        # Создаем таблицу для отображения продуктов
        columns = ["Номер позиции", "Название", "Описание", "Стоимость(руб)"]
        tree = ttk.Treeview(order_viewing_window, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col == "Название" else 100)
        tree.column("Описание", anchor="center", width=700)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заполняем таблицу продуктами
        for index, product in enumerate(order_details, start=1):
            tree.insert("", "end", values=(
                index, product[1], product[2], product[3]))

        tk.Button(order_viewing_window, text="Закрыть", command=order_viewing_window.destroy, font=("Arial", 14), width=20, height=2).pack(pady=10)


    def login(self):
        dialog = tk.Toplevel(self.root)  # Создание выползающего окна
        dialog.title("Вход в систему")
        dialog.geometry("500x300")

        tk.Label(dialog, text="Введите email:", font=("Arial", 14)).pack(pady=5)
        email_entry = tk.Entry(dialog, font=("Arial", 14), width=30)
        email_entry.pack(pady=5)

        tk.Label(dialog, text="Введите пароль:", font=("Arial", 14)).pack(pady=5)
        password_entry = tk.Entry(dialog, show="*", font=("Arial", 14), width=30)
        password_entry.pack(pady=5)

        def authenticate():
            email = email_entry.get()
            password = password_entry.get()
            employee = session.query(Employee).filter(Employee.email == email).first()
            if employee is None:
                messagebox.showerror("Ошибка", "Некорректный ввод данных")
            else:
                if employee and employee.password == password and str(employee.id)[0] == "5":
                    self.manager_menu(employee, dialog)
                elif str(employee.id)[0] == "1":
                    self.courier(employee, dialog)
                else:
                    messagebox.showerror("Ошибка", "Неверный логин или пароль")

        tk.Button(dialog, text="Войти", command=authenticate, font=("Arial", 14), width=20, height=2).pack(pady=10)
        tk.Button(dialog, text="Назад", command=self.main_menu, font=("Arial", 14), width=20, height=2).pack(pady=10)
    def courier(self, employee, window):
        window.destroy()
        courier_window = tk.Toplevel(self.root)
        courier_window.title(f"Добро пожаловать, {employee.name}!")
        courier_window.geometry("1400x800")
        tk.Label(courier_window, text=f"Список заказов", font=("Arial", 16)).pack(pady=20)
        result = session.execute(
            text("""
                SELECT * 
                FROM get_ready_and_preparing_orders();
            """)
        )
        orders = result.fetchall()
        global order_pos_num
        order_pos_num = [item[0] for item in orders]
        columns = ["Порядковый номер", "ID заказа", "Стоимость заказа", "Адрес доставки", "ID пиццерии", "Статус"]
        tree = ttk.Treeview(courier_window, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col == "Адрес доставки" or "ID_заказчика" else 100)
        tree.column("Адрес доставки", anchor="center", width=400)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        for index, order in enumerate(orders, start=1):
            tree.insert("", "end", values=(index, order[0], order[1], order[2], order[4], order[6]))
        tk.Button(courier_window, text="Посмотреть заказ подробнее",
                  command=lambda: self.get_num_order_courier(orders),
                  font=("Arial", 14), width=25,
                  height=2).pack(
            side=tk.LEFT,
            pady=10)
        tk.Button(courier_window, text="Выбрать заказ",
                  command=lambda: self.get_num_changing_courier(courier_window, order_pos_num, tree, employee),
                  font=("Arial", 14), width=20,
                  height=2).pack(
            side=tk.LEFT,
            pady=10)
        tk.Button(courier_window, text="Закрыть", command=courier_window.destroy, font=("Arial", 14), width=20,
                  height=2).pack(
            side=tk.LEFT,
            pady=10)

    def get_num_changing_courier(self, main_window, order_pos, tree, employee):
        dialog = tk.Toplevel(self.root)
        dialog.title("Требуется ввод")
        dialog.geometry("500x300")

        tk.Label(dialog, text="Введите порядковый номер заказа, который хотите взять:", font=("Arial", 14)).pack(pady=5)
        number_entry = tk.Entry(dialog, font=("Arial", 14), width=30)
        number_entry.pack(pady=5)

        def num_check():
            number = int(number_entry.get())
            if 1 <= number <= len(order_pos):
                session.execute(
                    text("""
                            CALL assign_courier_to_order(:order_id, :courier_id);
                        """),
                    {'order_id': order_pos[number - 1] , 'courier_id':employee.id}
                )
                session.commit()
                dialog.destroy()
                for item in tree.get_children():
                    tree.delete(item)
                main_window.destroy()
                messagebox.showerror("Уведомление", "Вы успешно взяли заказ")
                self.courier(employee, main_window)
            else:
                messagebox.showerror("Ошибка", "Некорректный ввод данных")

        tk.Button(dialog, text="Взять", command=num_check, font=("Arial", 14), width=20, height=2).pack(pady=10)
        tk.Button(dialog, text="Назад", command=dialog.destroy, font=("Arial", 14), width=20, height=2).pack(pady=10)

    def manager_menu(self, employee, window):
        window.destroy()
        manager_window = tk.Toplevel(self.root)
        manager_window.title(f"Добро пожаловать, {employee.name}!")
        manager_window.geometry("1400x800")
        tk.Label(manager_window, text=f"Список заказов", font=("Arial", 16)).pack(pady=20)
        pizzeria = session.query(Pizzeria).filter(Pizzeria.manager_id == employee.id).first()
        result = session.execute(
            text("""
                                SELECT *
                                FROM get_list_of_orders_by_pizzeria(:pizzeria_id)
                            """),
            {'pizzeria_id': pizzeria.id}
        )
        orders = result.fetchall()
        global order_pos_num
        order_pos_num = [item[0] for item in orders]

        common_order_summ = 0
        for order in orders:
            common_order_summ += order[1]
        columns = ["Порядковый номер", "ID заказа", "Стоимость заказа", "Адрес доставки", "ID заказчика", "ID курьера",
                   "Статус"]
        tree = ttk.Treeview(manager_window, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col == "Адрес доставки" or "ID_заказчика" else 100)
        tree.column("Адрес доставки", anchor="center", width=400)

        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        for index, order in enumerate(orders, start=1):
            tree.insert("", "end", values=(index, order[0], order[1], order[2], order[3], order[4], order[5]))
        tk.Label(manager_window, text=f"Общая сумма заказов: {common_order_summ};", font = ("Arial", 15)).pack(side=tk.RIGHT, pady=20)
        tk.Label(manager_window, text=f"Количество заказов:  {len(orders)};", font=("Arial", 15)).pack(side=tk.RIGHT,
                                                                                                       pady=20)
        tk.Button(manager_window, text="Посмотреть заказ подробнее", command=lambda :self.get_num_detailed_order_view(orders),
                  font=("Arial", 14), width=25,
                  height=2).pack(
            side=tk.LEFT,
            pady=10)
        tk.Button(manager_window, text="Изменить статус заказа", command=lambda : self.get_num_changing_order_status(manager_window, orders, tree),
                  font=("Arial", 14), width=20,
                  height=2).pack(
            side=tk.LEFT,
            pady=10)
        tk.Button(manager_window, text="Закрыть", command=manager_window.destroy, font=("Arial", 14), width=20,
                  height=2).pack(
            side=tk.LEFT,
            pady=10)
    def get_num_order_courier(self, orders):
        dialog = tk.Toplevel(self.root)  # Создание выползающего окна
        dialog.title("Требуется ввод")
        dialog.geometry("500x300")

        tk.Label(dialog, text="Введите порядковый номер заказа:", font=("Arial", 14)).pack(pady=5)
        number_entry = tk.Entry(dialog, font=("Arial", 14), width=30)
        number_entry.pack(pady=5)

        def num_check():
            number = int(number_entry.get())
            if 1 <= number <= len(orders):
                self.detailed_courier_view(order_pos_num[number - 1], dialog)
            else:
                messagebox.showerror("Ошибка", "Некорректный ввод данных")

        tk.Button(dialog, text="Просмотреть", command=num_check, font=("Arial", 14), width=20, height=2).pack(pady=10)
        tk.Button(dialog, text="Назад", command=dialog.destroy, font=("Arial", 14), width=20, height=2).pack(pady=10)
    def detailed_courier_view(self, order_id, dialog):
        dialog.destroy()
        # Создаем новое окно для просмотра состава заказа
        courier_detailed_order_window = tk.Toplevel(self.root)
        courier_detailed_order_window.title("Информация о заказе")
        courier_detailed_order_window.geometry("1300x400")
        order = session.query(Order).filter(Order.id == order_id).first()
        buyer = session.query(Buyer).filter(Buyer.id == order.customer_id).first()
        info_frame = tk.Frame(courier_detailed_order_window)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(info_frame, text=f"Статус заказа: {order.status_order};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
        tk.Label(info_frame, text=f"Имя клиента: {buyer.name};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
        tk.Label(info_frame, text=f"Номер телефона клиента: {buyer.phone};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
        tk.Label(info_frame, text=f"Адрес доставки: {order.delivery_address};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)

        # Выполнение SQL запроса для получения продуктов по ID
        result = session.execute(
            text("""
                                        SELECT *
                                        FROM get_order_details(:order_id)
                                    """),
            {'order_id': order_id}
        )
        # Получение всех строк результата
        order_details = result.fetchall()
        # Создаем таблицу для отображения продуктов
        columns = ["Номер позиции", "Название", "Описание", "Стоимость(руб)"]
        tree = ttk.Treeview(courier_detailed_order_window, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col == "Название" else 100)
        tree.column("Описание", anchor="center", width=700)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заполняем таблицу продуктами
        for index, product in enumerate(order_details, start=1):
            tree.insert("", "end", values=(
                index, product[1], product[2], product[3]))
        tk.Button(courier_detailed_order_window, text="Закрыть", command=courier_detailed_order_window.destroy, font=("Arial", 14),
                  width=20, height=2).pack(pady=10)

    def get_num_changing_order_status(self, main_window, orders, tree):
        dialog = tk.Toplevel(self.root)
        dialog.title("Требуется ввод")
        dialog.geometry("500x300")

        tk.Label(dialog, text="Введите порядковый номер заказа:", font=("Arial", 14)).pack(pady=5)
        number_entry = tk.Entry(dialog, font=("Arial", 14), width=30)
        number_entry.pack(pady=5)

        def num_check():
            number = int(number_entry.get())
            if 1 <= number <= len(orders):
                self.changing_order_status(main_window, order_pos_num[number - 1], dialog, tree)
            else:
                messagebox.showerror("Ошибка", "Некорректный ввод данных")

        tk.Button(dialog, text="Выбрать", command=num_check, font=("Arial", 14), width=20, height=2).pack(pady=10)
        tk.Button(dialog, text="Назад", command=dialog.destroy, font=("Arial", 14), width=20, height=2).pack(pady=10)
    def changing_order_status(self, main_window, order_id, window, tree):
        window.destroy()
        dialog = tk.Toplevel(self.root)
        dialog.title("Выберите статус заказа")
        dialog.geometry("500x300")
        tk.Button(dialog, text="Готов", command=lambda :self.updating_table_and_order_status(main_window, dialog, tree, order_id, "Готов"), font=("Arial", 14), width=20, height=2).pack(pady=10)
        tk.Button(dialog, text="Доставлен", command=lambda :self.updating_table_and_order_status(main_window, dialog, tree, order_id, "Доставлен"), font=("Arial", 14), width=20, height=2).pack(pady=10)
        tk.Button(dialog, text="Вернуться назад", command=dialog.destroy, font=("Arial", 14), width=20, height=2).pack(pady=10)

    def updating_table_and_order_status(self,main_window, dialog, tree, order_id, new_status_order):
        dialog.destroy()
        status_changing = session.execute(
            text("""
                        SELECT update_order_status(:order_id, :new_status_order);
                    """),
            {'order_id': order_id, 'new_status_order': new_status_order}
        )
        session.commit()
        for item in tree.get_children():
            tree.delete(item)
        order = session.query(Order).filter(Order.id== order_id).first()
        pizzeria = session.query(Pizzeria).filter(Pizzeria.id== order.pizzeria_id).first()
        employee = session.query(Employee).filter(Employee.id== pizzeria.manager_id).first()
        if new_status_order == "Доставлен":
            session.execute(
                text("""
                        SELECT increment_completed_orders(:courier_id);
                    """),
                {'courier_id': order.courier_id}
            )
            session.commit()
        messagebox.showinfo("Успех", "Статус заказа успешно обновлен.")
        main_window.update()
        self.manager_menu(employee, main_window)
    def get_num_detailed_order_view(self, orders):
        dialog = tk.Toplevel(self.root)  # Создание выползающего окна
        dialog.title("Требуется ввод")
        dialog.geometry("500x300")

        tk.Label(dialog, text="Введите порядковый номер заказа:", font=("Arial", 14)).pack(pady=5)
        number_entry = tk.Entry(dialog, font=("Arial", 14), width=30)
        number_entry.pack(pady=5)
        def num_check():
            number = int(number_entry.get())
            if 1 <= number <= len(orders):
                self.detailed_order_view(order_pos_num[number - 1], dialog)
            else:
                messagebox.showerror("Ошибка", "Некорректный ввод данных")

        tk.Button(dialog, text="Просмотреть", command=num_check, font=("Arial", 14), width=20, height=2).pack(pady=10)
        tk.Button(dialog, text="Назад", command=dialog.destroy, font=("Arial", 14), width=20, height=2).pack(pady=10)
    def detailed_order_view(self, order_id, dialog):
        dialog.destroy()
        # Создаем новое окно для просмотра состава заказа
        detailed_order_window = tk.Toplevel(self.root)
        detailed_order_window.title("Информация о заказе")
        detailed_order_window.geometry("1300x400")
        order = session.query(Order).filter(Order.id == order_id).first()
        buyer = session.query(Buyer).filter(Buyer.id == order.customer_id).first()
        info_frame = tk.Frame(detailed_order_window)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        tk.Label(info_frame, text=f"Статус заказа: {order.status_order};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
        tk.Label(info_frame, text=f"Имя клиента: {buyer.name};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
        tk.Label(info_frame, text=f"Номер телефона клиента: {buyer.phone};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
        tk.Label(info_frame, text=f"Адрес доставки: {order.delivery_address};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)

        # Выполнение SQL запроса для получения продуктов по ID
        result = session.execute(
            text("""
                                SELECT *
                                FROM get_order_details(:order_id)
                            """),
            {'order_id': order_id}
        )
        # Получение всех строк результата
        order_details = result.fetchall()
        # Создаем таблицу для отображения продуктов
        columns = ["Номер позиции", "Название", "Описание", "Стоимость(руб)"]
        tree = ttk.Treeview(detailed_order_window, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col == "Название" else 100)
        tree.column("Описание", anchor="center", width=700)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заполняем таблицу продуктами
        for index, product in enumerate(order_details, start=1):
            tree.insert("", "end", values=(
                index, product[1], product[2], product[3]))
        if order.courier_id is None:
            employee = session.query(Employee).filter(Employee.id == order.courier_id).first()
            tk.Label(detailed_order_window, text=f"Имя курьера: {employee.name};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
            tk.Label(detailed_order_window, text=f"Номер телефона курьера: {employee.phone};", font=("Arial", 14)).pack(
            side=tk.LEFT, pady=20)
        else:
            tk.Label(detailed_order_window, text=f"Курьер еще не взял заказ",
                     font=("Arial", 14)).pack(
                side=tk.LEFT, pady=20)

        tk.Button(detailed_order_window, text="Закрыть", command=detailed_order_window.destroy, font=("Arial", 14),
                  width=20, height=2).pack(pady=10)
    def check_the_order(self, product_ids, flag):
        # Создаем новое окно для изменения состава заказа
        order_edit_window = tk.Toplevel(self.root)
        order_edit_window.title("Cостава заказа")
        order_edit_window.geometry("1200x300")

        # Выполнение SQL запроса для получения продуктов по ID
        result = session.execute(text("""
            SELECT *
            FROM get_products_by_ids(:product_ids)
        """), {'product_ids': product_ids})
        products = result.fetchall()

        global ids
        ids = [item for item in product_ids]
        if not flag:
            order_summ = 0
            print(products)
            for i in range(len(products)):
                order_summ += products[i][4]
            print(order_summ)
            tk.Label(order_edit_window, text=f"Общая сумма заказа: {order_summ}",
                     font=("Arial", 16)).pack(pady=10)
        # Создаем таблицу для отображения продуктов
        columns = ["Номер позиции", "Название", "Описание", "Стоимость(руб)"]
        tree = ttk.Treeview(order_edit_window, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col == "Название" else 100)
        tree.column("Описание", anchor="center", width=700)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Заполняем таблицу продуктами
        for index, product in enumerate(products, start=1):
            tree.insert("", "end", values=(
                index, product[2], product[3], product[4]))
        if flag:
            # Добавляем элементы управления для удаления позиции
            self.add_buttons_changing_order(order_edit_window, tree)



    def add_buttons_changing_order(self, window, tree):
        """ Добавление элементов управления (кнопки) в окно """
        button_frame = tk.Frame(window)
        button_frame.pack(fill=tk.X, pady=10)

        label = tk.Label(button_frame, text="Введите номер позиции, которую хотите убрать из заказа:")
        label.pack(side=tk.LEFT, padx=5)

        position_entry = tk.Entry(button_frame, width=5)
        position_entry.pack(side=tk.LEFT, padx=5)

        remove_button = tk.Button(button_frame, text="Убрать позицию",
                                  command=lambda: self.remove_position(position_entry, tree, window), bg="lightgreen")
        remove_button.pack(side=tk.LEFT, padx=5)

        back_button = tk.Button(button_frame, text="Назад", command=window.destroy, bg="lightgray")
        back_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def remove_position(self, position_entry, tree, window):
        """ Удаление выбранной позиции из заказа """
        try:
            position = int(position_entry.get())
            total_items = len(tree.get_children())
            if 1 <= position <= total_items:
                # Получаем id продукта из выбранной позиции
                item_index = tree.item(tree.get_children()[position - 1])['values'][0]
                # Вызов SQL функции для возврата ингредиентов на склад
                self.return_ingredients_to_stock(ids[item_index - 1])

                # Удаляем позицию из таблицы
                tree.delete(tree.get_children()[position - 1])
                order_composition.remove(order_composition[position - 1])

                # Обновляем номера позиций в таблице
                self.update_position_numbers(tree)

                messagebox.showinfo("Успех", f"Позиция {position} успешно удалена!")
            else:
                messagebox.showerror("Ошибка", "Номер позиции выходит за допустимые пределы!")
        except ValueError:
            messagebox.showerror("Ошибка", "Пожалуйста, введите корректный номер позиции!")

    def update_position_numbers(self, tree):
        """ Обновление номеров позиций в таблице """
        for index, item in enumerate(tree.get_children(), start=1):
            tree.item(item, values=(index,) + tuple(tree.item(item)['values'][1:]))

    def return_ingredients_to_stock(self, product_id):
        """ Вызов SQL функции для возврата ингредиентов на склад """
        try:
            session.execute(text("""
                SELECT return_ingredients_to_stock(:product_id)
            """), {'product_id': product_id})
            session.commit()
            ids.remove(product_id)
            print(f"Ингредиенты для продукта {product_id} были возвращены на склад.")
        except Exception as e:
            print(f"Ошибка при возврате ингредиентов: {e}")

    def restoring_the_order(self):
        for product in order_composition:
            self.return_ingredients_to_stock(product)
        self.main_menu()

    def get_order_by_ids(self, order_ids, pizzeria):
        """ Открывает финальное окно для просмотра состава заказа """
        # Создаем новое окно для создания заказа
        order_edit_window = tk.Toplevel(self.root)
        order_edit_window.title("Оформление заказа")
        order_edit_window.geometry("1200x350")
        print(order_ids)
        # Вызов процедуры для получения продуктов по заказу
        result = session.execute(text("""
            SELECT *
            FROM get_products_by_ids(:order_ids)
        """), {'order_ids': order_ids})
        products = result.fetchall()
        columns = ["Номер позиции", "Название", "Описание", "Стоимость(руб)"]
        order_summ = 0
        print(products)
        for i in range(len(products)):
            order_summ += products[i][4]
        print(order_summ)
        tk.Label(order_edit_window, text=f"Общая сумма заказа c доставкой: {order_summ + pizzeria.delivery_cost}", font=("Arial", 16)).pack(pady=10)
        # Создаем таблицу
        tree = ttk.Treeview(order_edit_window, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=150 if col == "Название" else 100)
        tree.column("Описание", anchor="center", width=700)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for index, product in enumerate(products, start=1):
            tree.insert("", "end", values=(
                index, product[2], product[3], product[4]))
        # Создаем кнопки для подтверждения и возврата
        self.add_buttons_accepting_order(order_edit_window, pizzeria)

    def add_buttons_accepting_order(self, window, pizzeria):
        button_frame = tk.Frame(window)
        button_frame.pack(fill=tk.X, pady=10)

        confirm_button = tk.Button(button_frame, text="Далее", height=2, width=20,
                                       command=lambda: self.open_customer_info_window(pizzeria, window), bg="lightgreen")
        confirm_button.pack(side=tk.LEFT, padx=10, pady=5)

        back_button = tk.Button(button_frame, text="Назад", height=2, width=20,
                                command=lambda: self.go_back_to_user_choices(window), bg="lightgray")
        back_button.pack(side=tk.RIGHT, padx=10, pady=5)

    def show_order_summary(self, name, phone, address, pizzeria):
        # Проверка валидности номера телефона
        if not fullmatch(r"(\+)?\d+", phone):
            tk.messagebox.showwarning("Ошибка", "Номер телефона должен состоять только из цифр или начинаться с +")
            return

        summary_window = tk.Toplevel(self.root)
        summary_window.title("Заказ оформлен")
        summary_window.geometry("1300x425")
        # Получение/создание id покупателя
        customer = session.execute(text("""
        SELECT add_customer(:id_customer, :customer_name, :customer_number)
        """), {'id_customer': int(strftime("%H%M%S%x").replace("/", "")),
               'customer_name': name, 'customer_number': phone})
        customer_id = customer.scalar()
        session.commit()
        # Вызов процедуры для получения продуктов по заказу
        result = session.execute(text("""
                    SELECT *
                    FROM get_products_by_ids(:order_ids)
                """), {'order_ids': order_composition})
        products = result.fetchall()
        columns = ["Номер позиции", "Название", "Описание", "Стоимость(руб)"]
        order_summ = 0
        for i in range(len(products)):
            order_summ += products[i][4]

        tk.Label(summary_window, text=f"Общая сумма заказа c доставкой: {order_summ + pizzeria.delivery_cost}",
                 font=("Arial", 16)).pack(pady=10)

        order_creation = session.execute(text("""
                SELECT add_order(
                    :id_order,
                    :order_composition,
                    :customer_name,
                    :customer_phone,
                    :delivery_address,
                    :id_pizzeria,
                    :order_sum
                )
            """), {
            'id_order': strftime("%x%H%M%S").replace("/", ""),
            'order_composition': json.dumps(order_composition),
            'customer_name': name,
            'customer_phone': phone,
            'delivery_address': address,
            'id_pizzeria': pizzeria.id,
            'order_sum': order_summ + pizzeria.delivery_cost
        })
        session.commit()

        info_frame = tk.Frame(summary_window)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        tk.Label(info_frame, text=f"Имя: {name}").pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Телефон: {phone}").pack(anchor="w", padx=10, pady=5)
        tk.Label(info_frame, text=f"Адрес: {address}").pack(anchor="w", padx=10, pady=5)
        tk.Label(summary_window, text=f"Ваш уникальный id_покупателя (сохраните его): {customer_id}", font=("Arial", 14)).pack(pady=10)

        tree = ttk.Treeview(info_frame, columns=columns, show="headings", style="Treeview")
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center", width=200 if col == "Название"  else 100)
        tree.column("Описание", anchor="center", width=600)
        tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        for index, product in enumerate(products, start=1):
            tree.insert("", "end", values=(index, product[2], product[3], product[4]))

        close_button = tk.Button(summary_window, text="Закрыть", command=summary_window.destroy, bg="lightgray")
        close_button.pack(pady=10)

    def open_customer_info_window(self, pizzeria, window):
        window.destroy()
        customer_window = tk.Toplevel(self.root)
        customer_window.title("Информация по доставке")
        customer_window.geometry("500x300")

        tk.Label(customer_window, text="    Пожалуйста, введите свои данные", font=("Arial", 16)).grid(
            row=0, column=0, columnspan=2, pady=20)

        tk.Label(customer_window, text="Имя:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        name_entry = tk.Entry(customer_window, font=("Arial", 14), width=30)
        name_entry.grid(row=1, column=1, padx=10, pady=10)

        tk.Label(customer_window, text="Телефон:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=10,
                                                                            sticky="e")
        phone_entry = tk.Entry(customer_window, font=("Arial", 14), width=30)
        phone_entry.grid(row=2, column=1, padx=10, pady=10)

        tk.Label(customer_window, text="Адрес:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        address_entry = tk.Entry(customer_window, font=("Arial", 14), width=30)
        address_entry.grid(row=3, column=1, padx=10, pady=10)

        def confirm_customer_info():
            name = name_entry.get()
            phone = phone_entry.get()
            address = address_entry.get()
            if name and phone and address:
                self.show_order_summary(name, phone, address, pizzeria)
                customer_window.destroy()
            else:
                tk.messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")

        # Добавляем кнопки
        confirm_button = tk.Button(customer_window, text="Подтвердить", command=confirm_customer_info,
                                   font=("Arial", 14), bg="lightgreen", width=15, height=2)
        confirm_button.grid(row=4, column=0, padx=20, pady=20, sticky="w")

        back_button = tk.Button(customer_window, text="Назад", command=customer_window.destroy,
                                font=("Arial", 14), bg="lightgray", width=15, height=2)
        back_button.grid(row=4, column=1, padx=20, pady=20, sticky="e")

    def go_back_to_user_choices(self, window):
        window.destroy()

    def select_products(self, pizzeria):
        self.clear_window()
        # Состав заказа
        global order_composition
        order_composition = []
        tk.Label(self.root, text=f"Выберите позиции из меню из пиццерии по адресу: {pizzeria.address}",
                 font=("Arial", 18)).pack(pady=20)
        self.root.geometry("1200x400")
        def get_products():
            # Вызов процедуры для получения доступных продуктов
            result = session.execute(
                text("SELECT * FROM get_available_products_by_pizzeria(:pizzeria_id)"),
                {'pizzeria_id': pizzeria.id}
            )
            # Получаем все доступные продукты
            products = result.fetchall()
            columns = ["ID_продукта", "Название", "Описание", "Стоимость(руб)"]

            # Если виджет уже существует, просто обновляем его содержимое
            if hasattr(self, 'tree') and self.tree.winfo_exists():
                for row in self.tree.get_children():
                    self.tree.delete(row)
                for product in products:
                    self.tree.insert("", "end", values=(
                        product[0], product[1], product[2], product[3]))
            else:
                # Создаем виджет только при первом вызове
                self.tree = ttk.Treeview(self.root, columns=columns, show="headings", style="Treeview")
                for col in columns:
                    self.tree.heading(col, text=col.capitalize())
                    self.tree.column(col, anchor="center", width=150 if col == "Название" else 100)
                self.tree.column("Описание", anchor="center", width=700)
                self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                for product in products:
                    self.tree.insert("", "end", values=(
                        product[0], product[1], product[2], product[3]))

        # Показываем список доступных позиций
        get_products()

        def add_position():
            dialog = tk.Toplevel(self.root)  # Создание выползающего окна
            dialog.title("Выбор позиции")
            dialog.geometry("400x200")

            tk.Label(dialog, text="Введите ID позиции:", font=("Arial", 14)).pack(pady=10)
            product_id_entry = tk.Entry(dialog, font=("Arial", 14), width=20)
            product_id_entry.pack(pady=10)

            def confirm_selection():
                product_id = product_id_entry.get()
                try:
                    product_id = int(product_id)
                    order_composition.append(product_id)
                except ValueError:
                    messagebox.showerror("Ошибка", "Введите корректный числовой ID позиции.")
                    return

                # Получаем список доступных ID продуктов
                result = session.execute(
                    text("SELECT * FROM get_available_products_by_pizzeria(:pizzeria_id)"),
                    {'pizzeria_id': pizzeria.id}
                )
                products = result.fetchall()
                ids = [item[0] for item in products]

                if product_id in ids:
                    dialog.destroy()
                    # Убираем использованные ингредиенты и обновляем список доступных предметов
                    try:
                        session.execute(
                            text("CALL distract_ingridients(:product_id, :pizzeria_id)"),
                            {"product_id": product_id, "pizzeria_id": pizzeria.id}
                        )
                        session.commit()
                        # Обновляем список доступных продуктов
                        get_products()
                        messagebox.showinfo("Уведомление", f"Позиция {product_id} добавлена в заказ!")
                    except Exception as e:
                        session.rollback()
                        messagebox.showerror("Ошибка", f"Ошибка выполнения: {e}")
                else:
                    messagebox.showerror("Ошибка", "Позиция с таким ID в данной пиццерии недоступна.")

            tk.Button(dialog, text="Подтвердить", command=confirm_selection, font=("Arial", 14), width=15).pack(
                pady=10)
            tk.Button(dialog, text="Отмена", command=dialog.destroy, font=("Arial", 14), width=15).pack(pady=10)

        # Кнопки
        tk.Button(self.root, text="Просмотр заказа", command=lambda: self.check_the_order(order_composition, 0),
                  font=("Arial", 14), width=20, height=2).pack(side=tk.LEFT, pady=10)
        tk.Button(self.root, text="Добавить позицию", command=add_position, font=("Arial", 14), width=20, height=2).pack(
            side = tk.LEFT, pady=10)
        tk.Button(self.root, text="Изменить заказ",
                  command=lambda: self.check_the_order(order_composition, 1),
                  font=("Arial", 14), width=20, height=2).pack(side=tk.LEFT, pady=10)
        tk.Button(self.root, text="Оформить заказ", command=lambda: self.get_order_by_ids(order_composition, pizzeria), font=("Arial", 14), width=20,
                  height=2).pack(side=tk.LEFT, pady=10)
        tk.Button(self.root, text="Назад", command=self.restoring_the_order, font=("Arial", 14), width=20,
                  height=2).pack(side=tk.RIGHT, pady=10)

    def make_order(self):
        make_order_window = tk.Toplevel(self.root)
        make_order_window.title("Доступные пиццерии")
        make_order_window.geometry("600x400")
        tk.Label(make_order_window, text="Список доступных пиццерий", font=("Arial", 18)).pack(pady=2)
        # Отображение в виде списка информации про все пиццерии
        pizzerias = session.query(Pizzeria).all()
        columns = ["ID", "Адрес", "Стоимость доставки(руб)"]
        tree = ttk.Treeview(make_order_window, columns=columns, show="headings", style="Treeview")
        for column in columns:
            tree.heading(column, text=column.capitalize())
            tree.column(column, anchor="center", width=150)  # Устанавливаем ширину и выравнивание
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for row in tree.get_children():
            tree.delete(row)

        for pizzeria in pizzerias:
            tree.insert("", "end", values=(
                pizzeria.id, pizzeria.address, pizzeria.delivery_cost))
        # Кнопка для выбора нужной пиццерии
        def open_pizzeria_dialog():
            dialog = tk.Toplevel(self.root) #Создание выползающего окна
            dialog.title("Выбор пиццерии")
            dialog.geometry("400x200")

            tk.Label(dialog, text="Введите ID пиццерии:", font=("Arial", 14)).pack(pady=10)
            pizzeria_id_entry = tk.Entry(dialog, font=("Arial", 14), width=20)
            pizzeria_id_entry.pack(pady=10)
            def confirm_selection():
                pizzeria_id = pizzeria_id_entry.get()
                selected_pizzeria = session.query(Pizzeria).filter_by(id=pizzeria_id).first()

                if selected_pizzeria:
                    make_order_window.destroy()
                    dialog.destroy()
                    self.select_products(selected_pizzeria)
                else:
                    messagebox.showerror("Ошибка", "Пиццерия с таким ID не найдена")

            tk.Button(dialog, text="Подтвердить", command=confirm_selection, font=("Arial", 14), width=15).pack(pady=10)
            tk.Button(dialog, text="Отмена", command=dialog.destroy, font=("Arial", 14), width=15).pack(pady=10)

        # Кнопки
        tk.Button(make_order_window, text="Выбрать пиццерию", command=open_pizzeria_dialog, font=("Arial", 14), width=20,
                  height=2).pack(pady=10)
        tk.Button(make_order_window, text="Назад", command=make_order_window.destroy, font=("Arial", 14), width=20
                  , height=2).pack(pady=10)


    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = PizzaApp(root)
    root.mainloop()
