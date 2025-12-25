import parlant.sdk as p

@p.tool
async def check_room_availability(context: p.ToolContext) -> p.ToolResult:
    
    # Return a simulated result
    return p.ToolResult({
        "status": "Available",
        "price_per_night": 250,
        "currency": "USD"
    })
    
@p.tool
async def confirm_booking(context: p.ToolContext) -> p.ToolResult:
    # Generate a dummy confirmation code
    confirmation_code = "RES-987654"
    
    return p.ToolResult({
        "confirmation_code": confirmation_code,
        "message": "Booking confirmed successfully."
    })