# This is the code for the Specific branch

import json
from datetime import datetime

def lambda_handler(event, context):
    # Extract JSON and target time from the input
    calendly_output = event['calendly_input']
    target_time = event['target_time']  # Expected in ISO 8601 format (e.g., "2024-11-26T17:30:00")

    # Parse the target time and make it offset-naive
    target_time_dt = datetime.fromisoformat(target_time)

    # Extract available time slots
    available_slots = []
    for day in calendly_output['days']:
        for spot in day['spots']:
            if spot['status'] == 'available':
                # Parse the start_time and make it offset-naive
                start_time = datetime.fromisoformat(spot['start_time']).replace(tzinfo=None)
                available_slots.append(start_time)

    # Sort slots by proximity to the target time
    available_slots.sort(key=lambda slot: abs(slot - target_time_dt))

    # Get the three closest slots
    closest_slots = available_slots[:3]

    # Sort the closest slots chronologically
    closest_slots.sort()
    available_slots.sort()

    # Format output to military time (HH:MM)
    closest_slots_str = [slot.strftime("%H:%M") for slot in closest_slots]
    available_slots_str = [slot.strftime("%H:%M") for slot in available_slots]

    return {
        'statusCode': 200,
        'closest_slots': closest_slots_str,
        'available_slots': available_slots_str
    }
