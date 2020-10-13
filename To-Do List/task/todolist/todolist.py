from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')
Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String, default='default_value')
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return str(self.id) + ". " + self.task


def print_date_with_day(date):
    print(f"{date.strftime('%A')} {date.day} {date.strftime('%b')}:")


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
today = datetime.today()
date_format = "%Y-%m-%d"

while True:
    
    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit\n")
    menu_item = int(input())
    if menu_item == 1:
        
        rows = session.query(Table).filter(Table.deadline == today.date()).order_by(Table.deadline).all()
        print(f"Today {today.day} {today.strftime('%b')}:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            for i in range(len(rows)):
                print(f"{i+1}. {rows[0].task}")
            print("")
    elif menu_item == 2:
        for i in range(7):
            week_day = today + timedelta(days=i)
            rows = session.query(Table).filter(Table.deadline == week_day.date()).all()
            print_date_with_day(week_day)
            if len(rows) == 0:
                print("Nothing to do!\n")
            else:
                for j in range(len(rows)):
                    print(f"{j+1}. {rows[j].task}")
                print("")
    elif menu_item == 3:
        rows = session.query(Table).order_by(Table.deadline).all()
        print("All tasks:")
        if len(rows) == 0:
            print("Nothing to do!")
        else:
            i = 1
            for row in rows:
                print(f"{i}. {row.task}.", f"{row.deadline.day} {row.deadline.strftime('%b')}")
                i += 1
            print("")
    elif menu_item == 4:
        rows = session.query(Table).filter(Table.deadline < today.date()).all()
        if len(rows) == 0:
            print("Nothing is missed!\n")
        else:
            print("Missed tasks:")
            for i in range(len(rows)):
                row = rows[i]
                print(f"{i + 1}. {row.task}. ", f"{row.deadline.day} {row.deadline.strftime('%b')}")
            print("")
    elif menu_item == 5:
        new_task = str(input("Enter task\n"))
        new_task_deadline = datetime.strptime(str(input("Enter deadline\n")), date_format)
        new_row = Table(task=new_task, deadline=new_task_deadline)
        session.add(new_row)
        session.commit()
        print("The task has been added!\n")
    elif menu_item == 6:
        rows = session.query(Table).all()
        if len(rows) == 0:
            continue
        else:
            print("Choose the number of the task you want to delete:")
            for i in range(len(rows)):
                row = rows[i]
                print(f"{i + 1}. {row.task}. ", f"{row.deadline.day} {row.deadline.strftime('%b')}")
            print("")
            input_task_number = int(input())
            # task_id_to_delete = rows[input_task_number-1].id
            # session.query(Table).filter(Table.id == task_id_to_delete).delete()
            row_to_delete = rows[input_task_number-1]
            session.delete(row_to_delete)
            session.commit()
            print("The task has been deleted!")
        print("")
    elif menu_item == 0:
        print("Bye!")
        break
    else:
        continue
