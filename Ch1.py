class Option:
    def __init__(self,call_or_put,strike_price,expiration_date,american_or_european,asset,size=100):
        self.size = size
        self.call_or_put, self.strike_price, self.expiration_date, self.american_or_european,self.asset \
            = call_or_put.strip().lower()[0],strike_price,expiration_date,american_or_european.strip().lower()[0],asset
        assert self.call_or_put in ['c','p'] and self.american_or_european in ['a','e']

    def describe(self):
        timing_string = ''
        if self.american_or_european == 'a':
            timing_string = 'on or before'
        else:
            timing_string = 'on'


        if self.call_or_put == 'c':
            return f'The right to buy {self.size} shares of {self.asset} {timing_string} {self.expiration_date} for {self.strike_price} per share'
        else:
            return f'The right to sell {self.size} shares of {self.asset} {timing_string} {self.expiration_date} for {self.strike_price} per share'

    def revenue(self,spot_price):
        if self.call_or_put == 'c':
            return max((spot_price-self.strike_price)*self.size,0)
        else:
            return max((self.strike_price-spot_price)*self.size,0)


class Purchase:
    def __init__(self,premium,option):
        self.premium = premium
        self.option = option

    def describe(self):
        return f'You bought {self.option.describe()}, for a premium of {self.option.size*self.premium}'

    def profit(self,spot_price):
        return self.option.revenue(spot_price) - self.option.size*self.premium

class Sale:
    def __init__(self,premium, option):
        self.premium = premium
        self.option = option

    def describe(self):
        to_from = ''
        if self.option.call_or_put == 'c':
            to_from = 'from'
        else:
            to_from = 'to'

        return f'You sold {self.option.describe()} {to_from} you, for a premium of {self.option.size*self.premium}'

    def profit(self, spot_price):
        return -(self.option.revenue(spot_price) - self.option.size * self.premium)


def test1():
    Option1 = Option('put', 3000, 'Dec 31', 'eu', 'gold')
    Option2 = Option('c', 3000, 'Dec 31', 'a', 'gold')

    print(Option1.describe())
    print(Option1.revenue(4000))
    Option2.describe()
    print(Option2.revenue(4000))
    p1 = Purchase(5, Option1)
    p2 = Purchase(4.5, Option2)
    s1 = Sale(4.8, Option1)
    s2 = Sale(4.9, Option2)
    print(f"""
        {p1.describe()}
        {p1.profit(4000)}
        {p2.describe()}
        {p2.profit(4000)}
        {s1.describe()}
        {s1.profit(4000)}
        {s2.describe()}
        {s2.profit(4000)}
        """)


'''
It is May and a trader writes a September call option with a strike price of $20. The stock
price is $18 and the option price is $2. Describe the trader’s cash flows if the option is held
until September and the stock price is $25 at that time.
'''
def p15():
    o = Option('c',20,'sept','a','?')
    p = Sale(2,o)#writing means selling
    print(p.describe())
    print(p.profit(25))

'''
A trader writes a December put option with a strike price of $30. The price of the option
is $4. Under what circumstances does the trader make a gain?
'''
def p16():
    o = Option('p', 30, 'dec', 'a', '?')
    p = Sale(4, o)#writing means selling
    print(p.describe())
    print(p.profit(26))#answer is spot stays above 26 = 30-4



if __name__ == '__main__':
    p16()
