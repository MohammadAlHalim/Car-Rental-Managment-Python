import time
import random
import re
import smtplib
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#reading cars.txt 
cars=[]
file=open("cars.txt","r")
for line in file:
    car_nb,car_name, car_amount, price_per_day=line.replace("\n","").replace("_"," ").split("|",3)
    car=[car_nb,car_name,car_amount,price_per_day]
    cars+=[car]
file.close()

#reading cars_specs.txt 
cars_specs=[]
file=open("cars_specs.txt","r")
for line in file:
    cars_name, horsepower, seating_capacity, fuel_efficiency=line.replace("\n","").split("|",3)
    car_spec=[cars_name, horsepower, seating_capacity, fuel_efficiency]
    cars_specs+=[car_spec]
file.close()

#reading rented_cars.txt
rented_cars=[]
file=open("rented_cars.txt","r")
for line in file:
    rented_car_nb,rented_car_name,rented_car_amount=line.replace("\n","").split("|",2)
    rented_car=[rented_car_nb,rented_car_name,rented_car_amount]
    rented_cars+=[rented_car]
file.close()

# printing our logo
print ("""
                      ██╗          ██║   ██║██║██║██║   ██║██║       ██║   ██║██║██║██║      ██║██║██║██║   ██║██║██║██║██║
                      ██║          ██║   ██║      ██║   ██║ ██║      ██║   ██║       ██║     ██║            ██║           ██║
                      ██║    ██║   ██║   ██║      ██║   ██║  ██║     ██║   ██║        ██║    ██║            ██║           ██║
                      ██║    ██║   ██║   ██║██║██║██║   ██║   ██║    ██║   ██║         ██║   ██║██║██║██║   ██║██║██║██║██║
                      ██║  ██║██║  ██║   ██║      ██║   ██║    ██║   ██║   ██║         ██║   ██║            ██║         ██║
                      ██║ ██║  ██║ ██║   ██║      ██║   ██║     ██║  ██║   ██║       ██║     ██║            ██║         ██║   
                      ██║██║    ██║██║   ██║      ██║   ██║       ██║██║   ██║██║██║██║      ██║██║██║██║   ██║         ██║        


                    ██║          ██║   ██║         ██║   ██║██║██║██║   ██║██║██║██║   ██║           ██║      ██║██║██║██║██║
                    ██║          ██║   ██║         ██║   ██║            ██║            ██║             ██║    ██║
                    ██║    ██║   ██║   ██║         ██║   ██║            ██║            ██║                    ██║██║██║██║██║
                    ██║    ██║   ██║   ██║██║██║██║██║   ██║██║██║██║   ██║██║██║██║   ██║                    ██║██║██║██║██║                         
                    ██║  ██║██║  ██║   ██║         ██║   ██║            ██║            ██║                                ██║
                    ██║ ██║  ██║ ██║   ██║         ██║   ██║            ██║            ██║                                ██║
                    ██║██║    ██║██║   ██║         ██║   ██║██║██║██║   ██║██║██║██║   ██║██║██║██║██         ██║██║██║██║██║

    """)

# stating the real time the program was excuted
current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print("\nProgram executed at:", current_time)

print("Hello, inorder to continue please select one of the options listed below.")
USER_DB_FILE = "user_database.txt"

def load_user_database():
    user_database = {}
    try:
        with open(USER_DB_FILE, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(',')
                if len(parts) == 3:
                    username, email, password = parts
                    user_database[username] = {'email': email, 'password': password}
    except FileNotFoundError:
        # If the file doesn't exist, return an empty database
        pass
    return user_database

def save_user_database(user_database):
    with open(USER_DB_FILE, 'w') as file:
        for username, info in user_database.items():
            file.write(f"{username},{info['email']},{info['password']}\n")

def is_valid_email(email):
    # Define a simple email format validation using regular expression
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    return bool(re.match(email_pattern, email))

def signup():
    print("Sign Up")

    while True:
        username = input("Enter your username: ")

        # Check if the username already exists
        if username in user_database:
            print("Username already exists. Please choose a different username.")
        else:
            break  # Exit the loop if the username is unique

    while True:
        user_email = input("Enter your email address: ")

        # Validate the entered email address
        if is_valid_email(user_email):
            break  # Exit the loop if a valid email is entered
        else:
            print("Error: Invalid email address format. Please enter a valid email.")

    while True:
        password = input("Enter your password (at least 6 characters): ")
        confirm_password = input("Confirm your password: ")

        # Check if the passwords match
        if password == confirm_password and len(password) >= 6:
            break  # Exit the loop if the passwords match and the password is at least 6 characters long
        else:
            print("Error: Passwords do not match or password is less than 6 characters. Please try again.")

    # Store user information in the database
    user_database[username] = {'email': user_email, 'password': password}
    save_user_database(user_database)
    print(f"Welcome, {username}! Sign up successful.")

def login():
    print("Log In")

    while True:
        username = input("Enter your username: ")

        # Check if the username exists
        if username not in user_database:
            print("Username not found.")
            signup()  # Force the user to sign up if the username is not found
        else:
            break  # Exit the loop if the username is found

    if username in user_database:
        while True:
            entered_password = input("Enter your password: ")

            # Compare the entered password with the stored password
            if entered_password == user_database[username]['password']:
                print(f"Welcome, {username}!")
                break  # Exit the loop if the passwords match
            else:
                print("Incorrect password. Please try again.")

# Load existing user database or create an empty one
user_database = load_user_database()

while True:
    print("Choose an option:")
    print("1. Sign Up")
    print("2. Log In")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        signup()
        break
    elif choice == '2':
        login()
        break
    else:
        print("Invalid choice. Please enter 1 or 2:")


#here, the program introduces to the user our services, and lets him decide what to do
print()
print("\nWelcome to WanderWheels, where seamless journeys begin with our exceptional rental car services, ensuring you explore with comfort and style at every turn.")
print("""\nThe road is yours to shape. Please consider:\n
1. Embrace the adventure and explore our curated services.
2. Seek personalized guidance by contacting our dedicated customer support.
\nMake your selection by entering the corresponding number and let your journey unfold with us.\n""")

selection_nb=input("Please select: ")
print('⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺')

while selection_nb!="exit":
    
    if selection_nb=="1":
        print("\nWanderWheels Menu:")
        print("1. Display available cars")
        print("2. Rent a car")
        print("3. Return a car")
        print("4. Exit")
        print()
        choice = (input("Enter your choice (1-4): "))
        print('⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺')
        
        if choice=="1":
            
            print()
            print("Available cars in our shop: ")
            print()
            for i in range(0,len(cars)):
                print(i+1,')  ',cars_specs[i][0], "------ amount: ", cars[i][2], sep="")

            x=0
            print()
            enter_car=input("Do you want to see car specs(yes/no)? ")
            while enter_car!="no":
                x=0
                car_name=input("Enter a valid car name: ")
                for i in range(0, len(cars_specs)):
                    if cars_specs[i][0].lower()==car_name.lower():
                        x=1
                        print(cars_specs[i][0], "specs: ")
                        print("Horsepower:", cars_specs[i][1])
                        print("Seating Capacity:", cars_specs[i][2])
                        print("Fuel Efficiency (l/km)", cars_specs[i][3])
                        enter_car=input("Do you want to see another car specs(yes/no)? ")
            
                if x==0:
                    print("The input you have adressed is unvailable!!")
                   
            
            

        if choice=="2":
            print("|" + "-" * 13 + "|" + "-" * 32 + "|" + "-" * 8 + "|" + "-" * 15 + "|")
            print("| {:<11} | {:<30} | {:<6} | {:<13} |".format("Car Number", "Car Name", "Amount", "Price per Day"))
            print("|" + "-" * 13 + "|" + "-" * 32 + "|" + "-" * 8 + "|" + "-" * 15 + "|")
            for i, car in enumerate(cars, start=1):
                print("| {:<11} | {:<30} | {:<6} | {:<13} |".format(i, cars_specs[i-1][0], car[2], f"${car[3]}"))
            print("|" + "-" * 13 + "|" + "-" * 32 + "|" + "-" * 8 + "|" + "-" * 15 + "|")   
            print()
            rent_a_car=int(input("Kindly select your preferred car for rental by specifying its corresponding number from the table above: "))

            while rent_a_car>len(cars) or rent_a_car<=0:
                print("Invalid Number!!")
                rent_a_car=int(input("Kindly select a valid input(1-50): "))

            while int(cars[rent_a_car-1][2])==0:
                print("Sorry, This car is not available!!")
                rent_a_car=int(input("Kindly select another option: "))   

            if int(cars[rent_a_car-1][2])!=0:
                print("You have selected", cars_specs[rent_a_car-1][0])
                rent_duration=int(input("Kindly provide the number of days you wish to rent the car for: "))
                
                
                print()
                A="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                a="abcdefghijklmnopqrstuvwxyz"
                numbers="0123456789"
                captcha=""
                for i in range(2):
                    captcha+=random.choice(A)+random.choice(a)+random.choice(numbers)

                print(captcha)
                verification_user=input("Enter the kaptcha code above: ")

                while verification_user!=captcha:
                    captcha=""
                    for i in range(2):
                        captcha+=random.choice(A)+random.choice(a)+random.choice(numbers)
                    print("Oops!! Verification failed. ")
                    print()
                    print(captcha)
                    verification_user=input("Enter the kaptcha code above: ")
                print("Verificaition completed.")
                print()

                total_steps = 50  

                for i in range(1, total_steps + 1):
                    progress = i / total_steps
                    percentage = int(progress * 100)
                    bar_length = int(progress * 50)  
                    bar = "=" * bar_length + "-" * (50 - bar_length)
    
                    print(f"\r[{bar}] {percentage}%", end='', flush=True)
                    time.sleep(0.1)
                cars[rent_a_car-1][2]=str(int(cars[rent_a_car-1][2])-1)
                rented_cars[rent_a_car-1][2]=str(int(rented_cars[rent_a_car-1][2])+1)
                file=open("cars.txt","w")
                for i in range(len(cars)):
                    string1=str(cars[i]).replace("'","").replace("[","").replace("]","").replace(",","|").replace(" ","")+"\n"
                    file.write(string1)
                file.close()
                file=open("rented_cars.txt","w")
                for i in range(len(rented_cars)):
                    string2=str(rented_cars[i]).replace("'","").replace("[","").replace("]","").replace(",","|").replace(" ","")+"\n"
                    file.write(string2)
                file.close()

                print("\nCongrats on your rental!")
                print()
                print()
                print("                      ====== Your reciept ======")
                print()
                print("*Car NB:", rent_a_car)
                print("*Car name:", cars_specs[rent_a_car-1][0])
                print("*Rented days:", rent_duration )
                print("*Total price: $",int(cars[rent_a_car-1][3])*rent_duration)
                date_of_rental=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print()
                print("*Thank you for choosing WanderWheels. Your rental period begins on", date_of_rental)
                print()
                print('⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺⸺')
                HOST = "smtp-mail.outlook.com"
                PORT = 587
                From_Email = "wanderwheelsco@outlook.com"
                To_Email = input("Please enter your email: ")
                # Avoid using getpass for password input
                password ="kasvmomhjpbxdpzi"
                subject = "Thank you for your rent"
                message_body = f'''*Car NB: {rent_a_car}
*Car name: {cars_specs[rent_a_car-1][0]}
*Rented days: {rent_duration}
*Total price: ${int(cars[rent_a_car-1][3])*rent_duration}'''

                # Create a MIMEText object to represent the email body
                msg = MIMEMultipart()
                msg['From'] = From_Email
                msg['To'] = To_Email
                msg['Subject'] = subject
                msg.attach(MIMEText(message_body, 'plain'))
                try:
                    smtp = smtplib.SMTP(HOST, PORT)
                    
                    status_code, response = smtp.ehlo()
                    
                    status_code, response = smtp.starttls()
                    
                    status_code, response = smtp.login(From_Email, password)
                    
                    smtp.sendmail(From_Email, To_Email, msg.as_string())

                    smtp.quit()
                    print("[*] Script completed.")
                except Exception as e:
                    print(f"[*] An error occurred: {e}")
                finally:
                    if 'smtp' in locals() and smtp:
                        try:
                            smtp.quit()
                            print("")
                        except smtplib.SMTPServerDisconnected:
                            print("")

        if choice=="3":
            return_car=int(input("Based on the above table, please enter the number of the car you would like to return: "))
            while int(rented_cars[return_car-1][2])<=0:
                print("Sorry, This car cannot be returned!!")
                return_car= int(input("Please enter a valid number of the car you would like to return: "))
            for i in range(0,len(rented_cars)):
                if str(return_car) in rented_cars[i][0]:
                    rented_cars[return_car-1][2]=str(int(rented_cars[return_car-1][2])-1)
                    for j in range(0,len(cars)):
                        if str(return_car) in cars[j][0]:
                            cars[j][2]=str(int(cars[j][2])+1)
            print("proccesing") 
            total_steps = 20
            for i in range(1, total_steps + 1):
                progress = i / total_steps
                percentage = int(progress * 100)
                bar_length = int(progress * 20)
                bar = "=" * bar_length + "-" * (20 - bar_length)
                print(f"\r[{bar}] {percentage}%", end='', flush=True)
                time.sleep(0.1)
            print()
            print("Congratulations, You have successfully returned the car!!")
            file=open("rented_cars.txt","w")
            for i in range(len(rented_cars)):
                string2=str(rented_cars[i]).replace("'","").replace("[","").replace("]","").replace(",","|").replace(" ","")+"\n"
                file.write(string2)
            file.close()
            file=open("cars.txt","w")
            for i in range(len(cars)):
                string1=str(cars[i]).replace("'","").replace("[","").replace("]","").replace(",","|").replace(" ","")+"\n"
                file.write(string1)
            file.close()
        if choice=="4":
            total_steps = 20
            for i in range(1, total_steps + 1):
                progress = i / total_steps
                percentage = int(progress * 100)
                bar_length = int(progress * 20)
                bar = "=" * bar_length + "-" * (20 - bar_length)
                print(f"\r[{bar}] {percentage}%", end='', flush=True)
                time.sleep(0.1)
            print("\nYou have successfully exited the program!")
            break
    # costumer support feature  
    elif selection_nb=="2":
        print("Need help? Our customer support team is ready to assist you. Call us at 01 234 567 for immediate assistance or drop us an email at custsupport@wanderwheels.com for a prompt response.")
        print()
        print("""For assistance tailored to your needs, contact our dedicated team:

Sales Inquiries: 09 876 543
Technical Support: 03 134 246
              
Feel free to reach out via email as well:

General Inquiries: info@wanderwheels.com
Sales: sales@wanderwheels.com
Technical Support: techsupport@wanderwheels.com
We're here to help you in any way we can!""")
        print()
        break

    else:
        print("Whoops!! It appears there's a hiccup in the data you entered. Please review and try once more")
        print()
        selection_nb=input("Please select either 1 or 2: ")

print("You have successfully exited the program!!")