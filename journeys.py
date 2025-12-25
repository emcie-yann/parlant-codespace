import parlant.sdk as p
import tools

async def journey(agent: p.Agent) -> None:
    journey = await agent.create_journey(
        title="Book Hotel Room",
        conditions=["The customer wants to book a room"],
        description="Guides the user through checking availability and confirming a hotel reservation.",
    )

    # Start -> Ask for Dates
    step_dates = await journey.initial_state.transition_to(
        chat_state="Ask the guest for their desired check-in and check-out dates."
    )

    # Dates -> Ask for Room Type
    step_room_type = await step_dates.target.transition_to(
        chat_state="Ask which room type they prefer (Standard, Deluxe, or Suite)."
    )

    # Room Type -> Check Availability (Tool)
    step_check_avail = await step_room_type.target.transition_to(
        tool_instruction="Check availability for the requested dates and room type.",
        tool_state=tools.check_room_availability,
    )

    _step_not_avail = await step_check_avail.target.transition_to(
        condition="The room is not available",
        chat_state="Apologize and ask for alternative dates or a different room type.",
    )

    step_avail = await step_check_avail.target.transition_to(
        condition="The room is available",
        chat_state="Inform the guest the room is available and ask for the full name for the reservation.",
    )

    step_confirm = await step_avail.target.transition_to(
        chat_state="Present the full booking details (Dates, Room, Name) and ask for final confirmation."
    )

    step_finalize = await step_confirm.target.transition_to(
        condition="Guest confirms the booking", tool_state=tools.confirm_booking
    )

    # Book It -> Goodbye
    await step_finalize.target.transition_to(
        chat_state="Provide the booking confirmation number and wish them a pleasant stay."
    )
