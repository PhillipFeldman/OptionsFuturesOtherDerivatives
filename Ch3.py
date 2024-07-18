from Ch2 import Future
class Hedge:
    def __init__(self, hedge_asset, hedge_s_or_l, asset_amount,asset_price,future_contract:Future,beta,desired_beta=None):
        if desired_beta==None:
            desired_beta=beta
        self.hedge_asset,self.hedge_s_or_l, self.asset_amount,self.asset_price, self.future_contract, self.beta, self.desired_beta  = \
            hedge_asset,hedge_s_or_l, asset_amount,asset_price, future_contract, beta, desired_beta

        self.asset_value = asset_price*asset_amount
        self.num_contracts = None
        if self.desired_beta == self.beta:
            self.num_contracts = self.beta*self.asset_value/self.future_contract.price*self.future_contract.size
        elif self.desired_beta < self.beta:
            self.hedge_s_or_l = 's'
            self.num_contracts \
                = (self.beta-self.desired_beta)*self.asset_value/self.future_contract.price*self.future_contract.size
        else:
            self.hedge_s_or_l = 'l'
            self.num_contracts \
                = -(self.beta - self.desired_beta) * self.asset_value / self.future_contract.price * self.future_contract.size


