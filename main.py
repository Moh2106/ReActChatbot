import os

from fastapi import FastAPI
from agents import Agent, GradioAgentPack

app = FastAPI()


@app.get("/")
async def root():
    GradioAgentPack.GradioReActAgentPack().run()
    """agent = Agent.Agent().initialize_agents()
    response = agent.chat("I want to claim about Laptop Basic I buy. The screen don't work")
    return print(response)"""



@app.get("/chat")
async def say_hello():
    """agent = Agent.Agent().initialize_agents()

    while True:
        text_input = input("User: ")
        if text_input == "exit":
            break
        response = agent.chat(text_input)
        print(f"Agent: {response}")"""
