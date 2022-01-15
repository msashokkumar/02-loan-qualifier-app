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

| Language      | Version       |
| ------------- |---------------|
| Python        | 3.7.11        |
### Libraries and Frameworks

| Component      | Version       |
| ------------- |---------------|
| Anaconda        | 1.9.0        |
| Conda        | 4.11.0       |

### Operating System

This vesion of Loan Qualifier App is operation system agnostic.

---

## Installation Guide

### Pre-requisites

- Python 3.7
- Anaconda 1.9.0
- Conda 4.11.0
- A conda environment created specially for this project.  We will refer to that environment as `dev` in this doc.

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

This section should include screenshots, code blocks, or animations explaining how to use your project.

![No Qualifying Loans](/images/no_qualifying_loans.png?raw=true "Files not saves when there are no qualifying loans.")

---

## Contributors

In this section, list all the people who contribute to this project. You might want recruiters or potential collaborators to reach you, so include your contact email and, optionally, your LinkedIn or Twitter profile.

---

## License

When you share a project on a repository, especially a public one, it's important to choose the right license to specify what others can and can't with your source code and files. Use this section to include the license you want to use.
