# It was dictionary the format data that often use in backend
data_user = {
    "id": 1,
    "username": "Hanif",
    "role": "Backend Engineer",
    "is_active": True
}

# Function to show the data
def get_data():
    print("Connecting to the server...")
    return data_user

# Call the function and print

profile = get_data()
print(profile)