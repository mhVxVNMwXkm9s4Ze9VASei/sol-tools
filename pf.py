from dotenv import load_dotenv
import json
import requests
import os

load_dotenv()

PUMP_FUN_API_URL = os.environ.get("PUMP_FUN_API_URL")


def checkPumpCoin(tokenAddress):
    return
    # if not os.path.exists(tokenAddress):
    #     os.makedirs(tokenAddress)
    #     print(f"Created directory for token {tokenAddress}.")
    #     tokenData = getPumpData(tokenAddress)

    #     if "statusCode" in tokenData:
    #         print(f"Token {tokenAddress} is not a pump.fun coin.")
    #         return

    #     tokenDataFile = os.path.join(tokenAddress, "data.json")

    #     with open(tokenDataFile, "w") as f:
    #         json.dump(tokenData, f)
    # else:
    #     tokenDataFile = os.path.join(tokenAddress, "data.json")

    #     with open(tokenDataFile, "r") as f:
    #         tokenData = json.load(f)

    # ignore the above for now?

    # if not os.path.exists(tokenAddress):
    #     os.makedirs(tokenAddress)
    #     print(f"Created directory for token {tokenAddress}.")

    # tokenDataFile = os.path.join(tokenAddress, "data.json")
    # tradeDataFile = os.path.join(tokenAddress, "trades.json")

    # if os.path.exists(tokenDataFile):
    #     print(f"File already exists. Checking if token {
    #           tokenAddress} migrated to Raydium.")

    #     with open(tokenDataFile, "r") as f:
    #         fileData = json.load(f)

    #     if fileData["complete"] and os.path.exists(tradeDataFile):
    #         with open(tradeDataFile, "r") as f:
    #             print(f"Loading transaction data for token {tokenAddress}.")
    #             return json.load(f)
    #     else:
    #         print(f"Requesting transaction data for token {tokenAddress}.")
    #         tradeData = getPumpTransactions(tokenAddress)

    #         with open(tradeDataFile, "w") as f:
    #             print(f"Saving transaction data...")
    #             json.dump(tradeData, f)

    #         return tradeData
    # else:
    #     print(f"Data file for token {
    #           tokenAddress} does not exist.")
    #     print("Requesting transaction data...")
    #     tokenData = getPumpData(tokenAddress)

    #     with open(tokenDataFile, "w") as f:
    #         print("Saving transaction data...")
    #         json.dump(tokenData, f)


def getPumpData(tokenAddress):
    tokenDirectory = os.path.join("tokens", tokenAddress)

    if not os.path.exists(tokenDirectory):
        data = requestPumpTokenData(tokenAddress)

        if "statusCode" in data:
            print(f"Token {tokenAddress} is not a pump.fun coin.")
            return

        if data["complete"]:
            os.makedirs(tokenDirectory)
            print(f"Created directory for token {tokenAddress}.")
            savePumpTokenData(data)

        return data

    tokenDataFile = os.path.join("tokens", tokenAddress, "data.json")

    # There's no reason a data file wouldn't exist for a pump.fun token.
    # If the file was deleted, it's either the result of user interference
    # or data corruption. Either way, you'd have bigger problems to worry about.
    if os.path.exists(tokenDataFile):
        print(f"Data file exists for token {tokenAddress}")

        with open(tokenDataFile, "r") as f:
            fileData = json.load(f)
            return fileData

    # if not os.path.exists(tokenDirectory):
    #     os.makedirs(tokenDirectory)
    #     print(f"Created directory for token {tokenAddress}.")

    # tokenDataFile = os.path.join("tokens", tokenAddress, "data.json")

    # if os.path.exists(tokenDataFile):
    #     print(f"Data file exists for token {tokenAddress}.")

    #     with open(tokenDataFile, "r") as f:
    #         fileData = json.load(f)
    #         return fileData
    # else:
    #     print(f"There is no data file for token {tokenAddress}.")
    #     print("Requesting data...")

    #     data = requestPumpTokenData(tokenAddress)

    #     if data["complete"]:
    #         print(f"Downloaded and saved data for token {tokenAddress}.")
    #         savePumpTokenData(data)

    #     return data


def getPumpTransactionData(tokenData):
    tokenAddress = tokenData["mint"]
    print(f"Checking {tokenAddress}...")

    if tokenData["complete"] == False:
        return requestPumpTransactionData(tokenAddress)

    transactionDataFile = os.path.join(
        "tokens", tokenAddress, "transactions.json")

    if not os.path.exists(transactionDataFile):
        data = requestPumpTransactionData(tokenAddress)
        savePumpTransactionData(data)

        return data
    else:
        with open(transactionDataFile, "r") as f:
            return json.load(f)


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


def requestPumpComments(tokenAddress):
    # This may be useful to keep in a database in the future...
    r = requests.get(
        f"{PUMP_FUN_API_URL}/replies/{tokenAddress}?limit=10000&offset=0")

    return r.json()


def requestPumpTokenData(tokenAddress):
    r = requests.get(f"{PUMP_FUN_API_URL}/coins/{tokenAddress}")

    return r.json()


def requestPumpTransactionData(tokenAddress):
    r = requests.get(
        f"{PUMP_FUN_API_URL}/trades/all/{tokenAddress}?limit=10000&offset=0")

    return r.json()


def savePumpTokenData(data):
    tokenAddress = data["mint"]
    tokenDataFile = os.path.join("tokens", tokenAddress, "data.json")

    with open(tokenDataFile, "w") as f:
        json.dump(data, f)


def savePumpTransactionData(data):
    tokenAddress = data[0]["mint"]
    transactionDataFile = os.path.join(
        "tokens", tokenAddress, "transactions.json")

    with open(transactionDataFile, "w") as f:
        json.dump(data, f)


# ca = input("Enter token address: ")
# pumpComments = requestPumpComments(ca)
# print(pumpComments)
