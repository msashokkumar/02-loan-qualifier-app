# -*- coding: utf-8 -*-
"""Loan Qualifier Application.

This is a command line application to match applicants with qualifying loans.

Example:
    $ python app.py
"""
import sys
import fire
import questionary
from pathlib import Path
import terminal_banner as tb

from qualifier.utils.fileio import load_csv, write_csv

from qualifier.utils.calculators import (
    calculate_monthly_debt_ratio,
    calculate_loan_to_value_ratio,
)

from qualifier.filters.max_loan_size import filter_max_loan_size
from qualifier.filters.credit_score import filter_credit_score
from qualifier.filters.debt_to_income import filter_debt_to_income
from qualifier.filters.loan_to_value import filter_loan_to_value


def load_bank_data():
    """Ask for the file path to the latest banking data and load the CSV file.

    Returns:
        The bank data from the data rate sheet CSV file.
    """

    csvpath = questionary.text("Enter a file path to a rate-sheet (.csv):").ask()
    csvpath = Path(csvpath)
    if not csvpath.exists():
        sys.exit(f"Oops! Can't find this path: {csvpath}")

    return load_csv(csvpath)


def get_applicant_info():
    """Prompt dialog to get the applicant's financial information.

    Returns:
        Returns the applicant's financial information.
    """

    credit_score = questionary.text("What's your credit score?").ask()
    debt = questionary.text("What's your current amount of monthly debt?").ask()
    income = questionary.text("What's your total monthly income?").ask()
    loan_amount = questionary.text("What's your desired loan amount?").ask()
    home_value = questionary.text("What's your home value?").ask()

    credit_score = int(credit_score)
    debt = float(debt)
    income = float(income)
    loan_amount = float(loan_amount)
    home_value = float(home_value)

    return credit_score, debt, income, loan_amount, home_value


def find_qualifying_loans(bank_data, credit_score, debt, income, loan, home_value):
    """Determine which loans the user qualifies for.

    Loan qualification criteria is based on:
        - Credit Score
        - Loan Size
        - Debit to Income ratio (calculated)
        - Loan to Value ratio (calculated)

    Args:
        bank_data (list): A list of bank data.
        credit_score (int): The applicant's current credit score.
        debt (float): The applicant's total monthly debt payments.
        income (float): The applicant's total monthly income.
        loan (float): The total loan amount applied for.
        home_value (float): The estimated home value.

    Returns:
        A list of the banks willing to underwrite the loan.

    """

    # Calculate the monthly debt ratio
    monthly_debt_ratio = calculate_monthly_debt_ratio(debt, income)
    print(f"The monthly debt to income ratio is {monthly_debt_ratio:.02f}")

    # Calculate loan to value ratio
    loan_to_value_ratio = calculate_loan_to_value_ratio(loan, home_value)
    print(f"The loan to value ratio is {loan_to_value_ratio:.02f}.")

    # Run qualification filters
    bank_data_filtered = filter_max_loan_size(loan, bank_data)
    bank_data_filtered = filter_credit_score(credit_score, bank_data_filtered)
    bank_data_filtered = filter_debt_to_income(monthly_debt_ratio, bank_data_filtered)
    bank_data_filtered = filter_loan_to_value(loan_to_value_ratio, bank_data_filtered)

    print(f"Found {len(bank_data_filtered)} qualifying loans")

    return bank_data_filtered


def save_qualifying_loans(csv_header, qualifying_loans):
    """Saves the qualifying loans to a CSV file.

    Args:
        csv_header(list): Header row from the input csv file.
        qualifying_loans (list of lists): The qualifying bank loans.
    """
    # Prompt the  user if they want to save the qualifying loans as a csv file
    save_csv_file = questionary.confirm("Do you want to save the qualifying loans as a csv file?").ask()

    if save_csv_file:
        # Save results to csv file only if there are qualifying loans.
        # If there are no qualifying loans, alter the user and exit.
        if len(qualifying_loans):

            try_file_create = True
            file_create_attempt = 0

            # Keep trying until a unique file name is provided.
            # The user gets 3 attempts before the app exits.
            while try_file_create:

                # Try 3 times until a unique file name that doesn't already exist is provided.
                # If there are more than 3 attempts, quit and prompt user to retry.
                file_create_attempt += 1

                if file_create_attempt > 3:
                    print("Maximum failed attempts reached for creating a new file.")
                    print("Exiting. Please try again later.")
                    exit(0)

                output_csvpath = questionary.text("Enter a file path to store the csv file (.csv):").ask()
                output_csvpath = Path(output_csvpath)

                # Check if the file name provided by the user already exists.
                # If so, prompt the user to provide a new name.
                if output_csvpath.is_file():
                    print("File path already exists. Please enter an unique file name.")
                else:
                    try_file_create = False

            # Please confirm with the user if they want to save the file to the given location.
            # This provides the user an option to abort from saving the file.
            save_csv_file_confirm = questionary.confirm(f"Output will be stored to {output_csvpath}. Proceed?").ask()

            if save_csv_file_confirm:
                # write_csv is defined in qualifier/utils/fileio.py
                output_csv_path = write_csv(output_csvpath, csv_header, qualifying_loans)
                print(f"Qualifying loans saved to {output_csv_path}. Goodbye!")
            else:
                print("Output not saved to a csv file. Goodbye!")
        else:
            print("No qualifying loans to save. Good bye!")


def display_banner():
    """Display a welcome banner in CLI
    Ref: https://pypi.org/project/terminal-banner/
    """
    banner_text = "Welcome to \n\nLoan Qualifier App!\nNow with option to save output as a csv file."
    my_banner = tb.Banner(banner_text)
    print(my_banner)


def run():
    """The main function for running the script."""

    # TODO: Banner fails when the output target is not stdout
    display_banner()

    # Load the latest Bank data and headers from the input csv file
    csv_header, bank_data = load_bank_data()

    # Get the applicant's information
    credit_score, debt, income, loan_amount, home_value = get_applicant_info()

    # Find qualifying loans
    qualifying_loans = find_qualifying_loans(
        bank_data, credit_score, debt, income, loan_amount, home_value
    )

    # Save qualifying loans
    save_qualifying_loans(csv_header, qualifying_loans)


if __name__ == "__main__":
    fire.Fire(run)
