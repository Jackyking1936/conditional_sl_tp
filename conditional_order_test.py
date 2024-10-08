#%%
from pathlib import Path
import pickle

from fubon_neo.sdk import FubonSDK, Order
from fubon_neo.constant import TimeInForce, OrderType, PriceType, MarketType, BSAction

my_file = Path("./info.pkl")
if my_file.is_file():
    with open('info.pkl', 'rb') as f:
        user_info_dict = pickle.load(f)

sdk = FubonSDK()
accounts = sdk.login(user_info_dict['id'], user_info_dict['pwd'], user_info_dict['cert_path'], user_info_dict['cert_pwd'])

active_account = None
for account in accounts.data:
    if account.account == user_info_dict['target_account']:
        active_account = account

print(active_account)
# %%
from fubon_neo.sdk import  FubonSDK, Order, Condition, ConditionOrder
from fubon_neo.constant import ( 
    TriggerContent, TradingType, Operator, TPSLOrder, TPSLWrapper, SplitDescription,
    StopSign, TimeSliceOrderType, ConditionMarketType, ConditionPriceType, ConditionOrderType, TrailOrder, Direction, ConditionStatus, HistoryStatus
)

#%%
condition = Condition(
    market_type = TradingType.Reference,        
    symbol = "2881",
    trigger = TriggerContent.MatchedPrice,
    trigger_value = "80",
    comparison = Operator.LessThan
)

order = ConditionOrder(     
    buy_sell= BSAction.Sell,
    symbol = "2881",
    quantity = 1000,
    price = None,
    market_type = ConditionMarketType.Common,
    price_type = ConditionPriceType.Market,
    time_in_force = TimeInForce.ROD,
    order_type = ConditionOrderType.Stock,
)

res = sdk.stock.single_condition(active_account, "20240829","20241125", StopSign.Full , condition, order)
print(res)

# %%
sdk.stock.cancel_condition_orders(active_account, res.data.guid)

#%%
import pandas as pd
sdk.init_realtime()
reststock = sdk.marketdata.rest_client.stock
TSE_movers = reststock.snapshot.movers(market='TSE', type='COMMONSTOCK', direction='up', change='percent', gte=-10)
TSE_movers_df = pd.DataFrame(TSE_movers['data'])
OTC_movers = reststock.snapshot.movers(market='OTC', type='COMMONSTOCK', direction='up', change='percent', gte=-10)
OTC_movers_df = pd.DataFrame(OTC_movers['data'])

all_movers_df = pd.concat([TSE_movers_df, OTC_movers_df])
# %%
