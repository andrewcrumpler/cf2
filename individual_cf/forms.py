from decimal import Decimal
from django import forms

PAYMENT_TYPE_CHOICES = (
    ("1", "Principal and Interest"),
    ("0", "Interest Only"),
)

COUPON_TYPE_CHOICES = (
    ("1", "Fixed"),
    ("0", "Floating"),
)


class RateField(forms.DecimalField):
    def clean(self, *args, **kwargs):
        value = super().clean(*args, **kwargs)
        return value / Decimal("100")


class CalculatorForm(forms.Form):
    account_number = forms.CharField(
        label="Account Number", max_length=250, initial=13094)

    months_to_maturity = forms.DecimalField(
        label="Months to Maturity*",
        max_value=20000,
        min_value=0,
        decimal_places=0,
        initial=208
    )

    amortization_term = forms.DecimalField(
        label="Amortization Term (Months)",
        max_value=20000,
        min_value=0,
        decimal_places=0,
        initial=208
    )

    payment_type = forms.TypedChoiceField(
        coerce=int, label="Payment Type* (does not yet have functionality)", choices=PAYMENT_TYPE_CHOICES)

    coupon_type = forms.TypedChoiceField(
        coerce=int, label="Coupon Type* (Does not yet have functionality)",
        choices=COUPON_TYPE_CHOICES)

    recovery_lag = forms.DecimalField(
        label="Recovery Lag (Does not yet have functionality)",
        initial=0,
        max_value=20000,
        min_value=-1000,
        decimal_places=2,
    )

    bank_balance = forms.DecimalField(
        label="Bank Balance",
        decimal_places=2,
        initial=669247.36
    )

    expected_cf = forms.DecimalField(
        label="Expected Cash Flow",
        decimal_places=2,
        initial=897764
    )

    carrying_value = forms.DecimalField(
        label="Carrying Value",
        decimal_places=2,
        initial=627441
    )

    lgd = RateField(
        widget=forms.widgets.NumberInput(
            attrs={"aria-describedby": "annual-inflation-help"}
        ),
        label="Loss Given Default (%)",
        initial=100,
        max_value=100,
        min_value=0,
        decimal_places=4,
    )

    smm = RateField(
        widget=forms.widgets.NumberInput(
            attrs={"aria-describedby": "annual-inflation-help"}
        ),
        label="Single Monthly Mortality (%)",
        initial=0.426531877756064,
        max_value=100,
        min_value=0,
        decimal_places=20,
    )

    cdr = RateField(
        widget=forms.widgets.NumberInput(
            attrs={"aria-describedby": "annual-inflation-help"}
        ),
        label="Conditional Default Rate (%)",
        initial=0.0539095563266923,
        max_value=100,
        min_value=0,
        decimal_places=25,
    )

    discount_rate = RateField(
        widget=forms.widgets.NumberInput(
            attrs={"aria-describedby": "annual-inflation-help"}
        ),
        label="Discount Rate (%)",
        initial=5.875,
        max_value=100,
        min_value=0,
        decimal_places=4,
    )

    coupon_rate = RateField(
        widget=forms.widgets.NumberInput(
            attrs={"aria-describedby": "annual-inflation-help"}
        ),
        label="Coupon Rate (%)",
        initial=5.375,
        max_value=100,
        min_value=0,
        decimal_places=10,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the Bootstrap HTML class 'form-control' to the widget of each field
        for field in self.fields.values():
            if "class" in field.widget.attrs:
                field.widget.attrs["class"] += " form-control"
            else:
                field.widget.attrs["class"] = "form-control"