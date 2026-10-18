# Blood Bank Management System
A simple console-based application written in Python to manage blood donors, blood stock
and patient requests. All data is saved automatically in a local `data.json` file.
## Features
- Register donors (name, age, blood group, phone) with age validation (18-65)
- View all donors or search by blood group
- Record blood donations and update stock automatically
- View stock for all 8 blood groups with a low-stock warning
- Issue blood to patients (blocks requests that exceed available stock)
- Full transaction history (donations and issues)
- Delete donor records
- Persistent storage using JSON
## Requirements
- Python 3.8 or higher
- No external libraries needed
## How to Run
1. Clone the repository:
```bash
git clone https://github.com/&lt;your-username&gt;/blood-bank-management.git
cd blood-bank-management
```
2. Run the program:
```bash
python main.py
```
## Menu Options
| Option | Action |
|--------|--------|
| 1 | Add donor |
| 2 | View all donors |
| 3 | Search donors by blood group |
| 4 | Record a donation |
| 5 | View blood stock |
| 6 | Issue blood to patient |
| 7 | View transaction history |
| 8 | Delete donor |
| 0 | Exit |
## Project Structure

```
blood-bank-management/
├── main.py # Application code
├── README.md # Project documentation
├── .gitignore # Files ignored by Git
└── data.json # Created automatically on first save
```
## Future Improvements
- Blood expiry tracking (e.g. 42 days for red cells)
- Donor eligibility check based on last donation date
- Search by donor name or phone
- GUI using Tkinter or a web version using Flask
- Database support (SQLite)
## License
This project is open source and free to use for learning purposes.