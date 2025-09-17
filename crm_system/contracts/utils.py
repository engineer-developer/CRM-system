from datetime import date

from django.db import DatabaseError

from contracts.models import Contract
from customers.models import Customer
from products.models import Product


def create_contract(
    product: Product,
    customer: Customer,
    start_date: date,
    end_date: date,
):
    """Создаем объект контракта"""
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
    except DatabaseError:
        return None


def contract_name_factory(contract: Contract):
    """Создаем наименование контракта"""
    customer_fullname = contract.customer.fullname()
    product_name = contract.product.name
    contract_name = (
        f"Контракт c '{customer_fullname}' об оказании услуги '{product_name}'"
    )
    return contract_name
