    # Ensure data is a dictionary
    if isinstance(data, dict):
        # Use get method to safely access the 'temp' key
        temp = data.get('temp', default_value)
    else:
        # Handle the case where data is not a dictionary
        temp = default_value
    
    # Replace default_value with an appropriate default value
    default_value = None  # or any other value that makes sense in your context
