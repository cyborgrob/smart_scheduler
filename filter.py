import json
from datetime import datetime, timedelta


def lambda_handler(event, context):
    # Extract data from the event
    calendly_data = event['calendly_data']
    preferences = event['preferences']

    # Extract day and time preferences
    day_preference = preferences[0]['day_preference']
    time_preference = preferences[0]['time_preference']
    specific_time = preferences[0].get('specific_time')
    spec_time_pref = preferences[0].get('spec_time_pref')

    # Map days to their abbreviations
    day_map = {
        "M": 0,  # Monday
        "T": 1,  # Tuesday
        "W": 2,  # Wednesday
        "Th": 3,  # Thursday
        "F": 4  # Friday
    }

    # Helper function to filter based on time preference
    def filter_by_time(time_preference, specific_time, spec_time_pref, start_time):
        time = datetime.strptime(start_time, "%Y-%m-%dT%H:%M:%S%z").time()
        if time_preference == "M":  # Morning
            return time < datetime.strptime("12:00", "%H:%M").time()
        elif time_preference == "A":  # Afternoon
            return time >= datetime.strptime("12:00", "%H:%M").time()
        elif time_preference == "E":  # Evening
            return time >= datetime.strptime("18:00", "%H:%M").time()
        elif time_preference == "S":  # Specific time
            # Parse the specific time into a datetime object for comparison
            specific_time_obj = datetime.strptime(specific_time, "%H:%M").time()
            if spec_time_pref == "B":  # Before the specific time
                return time < specific_time_obj
            elif spec_time_pref == "A":  # After or at the specific time
                return time >= specific_time_obj
            elif spec_time_pref == "O":  # At/around the specific time (within 1 hour)
                # Convert times to datetime objects for easier time math
                specific_time_dt = datetime.strptime(specific_time, "%H:%M")
                start_time_dt = datetime.combine(datetime.today(), time)
                lower_bound = specific_time_dt - timedelta(hours=1)
                upper_bound = specific_time_dt + timedelta(hours=1)
                return lower_bound.time() <= time <= upper_bound.time()
        return True  # No preference

    # Helper function to filter based on day preference
    def is_preferred_day(date, day_preference):
        day_index = datetime.strptime(date, "%Y-%m-%d").weekday()
        return any(day_index == day_map[d] for d in day_preference)

    def convert_to_readable_dates(appointments):
        """
        Converts ISO 8601 datetime strings to a human-readable format.

        :param appointments: List of ISO 8601 datetime strings
        :return: List of human-readable datetime strings
        """
        readable_appointments = []
        for appointment in appointments:
            # Parse the ISO 8601 datetime string into a datetime object
            dt = datetime.strptime(appointment, "%Y-%m-%dT%H:%M:%S%z")

            # Format the datetime into the desired human-readable format
            formatted_date = dt.strftime("%A, %B %d at %I:%M%p")  # Use %I for 12-hour format with leading zero

            # Strip leading zero from the hour if present
            if formatted_date[formatted_date.index("at") + 3] == "0":
                formatted_date = formatted_date.replace("at 0", "at ")            

            readable_appointments.append(formatted_date)
        return readable_appointments

    filtered_appointments = []
    for day in calendly_data['days']:
        if is_preferred_day(day['date'], day_preference):  # Match preferred day
            for spot in day['spots']:
                if filter_by_time(time_preference, specific_time, spec_time_pref, spot['start_time']): # Match preferred time
                    filtered_appointments.append(spot['start_time'])
                    if len(filtered_appointments) >= 4:  # Limit to 4 appointments
                        return {
                            "filtered_appointments": convert_to_readable_dates(filtered_appointments)
                        }

    filtered_appointments = convert_to_readable_dates(filtered_appointments)

    return {
        "filtered_appointments": filtered_appointments
    }
