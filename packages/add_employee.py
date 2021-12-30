import pandas as pd
import argparse
import hashlib
from email_validator import validate_email, EmailNotValidError

from packages.check_password import check_password

def add_employee(email, password):
    
    df_employees = pd.read_csv(r"csv_files/employees.csv")
    db_employees = pd.read_csv(r"csv_files/db_employees.csv")

    #Check if the mail is written in a valid format
    
    try: 
        valid = validate_email(email)
        email = valid.email
        
        #Check if the domain is the correct one
        
        if "@gold1.com" not in email:
            print("Please enter an employee email. \n")

        else:
            check = False
            
            #Check if the employee is already registered
            
            for mail in db_employees["email"]:
                if mail == email:
                    check = True
                    print("This account is already registered. \n")
                    break

            #Check if the email is in the one allowed to register as an employee
            
            if check == False:     
                presence = False
                for mail in df_employees["email"]:
                    if email == mail:
                        presence = True
                        print('Your email allows you to register as an employee. \n')
                        
                        #Ask the employee to confirm the password he/she wants to use
                        
                        password_check = check_password(password)
                        if password_check == True:
                            
                            #Register the employee
                            
                            digest_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
                            new_df = pd.DataFrame({"email": [email], "password": [digest_password]})
                            db_employees = db_employees.append(new_df)
                            db_employees.to_csv(r'csv_files/db_employees.csv', index = False)
                            print("Registration was successful!. \n")
                        
                        break
                        

                if presence == False: 
                    print("We are sorry, this email is not allowed to register as an employee. \n")
                    
    except EmailNotValidError as e:
        print(str(e))
    
