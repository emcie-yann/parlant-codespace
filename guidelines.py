import parlant.sdk as p

async def guidelines(agent:p.Agent) -> None:
    
    await agent.create_guideline(
        condition="The customer asks what type of room you have",
        action="List the available room types and their features",
    )
    
    await agent.create_guideline(
        condition="The customer requests a standard room",
        action="Asks if they want any special services before confirming their booking"
    )
    
    await agent.create_guideline(
        condition="The user requests a cancellation of their booking",
        action="First express empathy and understanding for their change and explain the cancelation policy before proceeding with the cancellation"
    )