
class PaymentOption:
    CASH = 'cash'
    BANK = 'bank'
    BKASH = 'bkash'
    ROCKET = 'rocket'
    NAGAD = 'nagad'

    CHOICES = [
        (CASH, 'Cash'),
        (BANK, 'Bank'),
        (BKASH, 'bKash'),
        (ROCKET, 'Rocket'),
        (NAGAD, 'Nagad')
    ]


class WithdrawalOptions:
    AS_PER_REQUEST = 'as_per_request'
    DAILY = 'daily'
    WEEKLY = 'weekly'
    BI_WEEKLY = 'bi-weekly'
    MONTHLY = 'monthly'

    CHOICES = (
        (AS_PER_REQUEST, 'As per Request'),
        (DAILY, 'Daily'),
        (WEEKLY, 'weekly'),
        (BI_WEEKLY, 'BI-Weekly'),
        (MONTHLY, 'Monthly')
    )
