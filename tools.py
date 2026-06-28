#!/usr/bin/env python3
"""
Custom Tools for TravelWise - Complete Demo

All tools fully implemented and ready to use.
"""


def convert_currency(amount: float, from_currency: str, to_currency: str) -> str:
    """Convert currency using TravelWise exchange rates.
    
    Args:
        amount: The amount to convert
        from_currency: Source currency code (USD, EUR, JPY, GBP)
        to_currency: Target currency code (USD, EUR, JPY, GBP)
    
    Returns:
        Conversion result as a formatted string
    """
    rates = {
        "USD": 1.0,
        "EUR": 0.92,
        "JPY": 149.50,
        "GBP": 0.79,
        "AUD": 1.53,
        "CAD": 1.36
    }
    
    if from_currency.upper() not in rates:
        return f"[ERROR] Unsupported currency: {from_currency}"
    if to_currency.upper() not in rates:
        return f"[ERROR] Unsupported currency: {to_currency}"
    
    usd_amount = amount / rates[from_currency.upper()]
    result = usd_amount * rates[to_currency.upper()]
    
    return f"{amount} {from_currency.upper()} = {result:.2f} {to_currency.upper()}"


def calculate_budget(daily_budget: float, num_days: int, currency: str = "USD") -> str:
    """Calculate total trip budget based on daily spending.
    
    Args:
        daily_budget: Amount to spend per day
        num_days: Number of days for the trip
        currency: Currency code (default: USD)
    
    Returns:
        Budget calculation as a formatted string
    """
    total = daily_budget * num_days
    
    return f"Trip budget: {total:.2f} {currency} ({num_days} days x {daily_budget:.2f}/day)"
