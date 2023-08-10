import tkinter as tk
from tkinter import messagebox
import pyperclip
from password_generator import generate_password
from password_storage import save_password, get_password, get_available_ids, delete_password, delete_all_passwords, select_all_accounts

class PasswordManagerApp:
    def __init__(self, master, encryption_key, salt):
        self.master = master
        self.master.title("Password Manager")
        self.encryption_key = encryption_key
        self.salt = salt

        # Create and place widgets
        self.password_label = tk.Label(master, text="Generated Password:")
        self.password_label.pack()

        self.password_entry = tk.Entry(master)
        self.password_entry.pack()

        self.length_label = tk.Label(master, text="Password Length (8-128):")
        self.length_label.pack()

        self.length_entry = tk.Entry(master)
        self.length_entry.pack()

        self.account_label = tk.Label(master, text="Account Name:")
        self.account_label.pack()

        self.account_entry = tk.Entry(master)
        self.account_entry.pack()

        self.description_label = tk.Label(master, text="Account Description:")
        self.description_label.pack()

        self.description_entry = tk.Entry(master)
        self.description_entry.pack()

        self.generate_button = tk.Button(master, text="Generate Password", command=self.generate_password)
        self.generate_button.pack()

        self.save_button = tk.Button(master, text="Save Password", command=self.save_password)
        self.save_button.pack()

        self.id_label = tk.Label(master, text="Available IDs:")
        self.id_label.pack()

        self.id_listbox = tk.Listbox(master)
        self.id_listbox.pack()

        self.retrieve_button = tk.Button(master, text="Retrieve Password", command=self.retrieve_password)
        self.retrieve_button.pack()

        self.delete_button = tk.Button(master, text="Delete Password", command=self.delete_password)
        self.delete_button.pack()

        # Add "Delete All Passwords" button
        self.delete_all_button = tk.Button(master, text="Delete All Passwords", command=self.delete_all_passwords)
        self.delete_all_button.pack()

        self.show_all_button = tk.Button(master, text="Show All Accounts", command=self.show_all_accounts)
        self.show_all_button.pack()

        self.quit_button = tk.Button(master, text="Quit", command=self.quit_application)
        self.quit_button.pack()

        self.update_id_list()


    def generate_password(self):
        try:
            length = int(self.length_entry.get())
            if length < 8 or length > 128:
                raise ValueError("Password length should be between 8 and 128.")
            
            password = generate_password(length=length)
            self.password_entry.delete(0, tk.END)
            self.password_entry.insert(0, password)
            # Copy the generated password to the clipboard.
            # pyperclip.copy(password)
            # messagebox.showinfo("Password Generated", "Password has been generated and copied to the clipboard.")
        except ValueError as e:
            messagebox.showerror("Invalid Input", str(e))

    def save_password(self):
        password = self.password_entry.get()
        account_name = self.account_entry.get()  # Get the account name
        account_description = self.description_entry.get()  # Get the account description

        if not account_name:
            messagebox.showerror("Error", "Please enter an Account Name.")
            return

        # Prompt the user for the account description
        if account_description == "":
            # account_description = tkinter.simpledialog.askstring("Account Description", "Enter the Account Description:")
            account_description = "None"

        save_password(account_name, password, self.encryption_key, account_description)
        messagebox.showinfo("Password Saved", "Password has been saved securely.")
        self.update_id_list()

    def update_id_list(self):
        self.id_listbox.delete(0, tk.END)
        available_ids = get_available_ids()
        for account_name in available_ids:
            self.id_listbox.insert(tk.END, account_name)

    def retrieve_password(self):
        selected_index = self.id_listbox.curselection()
        if selected_index:
            selected_id = self.id_listbox.get(selected_index)
            passwords = get_password(selected_id, self.encryption_key)
            if passwords:
                password = passwords[-1]  # Display the most recent password
                self.password_entry.delete(0, tk.END)
                self.password_entry.insert(0, password)
                # Copy the retrieved password to the clipboard.
                pyperclip.copy(password)
                messagebox.showinfo("Password Retrieved", "Password has been retrieved and copied to the clipboard.")
            else:
                messagebox.showerror("Password Not Found", "No password found for the selected ID.")
        else:
            messagebox.showerror("Select an ID", "Please select an ID to retrieve the password.")
            
    def delete_password(self):
        selected_index = self.id_listbox.curselection()
        if selected_index:
            selected_id = self.id_listbox.get(selected_index)
            delete_password(selected_id, selected_index[0])
            messagebox.showinfo("Password Deleted", "Password has been deleted.")
            # Remove the selected ID from the listbox.
            self.id_listbox.delete(selected_index)
        else:
            messagebox.showerror("Select an ID", "Please select an ID to delete the password.")

    def delete_all_passwords(self):
        # Confirm with the user before deleting all passwords
        if messagebox.askyesno("Delete All Passwords", "Are you sure you want to delete all passwords?"):
            # Call the delete_all_passwords function from password_storage.py
            delete_all_passwords(self.encryption_key)
            # Update the password list in the interface after deletion
            self.update_id_list()

    def show_all_accounts(self):
        all_accounts = select_all_accounts()
        if all_accounts:
            # Create a multi-line string with account information
            formatted_accounts = "\n".join([f"Account Name: {account['account_name']}\nDescription: {account['account_description']}\nEncrypted Password: {account['encrypted_password']}\n" for account in all_accounts])

            # Create a new Toplevel window for the custom dialog box
            top = tk.Toplevel(self.master)
            top.title("All Accounts")
            
            # Set the window dimensions to the size of the screen
            width = self.master.winfo_screenwidth()
            height = self.master.winfo_screenheight()
            top.geometry(f"{width}x{height}")

            # Create a label to display the account information
            label = tk.Label(top, text=formatted_accounts, justify="left")
            label.pack(padx=10, pady=10)  # Add some padding for better appearance

            # Add a button to close the dialog box
            close_button = tk.Button(top, text="Close", command=top.destroy)
            close_button.pack(pady=10)
        else:
            messagebox.showinfo("All Accounts", "No accounts found.")

    def quit_application(self):
        # Ask for confirmation before quitting
        if messagebox.askyesno("Quit Application", "Are you sure you want to quit?"):
            self.master.destroy()