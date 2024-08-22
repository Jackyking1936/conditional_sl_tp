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
sdk.init_realtime()
restfut = sdk.marketdata.rest_client.futopt  
restfut.intraday.tickers(type='OPTION', exchange='TAIFEX',session='REGULAR', contractType='I')
# %%

from fubon_neo.sdk import  FubonSDK, Condition, ConditionOrder
from fubon_neo.constant import ( 
    TriggerContent, TradingType, Operator, TPSLOrder, TPSLWrapper, SplitDescription,
    StopSign, TimeSliceOrderType, ConditionMarketType, ConditionPriceType, ConditionOrderType, TrailOrder, Direction, ConditionStatus, HistoryStatus
)
from datetime import datetime, timedelta

condition = Condition(
    market_type = TradingType.Reference,        
    symbol = "2881",
    trigger = TriggerContent.MatchedPrice,
    trigger_value = "80",
    comparison = Operator.LessThan
)

order = ConditionOrder(
    buy_sell= BSAction.Sell,
    symbol = "21",
    quantity = 1000,
    price = None,
    market_type = ConditionMarketType.Common,
    price_type = ConditionPriceType.Market,
    time_in_force = TimeInForce.ROD,
    order_type = ConditionOrderType.Stock,
    user_def = "c_sl"
)

res = sdk.stock.single_condition(active_account, "20240821","20241118", StopSign.Full , condition, order)
# %%
get_res = sdk.stock.get_condition_order(active_account)
#%%
sdk.stock.cancel_condition_orders(active_account, "f28ff37c-76b0-441f-8aaf-2a8bf19f904e")
#%%
guid_list = []
for i in range(100):
    condition = Condition(
        market_type = TradingType.Reference,        
        symbol = "2881",
        trigger = TriggerContent.MatchedPrice,
        trigger_value = "80",
        comparison = Operator.LessThan
    )

    order = ConditionOrder(
        buy_sell= BSAction.Sell,
        symbol = "21",
        quantity = 1000,
        price = None,
        market_type = ConditionMarketType.Common,
        price_type = ConditionPriceType.Market,
        time_in_force = TimeInForce.ROD,
        order_type = ConditionOrderType.Stock
    )

    res = sdk.stock.single_condition(active_account, "20240821","20241118", StopSign.Full , condition, order)
    guid_list.append(res.data.guid)
#%%

for i in range(len(guid_list)):
    sdk.stock.cancel_condition_orders(active_account, guid_list[i])