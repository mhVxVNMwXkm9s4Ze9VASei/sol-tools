from pf import getPumpData, getPumpTransactionData
from funcs import getCurrentISOTime, duplicateFile
import json
import os


def getInputTokens(fileName):
    inputFileName = f"{fileName}.txt"
    inputFile = os.path.join("mutuals", "inputs", inputFileName)

    if not os.path.exists(inputFile):
        print(f"There is no file named {fileName}.txt in the input folder!")
        return

    currentTime = getCurrentISOTime()
    outputFolder = os.path.join("mutuals", "inputs", fileName)

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    outputFileName = f"{fileName}_{currentTime}.txt"
    outputFile = os.path.join("mutuals", "inputs", fileName, outputFileName)
    duplicateFile(inputFile, outputFile)

    with open(inputFile, "r") as f:
        tokens = f.read().splitlines()
        return tokens


def getMutuals(tokens):
    wallets = {}

    for token in tokens:
        tokenData = getPumpData(token)
        transactionData = getPumpTransactionData(tokenData)
        tokenInfo = f"{token} ({tokenData["symbol"]})"

        for transaction in transactionData:
            user = transaction["user"]
            wallets.setdefault(user, {"tokens": [tokenInfo], "hitRate": 1})

            if tokenInfo not in wallets[user]["tokens"]:
                wallets[user]["tokens"].append(tokenInfo)
                wallets[user]["hitRate"] += 1

    filtered = {user: info for user, info in sorted(wallets.items(
    ), key=lambda x: x[1]["hitRate"], reverse=True) if len(info["tokens"]) > 1}

    return filtered


def saveOutputTokens(inputName, data):
    outputFolder = os.path.join("mutuals", "outputs", inputName)

    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)

    formattedTime = getCurrentISOTime()
    outputFileName = f"{formattedTime}.json"
    outputFilePath = os.path.join(
        "mutuals", "outputs", inputName, outputFileName)

    with open(outputFilePath, "w") as f:
        json.dump(data, f, indent=4)
        print(f"Successfully saved data for {inputName} in {outputFileName}!")


inputFile = input(
    "Enter the name of the file with the tokens you wish to check: ")
tokens = getInputTokens(inputFile)
mutuals = getMutuals(tokens)
saveOutputTokens(inputFile, mutuals)
print(f"Saved found wallets in mutuals/outputs/{inputFile}.txt!")
