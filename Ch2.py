class Future:
    def __init__(self,asset,size,delivery,price):
        self.asset, self.size, self.delivery,self.price = asset,size,delivery,price

    def describe(self):
        return (f'contract for {self.size} of {self.asset} at {self.price} per unit,'
                f' to be delivered {self.delivery}')


class MarginAccount:
    def __init__(self,num_contracts,futures_contract:Future,
                 short_or_long,initial_margin,maintenance_margin_rate = .75):
        assert short_or_long in ['s','l']
        self.num_contracts, self.futures_contract,\
        self.short_or_long, self.initial_margin, self.maintenance_margin_rate = \
            num_contracts, futures_contract,\
        short_or_long, initial_margin, maintenance_margin_rate

        self.maintenance_margin = self.initial_margin*self.maintenance_margin_rate
        self.futures_price = futures_contract.price
        self.current_price = futures_contract.price
        self.balance = initial_margin
        self.needs_settling = False

    def settle_day(self,new_price):
        price_delta = new_price -self.current_price
        self.current_price = new_price
        if self.short_or_long == 's':
            price_delta*=-1
        account_delta = price_delta*self.num_contracts*self.futures_contract.size
        self.balance+= account_delta
        if self.balance <= self.maintenance_margin:
            self.needs_settling = True
            print(f'Account must be settled to {self.initial_margin} by tomorrow.')
        elif self.balance >= self.initial_margin:
            self.needs_settling = False

    def withdraw(self,amount):
        if self.balance - self.initial_margin >= amount:
            self.balance -= amount
            self.needs_settling = False

    def deposit(self,amount):
        self.balance+= amount
        if self.balance >= self.initial_margin:
            self.needs_settling = False


    def describe(self):
        return (f'A margin account for {self.num_contracts} {self.futures_contract.describe()} .'
                f'The current futures price is {self.current_price} . '
                f'The current balance is {self.balance} .'
                f'The initial margin was {self.initial_margin} .'
                f'The maintenance margin is {self.maintenance_margin}')



"""
Suppose that in September 2018 a company takes a long position in a contract on May
2019 crude oil futures. It closes out its position in March 2019. The futures price (per
barrel) is $48.30 when it enters into the contract, $50.50 when it closes out its position,
and $49.10 at the end of December 2018. One contract is for the delivery of 1,000 barrels.
What is the company’s total profit? When is it realized? How is it taxed if it is (a) a hedger
and (b) a speculator? Assume that the company has a December 31 year end.
"""
#code doesn't handle tax and accounting implications
def problem4():
    future = Future('oil barrels',1000,'May 2019',48.3)
    contract = MarginAccount(1,future,'l',0,0)
    contract.settle_day(49.1)
    #contract.settle_day(50.5)
    print(contract.describe())



"""
A trader buys two July futures contracts on frozen orange juice concentrate. Each
contract is for the delivery of 15,000 pounds. The current futures price is 160 cents per
pound, the initial margin is $6,000 per contract, and the maintenance margin is $4,500 per
contract. What price change would lead to a margin call? Under what circumstances
could $2,000 be withdrawn from the margin account?
"""
def problem11():
    future = Future('frozen orange juice concentrate(pounds)',15000,'july',1.6)
    contract = MarginAccount(2,future,'l',6000)
    contract.settle_day(1.5)
    contract.settle_day(1.6666667)
    print(contract.describe())



if __name__ == '__main__':
    problem11()