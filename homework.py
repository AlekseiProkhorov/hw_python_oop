import datetime as dt

def get_today_date():
    return dt.datetime.today().date()

def check_if_7days_passed(date):
    if (dt.datetime.today().date() - date).days <= 7:
        return False
    else: 
        return True

def format_currency(currency):
    if currency == 'rub':
        return 'руб'
    elif currency == 'eur':
        return 'Euro'
    elif currency == 'usd':
        return 'USD'

class Calculator:

    def __init__(self, limit):
        self.limit = limit 
        self.records = []            

    def add_record(self, record):  
        self.records.append(record)

    def get_today_stats(self):
        spent_value = 0
        for record in self.records:
            if record.date == get_today_date():
                spent_value += record.amount
        return spent_value

    def get_week_stats(self):
        spent_value = 0
        for record in self.records:
            if not check_if_7days_passed(record.date):
                spent_value += record.amount
        return spent_value

class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained <= 0:
            return 'Хватит есть!'
        else:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {calories_remained} кКал' 

class CashCalculator(Calculator):
    
    USD_RATE = 79.45
    EURO_RATE = 84.93
    
    def get_today_cash_remained(self, currency):

        spent_cash = super().get_today_stats()
        
        if currency == 'rub':
            spent_cash_in_currency = spent_cash
            limit_in_currency = self.limit
        elif currency == 'usd':
            spent_cash_in_currency = spent_cash / self.USD_RATE
            limit_in_currency = self.limit / self.USD_RATE
        elif currency == 'eur':
            spent_cash_in_currency = spent_cash / self.EURO_RATE
            limit_in_currency = self.limit / self.EURO_RATE

        formatted_currency = format_currency(currency)

        if spent_cash < self.limit:
            return f'На сегодня осталось {float(round(limit_in_currency - spent_cash_in_currency, 2))} {formatted_currency}'
        elif spent_cash == self.limit:
            return 'Денег нет, держись'
        else:
            return f'Денег нет, держись: твой долг - {float(round(spent_cash_in_currency - limit_in_currency, 2))} {formatted_currency}'
        
class Record:
    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        if date == None:
            self.date = get_today_date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
