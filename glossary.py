import parlant.sdk as p

async def glossary(agent:p.Agent) -> None:
    
    await agent.create_term(
        name="Oceanfront Deluxe",
        description=(
                "A premium 450 sq ft room featuring a king-sized bed, private balcony, "
                "and direct unobstructed views of the ocean. Includes distinct amenities "
                "like a rainfall shower and complimentary minibar."
            ),
            synonyms=["Ocean View", "Deluxe Ocean", "Seaside Room", "Water View"]
    )
    
    await agent.create_term(
            name="Skyline Suite",
            description=(
                "Our signature 900 sq ft suite located on the top floors. "
                "Features panoramic city views, a separate living area, kitchenette, "
                "and exclusive access to the VIP Executive Lounge."
            ),
            synonyms=["Penthouse", "City View Suite", "VIP Suite", "Executive Suite"]
        )

    await agent.create_term(
            name="Adjoining Room",
            description=(
                "Two distinct rooms connected by a private internal door, allowing for "
                "combined living space without using the hallway. "
                "Must be requested specifically for families or groups."
            ),
            synonyms=["Connecting Room", "Family Connector", "Combined Room"]
        )

        # --- Cancellation & Policy Terms ---

    await agent.create_term(
        name="Flexible Rate",
        description=(
            "A booking rate that allows free cancellation or modification up to "
            "24 hours before the standard check-in time (3:00 PM local time). "
            "Cancellations after this window incur a one-night fee."
        ),
        synonyms=["Refundable Rate", "Standard Cancellation", "Free Cancellation"]
    )

    await agent.create_term(
        name="Non-Refundable Rate",
        description=(
            "A discounted rate that requires full payment immediately upon booking. "
            "No refunds, modifications, or cancellations are permitted under any "
            "circumstances, including medical emergencies."
        ),
        synonyms=["Prepaid Rate", "Saver Rate", "Advance Purchase", "Strict Cancellation"]
    )
    
    await agent.create_term(
            name="No-Show Policy",
            description=(
                "The policy applied when a guest fails to arrive by 11:59 PM on the "
                "scheduled check-in date without prior notice. The reservation is "
                "cancelled and the full cost of the stay is charged."
            ),
            synonyms=["Failure to Arrive", "Did Not Arrive"]
    )