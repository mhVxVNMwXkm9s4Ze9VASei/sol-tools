from dotenv import load_dotenv
import requests
import os

load_dotenv()

PUMP_FUN_API_URL = os.environ.get("PUMP_FUN_API_URL")


def getPumpComments(token_address):
    r = requests.get(
        f"{PUMP_FUN_API_URL}/replies/{token_address}?limit=10000&offset=0")

    return r.json()


def getPumpTransactions(token_address):
    r = requests.get(
        f"{PUMP_FUN_API_URL}/trades/{token_address}?limit=10000&offset=0")

    return r.json()


def groupPumpTransactionsByTrader(transactions):
    parsedTransactions = {}

    for transaction in transactions:
        solAmount = transaction["sol_amount"] / 1e9
        tokenAmount = transaction["token_amount"] if transaction["is_buy"] else - \
            transaction["token_amount"]
        trader = transaction["user"]

        if trader not in parsedTransactions:
            parsedTransactions[trader] = {
                "amountBought": solAmount if transaction["is_buy"] else 0,
                "amountSold": solAmount if not transaction["is_buy"] else 0,
                "tokensHeld": tokenAmount,
            }
        else:
            parsedTransactions[trader]["amountBought"] += solAmount if transaction["is_buy"] else 0
            parsedTransactions[trader]["amountSold"] += solAmount if not transaction["is_buy"] else 0
            parsedTransactions[trader]["tokensHeld"] += tokenAmount

    return parsedTransactions
