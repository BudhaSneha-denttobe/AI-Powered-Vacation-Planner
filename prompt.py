def build_prompt(destination, days, budget, travel_type):
    return f"""
You are an expert AI travel planner.

Create a {days}-day personalized trip plan for {destination}.

Traveler type: {travel_type}
Budget: {budget}

Include:
- Day-wise itinerary
- Famous attractions
- Local food recommendations
- Budget estimation
- Travel tips
- Best time to visit

Make the response creative, friendly, and detailed.
"""
