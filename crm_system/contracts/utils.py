from datetime import date

from contracts.models import Contract
from customers.models import Customer
from products.models import Product


def create_contract(
    product: Product,
    customer: Customer,
    start_date: date,
    end_date: date,
):
    try:
        contract = Contract(
            cost=product.cost,
            product=product,
            customer=customer,
            start_date=start_date,
            end_date=end_date,
        )
        contract.name = contract_name_factory(contract)
        contract.save()
        return contract
    except Exception:
        return None


def contract_name_factory(contract: Contract):
    contract_name = "Контракт c '{}' об оказании услуги '{}'".format(
        contract.customer.fullname(),
        contract.product.name,
    )
    return contract_name
