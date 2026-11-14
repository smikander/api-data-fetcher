import requests

def validate_name(name):
    if isinstance(name, str):
        name = name.strip()
        return bool(name)
    return False

def validate_email(email):
    if isinstance(email, str):
        email = email.strip()
        at_count = email.count("@") == 1
        if email and at_count:
            localpart, domain = email.split("@")
            if (localpart 
                and domain 
                and "." in domain 
                and not domain.endswith(".") 
                and not domain.startswith(".") 
                and " " not in email):
                return True      
    return False

def process_users(users):
    if isinstance(users, list):
        for user in users:
            if not isinstance(user, dict):
                print("Virheellinen käyttäjätieto")
                continue
            name = user.get("name")
            if validate_name(name):
                print("Nimi:", name)
            else:
                print("Virheellinen nimi")    
            email = user.get("email")
            if validate_email(email):
                print("Sähköposti:", email)
            else:
                print("Virheellinen sähköposti")      
    else:
        print("API palautti virheellisen tietorakenteen")    

def fetch_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url, timeout=5)
    response.raise_for_status()  
    return response.json()                    
    
if __name__ == "__main__":
    try:
        users = fetch_users()
        process_users(users)


    except requests.exceptions.JSONDecodeError as error:
        print("API palautti virheellistä JSON-dataa:", error)       

    except requests.exceptions.RequestException as error:
        print("API-pyyntö epäonnistui:", error) 
