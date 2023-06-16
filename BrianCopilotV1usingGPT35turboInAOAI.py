# Brian Copilot version 1.1.0
# This uses Azure OpenAI service and the GPT 3.5 model
# Note: The openai-python library support for Azure OpenAI is in preview.
# Sign in using az login

import os
import openai
import json

from azure.identity import DefaultAzureCredential
# from azure.identity import AzureCliCredential # this is used in Azure Notebook
from azure.keyvault.secrets import SecretClient

openai.api_type = "azure"
openai.api_base = "https://blstech-azureopenai.openai.azure.com/" # Your Azure OpenAI API endpoint
openai.api_version = "2023-03-15-preview"
deployment_name = "GPT35turbo" # Your Azure OpenAI deployment name

# Create an instance of the DefaultAzureCredential class to authenticate with Azure
credential = DefaultAzureCredential()
# Create an instance of the AzureCliCredential class to authenticate with Azure - this is used in Azure Notebook
# credential = AzureCliCredential()

# Set the name of your Key Vault and the name of your secret
key_vault_name = "blstech-kv1" # Your Key Vault name
secret_name = "AzureOpenAI-API" # Your Key Vault secret name

# Create an instance of the SecretClient class to retrieve the secret
secret_client = SecretClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)

# Retrieve the API key from Azure Key Vault
api_key = secret_client.get_secret(secret_name).value

openai.api_key = api_key

def generate_response_and_store(user_input_array, response_array):
    user_input = "\n".join(user_input_array)
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        temperature=1.0,
        max_tokens=200,
        n=1,
        stop=None,
        messages=[
            {"role": "system", "content": "You are a helpful cybersecurity assistant."},
            {"role": "user", "content": user_input},
        ]
    )
    generated_text = response.choices[0]['message']['content']
    response_array.append(generated_text)
    return generated_text.strip()

response_array = []
user_input_array = []  # Create an empty array to store user input

print('The completion is using GPT3.5 model in Azure OpenAI API service') 
while True:
    print('Please enter an input prompt: (enter "exit" to quit)')
    user_input = input()
    if user_input == "exit":
        break
    user_input_array.append(user_input)  # Add user input to array

    user_output = generate_response_and_store(user_input_array, response_array)
    response_array.append(user_output)
    print(user_output)