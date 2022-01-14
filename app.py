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

    # [['Bank of Big - Starter Plus', '300000', '0.85', '0.39', '700', '4.35'],
    #  ['West Central Credit Union - Starter Plus', '300000', '0.8', '0.44', '650', '3.9'],
    #  ['FHA Fredie Mac - Starter Plus', '300000', '0.85', '0.45', '550', '4.35'],
    #  ['FHA Fannie Mae - Starter Plus', '200000', '0.9', '0.37', '630', '4.2'],
    #  ['General MBS Partners - Starter Plus', '300000', '0.85', '0.36', '670', '4.05'],
    #  ['Bank of Fintech - Starter Plus', '100000', '0.85', '0.47', '610', '4.5'],
    #  ['iBank - Starter Plus', '300000', '0.9', '0.4', '620', '3.9'],
    #  ['Goldman MBS - Starter Plus', '100000', '0.8', '0.43', '600', '4.35'],
    #  ['Prosper MBS - Starter Plus', '100000', '0.9', '0.38', '640', '3.75'],
    #  ['Developers Credit Union - Starter Plus', '200000', '0.85', '0.46', '640', '4.2'],
    #  ['Bank of Stodge & Stiff - Starter Plus', '100000', '0.8', '0.35', '680', '4.35']]

    save_csv_file = questionary.confirm("Do you want to save the qualifying loans as a csv file?").ask()

    if save_csv_file:
        if len(qualifying_loans):

            try_file_create = True
            count = 0

            while try_file_create:

                # Try 3 times until a unique file name that doesn't already exist is received.
                count += 1

                if count > 3:
                    print("Maximum attempts reached for creating a new file.")
                    print("Exiting. Please try again later.")
                    exit(0)

                output_csvpath = questionary.text("Enter a file path to store the csv file (.csv):").ask()
                output_csvpath = Path(output_csvpath)

                if output_csvpath.is_file():
                    print("File path already exists. Please enter an unique file name.")
                else:
                    try_file_create = False

            save_csv_file_confirm = questionary.confirm(f"Output will be stored to {output_csvpath}. Proceed?").ask()

            if save_csv_file_confirm:
                output_csv_path = write_csv(output_csvpath, csv_header, qualifying_loans)
            else:
                print("Output not saved to a csv file. Goodbye!")
        else:
            print("No qualifying loans to save. Good bye!")


def display_banner():
    """Display a welcome banner in CLI
    Ref: https://pypi.org/project/terminal-banner/
    """
    banner_text = "Welcome to \n\n Loan Qualifier App!"
    my_banner = tb.Banner(banner_text)
    print(my_banner)


def run():
    """The main function for running the script."""

    # TODO: Banner fails when then output is not
    # display_banner()

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
