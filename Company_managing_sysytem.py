# Using pandas for reading xls input and because I like it
from pandas import read_csv


class Employee:
    pay_rise = 1.04
    num_of_all_employees = 0

    def __init__(self, first_name, last_name, pay, department, work_days=None, duty=None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = first_name.lower() + '.' + last_name.lower() + '@company.com'
        self.department = department
        self.pay = pay
        if work_days is None:
            work_days = []
        if type(work_days) == str:
            work_days = work_days.split()
        self.work_days = work_days
        if duty is None:
            duty = []
        self.duty = duty
        Employee.num_of_all_employees += 1

    def full_name(self):
        return '{} {} from the {} department'.format(self.first_name, self.last_name, self.department)

    def apply_raise(self, default_pay_rise=pay_rise):
        self.pay = int(self.pay * default_pay_rise)

    # TODO add a function that show every employee, every manager and every developer

    def is_at_work(self, *days):

        days_of_the_week = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        absent = []
        na_days = []

        for day in days:
            if day.lower() not in days_of_the_week:
                na_days.append(day)
            else:
                if day not in self.work_days and day not in absent:
                    absent.append(day)

        if len(na_days) == 1:
            print('There is no day named {}'.format(na_days[0]))
        elif len(na_days) > 1:
            print('There are no days named: ', end='')
            for day in na_days[:-1]:
                print(day, end=', ')
            print('{}'.format(na_days[-1]))

        if len(absent) == 1:
            print('{} {} is not at work on {}s'.format(self.first_name, self.last_name, absent[0]))
        elif len(absent) > 1:
            print('{} {} is not at work following days: '.format(self.first_name, self.last_name), end='')
            for day in absent[:-1]:
                print(day, end=', ')
            print('{}.'.format(absent[-1]))

    def add_day_at_work(self, *new_day):
        if new_day not in self.work_days:
            self.work_days.extend(new_day)

    def remove_day_at_work(self, day):
        if day in self.work_days:
            self.work_days.remove(day)

    def add_duty(self, *new_duty):
        if new_duty in self.duty:
            raise Exception('{} is already in the duties of {} {}'.format(new_duty, self.first_name, self.last_name))
        else:
            self.duty.extend(new_duty)

    def remove_duty(self, *duty):
        for d in duty:
            if d in self.duty:
                self.duty.remove(d)
            else:
                raise Exception('{} is not in the duties of {} {}'.format(d, self.first_name, self.last_name))

    @classmethod
    def from_string(cls, emp_string):
        first_name, last_name, pay, department, work_days = emp_string.split(',', 3)
        work_days = list(work_days.split(','))
        return cls(first_name, last_name, pay, department, work_days)


class Developer(Employee):
    num_of_developers = 0

    def __init__(self, first_name, last_name, pay, department, work_days, prog_lang, duty=None):
        super().__init__(first_name, last_name, pay, department, work_days, duty)
        self.prog_lang = prog_lang
        Employee.num_of_all_employees += 1
        Developer.num_of_developers += 1


class Manager(Employee):
    num_of_managers = 0

    def __init__(self, first_name, last_name, pay, department, work_days, rank, duty=None):
        super().__init__(first_name, last_name, pay, department, work_days, duty)
        self.rank = rank
        Employee.num_of_all_employees += 1
        Manager.num_of_managers += 1

    def full_name(self):
        return '{} {} {} from the {} department'.format(self.rank, self.first_name, self.last_name, self.department)


"""Reads in xls generated data about employees. Comment out if redundant."""

developer_df = read_csv('developer_database.csv')
manager_df = read_csv('manager_database.csv')

developer = [Developer(developer_df.loc[worker, 'firstname'], developer_df.loc[worker, 'lastname'],
                       developer_df.loc[worker, 'pay'], developer_df.loc[worker, 'department'],
                       developer_df.loc[worker, 'work_days'], developer_df.loc[worker, 'prog_lang'])
             for worker in range(len(developer_df))]

manager = [Manager(manager_df.loc[worker, 'firstname'], manager_df.loc[worker, 'lastname'],
                   manager_df.loc[worker, 'pay'], manager_df.loc[worker, 'department'],
                   manager_df.loc[worker, 'work_days'], manager_df.loc[worker, 'rank'])
           for worker in range(len(manager_df))]

"""Testing"""

# TODO test add day and remove function
