# Loan Qualifier App

The loan qualifier by itself is a handy tool which provides loan qualifications by considering the following factors:

1. Daily Rate Sheet
2. User's Credit Score
3. User's monthly debt
4. User'smonthly income
5. Desired Loan Amount
6. User's home value

Based on the above factors, the tool show how many loans the user qualifies - but does not show the loans themselves
that the user qualifies for. This projects presents a utility that provides the application user the option to to save 
the loans that the user qualifies for as a csv file.

The application user will be able to:
- Store the qualifier output as a csv file in the location they wish.
- Cancel saving the output to a csv file after providing the file name.

The app will not store the result as csv file if:
- there are no qualifying loans for the user.
- the output csv file name is not unique. 

The application user will have 3 attempts to provide a unique name. After 3 failed attempts, the app will exit.

---

## Technologies

Loan Qualifier App is an application built with the following technologies:

### Language

| Language | Version |
|----------|---------|
| Python   | 3.7.11  |
### Libraries and Frameworks

| Component | Version |
|-----------|---------|
| Anaconda  | 1.9.0   |
| Conda     | 4.11.0  |

### Operating System

This version of Loan Qualifier App is operating system agnostic.

---

## Installation Guide

### Pre-requisites

- Python 3.7
- Anaconda 1.9.0
- Conda 4.11.0
- A conda environment created specially for this project.  We will refer to that environment as `dev` in this doc.

### Installation

```bash
conda create --name dev python=3.7
conda activate dev
```

Install the following python module in the `dev` conda environment:

```bash
pip install fire
pip install questionary
```

Alternatively the modules can be installed via requirements.txt file as:

```bash
cd <path_to_dir>/02_loan_qualifier_app
pip install -r requirements.txt
```

---

## Usage

Clone the repository to a base location on your laptop. In examples shown below, the base location is
`/Users/ashok/berkley/fintech-workspace/`. 

```bash
git clone git@github.com:msashokkumar/02_loan_qualifier_app.git
```

To run the application, please use the complete path of the file `app.py`. 

```bash
conda activate dev
python /Users/ashok/berkley/fintech-workspace/02_loan_qualifier_app/app.py
```

When the qualifier app determines there are qualifying loans, its prompts the user if they want to save the output to a 
csv file. If yes, it will prompt for the file name. Once the file name is provided, the app will require confirmation to go
ahead and save the csv file. The user can choose to not save the file at this time.

![Opt out of saving](/media/images/qualifying_loans_out_out_save.png?raw=true "User can opt out of saving the csv file even after providing the file name.")

If the user chooses to save the file, the csv file will be stored in the location provided.

![Qualifying Loans](/media/images/qualifying_loans_unique_path.png?raw=true "File saved when there are qualifying loans and unqiue file name provided.")

The application user has 3 attempts fo provide a unique file name after which the app will exit. If unique file name is
provided within 3 attempts, the csv file will be stored.

![Unique Filename Required](/media/images/qualifying_loans_unique_path_attempts_failed.png?raw=true "3 failed attempts of providing a unique name will result in app exiting.")

If there are no qualifying loans for the user, the app will not try to save the csv file and will exit.

![No Qualifying Loans](/media/images/no_qualifying_loans.png?raw=true "Files not saves when there are no qualifying loans.")

---
## Contributors

```markdown
{
  "name": "Ashok Kumar Madhavi Selvaraj",
  "email": "ashok.ms.kumar@gmail.com",
  "linkedin": "https://www.linkedin.com/in/msashokkumar"
}
```
---

## License

Please refer to LICENSE.
