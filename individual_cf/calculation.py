import pandas as pd
import numpy as np
from babel.numbers import format_currency, format_decimal, default_locale
from decimal import Decimal


class Calculation:
    def __init__(self, data):
        self.account_number = data["account_number"]
        self.months_to_maturity = data["months_to_maturity"]
        self.amortization_term = data["amortization_term"]
        self.payment_type = data["payment_type"]
        self.coupon_type = data["coupon_type"]
        self.recovery_lag = data["recovery_lag"]
        self.bank_balance = data["bank_balance"]
        self.expected_cf = data["expected_cf"]
        self.carrying_value = data["carrying_value"]
        self.lgd = data["lgd"]
        self.smm = data["smm"]
        self.cdr = data["cdr"]
        self.discount_rate = data["discount_rate"]
        self.coupon_rate = data["coupon_rate"]

    @property
    def _raw_actual_total(self):
        expected_default = self.bank_balance * self.cdr
        expected_principal = -np.ppmt(self.coupon_rate / 12, 1, self.months_to_maturity, self.bank_balance -
                                      expected_default)
        expected_interest = (self.bank_balance - expected_default) * (self.coupon_rate / 12)
        prepaid_principal = (self.bank_balance - expected_default - expected_principal) * self.smm
        ending_principal = (self.bank_balance - expected_default - expected_principal - prepaid_principal)
        recovery = 0
        expected_cash_flows = (expected_principal + expected_interest + prepaid_principal)
        pv_of_cash_flows = expected_cash_flows / (1 + (self.discount_rate / 12))

        # Create data frame top row
        initial_cf = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        cf_df = pd.DataFrame(initial_cf, columns=['Period', 'Beginning Principal', 'Expected Default',
                                                  'Expected Principal', 'Interest Rate', 'Expected Interest',
                                                  'Prepaid Principal', 'Ending Principal', 'Recovery',
                                                  'Expected Cash Flows', 'PV of Cash Flows'])

        # Append period 1 CF
        append_df = [[1, self.bank_balance, expected_default, expected_principal,
                      self.coupon_rate, expected_interest, prepaid_principal, ending_principal, recovery,
                      expected_cash_flows, pv_of_cash_flows]]
        append_df_mod = pd.DataFrame(append_df, columns=['Period', 'Beginning Principal', 'Expected Default',
                                                         'Expected Principal', 'Interest Rate', 'Expected Interest',
                                                         'Prepaid Principal', 'Ending Principal', 'Recovery',
                                                         'Expected Cash Flows', 'PV of Cash Flows'])
        cf_df_appended = cf_df.append(append_df_mod, ignore_index=True)
        # loop
        count = 0
        while count < self.months_to_maturity - 1:
            period = int(cf_df_appended["Period"].tail(1)) + 1
            bank_balance = Decimal(float(cf_df_appended["Ending Principal"].tail(1)))
            expected_default = bank_balance * self.cdr
            expected_principal = -np.ppmt(self.coupon_rate / 12, 1, self.months_to_maturity - period + 1,
                                          bank_balance - expected_default)
            expected_interest = (bank_balance - expected_default) * (self.coupon_rate / 12)
            prepaid_principal = (bank_balance - expected_default - expected_principal) * self.smm
            ending_principal = (bank_balance - expected_default - expected_principal - prepaid_principal)
            recovery = 0
            expected_cash_flows = (expected_principal + expected_interest + prepaid_principal)
            pv_of_cash_flows = expected_cash_flows / ((1 + (self.discount_rate / 12)) ** period)
            append_df2 = [[period, bank_balance, expected_default, expected_principal,
                           self.coupon_rate, expected_interest, prepaid_principal, ending_principal, recovery,
                           expected_cash_flows, pv_of_cash_flows]]
            append_df2_mod = pd.DataFrame(append_df2, columns=['Period', 'Beginning Principal', 'Expected Default',
                                                               'Expected Principal', 'Interest Rate',
                                                               'Expected Interest',
                                                               'Prepaid Principal', 'Ending Principal', 'Recovery',
                                                               'Expected Cash Flows', 'PV of Cash Flows'])
            cf_df_appended = cf_df_appended.append(append_df2_mod, ignore_index=True)
            count += 1
        return pd.DataFrame(cf_df_appended, columns=['Period', 'Beginning Principal', 'Expected Default',
                                                               'Expected Principal', 'Interest Rate',
                                                               'Expected Interest',
                                                               'Prepaid Principal', 'Ending Principal', 'Recovery',
                                                               'Expected Cash Flows', 'PV of Cash Flows'])

    @property
    def _cf_df_appended_df(self):
        return str(np.nansum(self._raw_actual_total["Expected Cash Flows"]))

    def _format_as_dollars(self, value):
        return format_currency(value, "USD", locale="en_US")

    def _format_as_decimal(self, value):
        return int(value)

    @property
    def actual_total(self):
        # expected cf at the moment
        return self._format_as_dollars(self._cf_df_appended_df)

    def appended_df(self):
        return self._raw_actual_total

    @property
    def _raw_inflation_adjusted_total(self):
        return str(np.nansum(self._raw_actual_total["PV of Cash Flows"]))

    @property
    def inflation_adjusted_total(self):
        return self._format_as_dollars(self._raw_inflation_adjusted_total)