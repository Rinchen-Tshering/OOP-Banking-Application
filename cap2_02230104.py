######################################################
#Rinchen Tshering
#First Year Electronics and communication Engineering (1ECE)
#02230104
######################################################
#Refrences 
#https://youtu.be/tJxcKyFMTGo?si=Wunl2JSweuQVY6EV
#https://youtu.be/HkLhYKp8YfE?si=dC3RGuVABIzXCQI_
#https://youtu.be/rq8cL2XMM5M?si=C6B-UDnbnTo8yVIK 
######################################################

import random  # Importing the random module for generating random account numbers and passwords
import os  # Importing the os module for file operations

class Account:
    # Initialize an account with account number, type, and balance
    def __init__(self, account_number, account_type, balance=0):
        self.account_number = account_number
        self.password = self.generate_password()  # Generate a default password
        self.account_type = account_type
        self.balance = balance

    # using static method to generate a random account number
    @staticmethod
    def generate_account_number():
        return str(random.randint(1000000000, 9999999999))

    # using static method to generate a random password
    @staticmethod
    def generate_password():
        return str(random.randint(1000, 9999))

    # Deposit an amount into the account
    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance is {self.balance}.")
        else:
            print("Deposit amount must be positive.")

    # Withdraw an amount from the account
    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance is {self.balance}.")
        else:
            print("Insufficient funds or invalid amount.")

    # Check the current balance
    def check_balance(self):
        print(f"Current balance: {self.balance}")

    # Convert account details to a dictionary format
    def to_dict(self):
        return {
            "account_number": self.account_number,
            "password": self.password,
            "account_type": self.account_type,
            "balance": self.balance
        }

# Create a subclass for BusinessAccount
class BusinessAccount(Account):
    def __init__(self, account_number, balance=0):
        super().__init__(account_number, "Business", balance)

# Create subclass for PersonalAccount
class PersonalAccount(Account):
    def __init__(self, account_number, balance=0):
        super().__init__(account_number, "Personal", balance)

class BankSystem:
    def __init__(self):
        self.accounts = {}  # create a dictionary to store account information
        self.load_accounts()  # Load existing accounts from file

    # Method to load accounts from a file
    def load_accounts(self):
        if os.path.exists("accounts.txt"):  # Check if the file exists
            with open("accounts.txt", "r") as f:
                for line in f:
                    account = eval(line.strip())
                    if account['account_type'] == "Business":
                        acc = BusinessAccount(account['account_number'], account['balance'])
                    else:
                        acc = PersonalAccount(account['account_number'], account['balance'])
                    acc.password = account['password']
                    self.accounts[account['account_number']] = acc

    # Save accounts to a file
    def save_accounts(self):
        with open("accounts.txt", "w") as f:
            for account in self.accounts.values():
                f.write(str(account.to_dict()) + "\n")

    # Create a new account
    def create_account(self, account_type):
        account_number = Account.generate_account_number()  # Generate a new account number
        if account_type == "Business":
            new_account = BusinessAccount(account_number)
        else:
            new_account = PersonalAccount(account_number)
        self.accounts[account_number] = new_account  # Add the new account to the dictionary
        self.save_accounts()  # Save the updated accounts to the file
        print(f"Account created successfully! Account Number: {account_number}, Password: {new_account.password}")

    # Method to log in to an existing account
    def login(self, account_number, password):
        if account_number in self.accounts and self.accounts[account_number].password == password:
            print("Login successful.")
            return self.accounts[account_number]
        else:
            print("Invalid account number or password.")
            return None

    # Method to delete an account
    def delete_account(self, account_number):
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_accounts()
            print("Account deleted successfully.")
        else:
            print("Account not found.")

    # Method to transfer money between accounts
    def transfer_money(self, from_account, to_account_number, amount):
        if from_account.balance >= amount:
            if to_account_number in self.accounts:
                to_account = self.accounts[to_account_number]
                from_account.withdraw(amount)
                to_account.deposit(amount)
                self.save_accounts()
                print(f"Transferred {amount} to account {to_account_number}.")
            else:
                print("Receiving account not found.")
        else:
            print("Insufficient funds.")

def main():
    bank_system = BankSystem()  # Create an instance of BankSystem

    while True:
        print("\n1. Create Account\n2. Login\n3. Exit")
        choice = input("Enter choice: ")

        if choice == "1":
            account_type = input("Enter account type (Personal/Business): ")
            bank_system.create_account(account_type)  # Create a new account

        elif choice == "2":
            account_number = input("Enter account number: ")
            password = input("Enter password: ")
            account = bank_system.login(account_number, password)  # Log in to an existing account
            if account:
                while True:
                    print("\n1. Deposit\n2. Withdraw\n3. Check Balance\n4. Transfer Money\n5. Delete Account\n6. Logout")
                    choice = input("Enter choice: ")

                    if choice == "1":
                        amount = float(input("Enter amount to deposit: "))
                        account.deposit(amount)  # Deposit money

                    elif choice == "2":
                        amount = float(input("Enter amount to withdraw: "))
                        account.withdraw(amount)  # Withdraw money

                    elif choice == "3":
                        account.check_balance()  # Check balance

                    elif choice == "4":
                        to_account_number = input("Enter receiving account number: ")
                        amount = float(input("Enter amount to transfer: "))
                        bank_system.transfer_money(account, to_account_number, amount)  # Transfer money

                    elif choice == "5":
                        bank_system.delete_account(account.account_number)  # Delete account
                        break

                    elif choice == "6":
                        print("logged out successfully")
                        break

        elif choice == "3":
            print("Thank you for using the app")
            break

if __name__ == "__main__":
    main()
