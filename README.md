# Minesweeper

This project implements a Minesweeper game with a Vue.js frontend and Python Flask backend.

## Requirements

### Frontend
- Node.js (v14 or later recommended)
- Yarn package manager
- Vue.js 3
- TypeScript

### Backend
- Python 3.11
- Flask
- Flask-CORS
- unittest

## Setup

### Clone this repository

### Set up the frontend:
```bash
cd frontend
yarn install
```

### Set up the backend:
```bash
pip install flask
pip install flask-cors
```

## Setup

### Clone this repository

### Set up the frontend:
```bash
cd frontend
yarn install
```
## Running the Application

### Start the backend server:
```bash
cd backend
python main.py
```

### In a new terminal, start the frontend development server:
```bash
cd frontend
yarn serve
```
### Open a web browser and navigate to http://localhost:8080 (or the address shown in your terminal).

## Running Tests

To run backend tests:
```bash
cd backend
python -m unittest test_mine_sweeper_board.py
```