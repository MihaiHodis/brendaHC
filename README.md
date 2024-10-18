# Brenda Home Cooking

Welcome to **Brenda Home Cooking** - an online bakery and home-cooking store where customers can explore a variety of freshly prepared cakes, cookies, savory snacks, and more. This web application is built using Flask for the backend, integrated with a MariaDB/MySQL database, and styled with Bootstrap for a sleek and responsive front-end experience.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Folder Structure](#folder-structure)
7. [Contributing](#contributing)
8. [License](#license)

## Project Overview

**Brenda Home Cooking** aims to provide an intuitive and visually appealing platform for customers to browse through categories of baked goods and specialty dishes. The app provides detailed product information, customer reviews, and allows easy navigation through multiple categories.

## Features

- **Dynamic Product Categories**: Users can browse multiple categories, such as Cakes, Cookies, Pastries, and more.
- **Product Reviews**: Customers can view and add reviews for different products.
- **Responsive Design**: The site is designed to be accessible on desktop, tablet, and mobile devices.
- **Admin-Friendly**: Easily add or update products and categories through the database.
- **API Support**: RESTful API for accessing product details.

## Installation

To get started, follow these steps:

### Prerequisites

- Python 3.9+
- MariaDB/MySQL
- Git

### Setup

1. **Clone the Repository**
   ```sh
   git clone git@github.com:YourUsername/brendaHC.git
   cd brendaHC
   ```

2. **Set up a Virtual Environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install Requirements**
   ```sh
   pip install -r requirements.txt
   ```

4. **Configure the Database**
   - Update the database connection settings in the `app/__init__.py` file.
   - Make sure you have created the database with the correct tables (`categorii` and `produse`). You can use the following SQL command to create the necessary tables:
   
   ```sql
   CREATE TABLE categorii (
     id INT PRIMARY KEY AUTO_INCREMENT,
     nume VARCHAR(100) NOT NULL,
     imagine VARCHAR(255) NOT NULL
   );
   
   CREATE TABLE produse (
     id INT PRIMARY KEY AUTO_INCREMENT,
     nume VARCHAR(100) NOT NULL,
     imagine VARCHAR(255) NOT NULL,
     categorie_id INT,
     pret DECIMAL(10, 2),
     descriere TEXT,
     FOREIGN KEY (categorie_id) REFERENCES categorii(id)
   );
   ```

5. **Run the Application**
   ```sh
   flask run --host=0.0.0.0 --port=5000
   ```

6. **Access in Browser**
   Open your browser and navigate to [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Usage

- Navigate through different product categories.
- Click on individual products for detailed descriptions.
- Add product reviews.

## API Endpoints

- **GET /api/produse**: Returns a JSON of available products.

Example Response:
```json
[
  { "id": 1, "nume": "Torturi", "imagine": "images/tort.jpg" },
  { "id": 2, "nume": "Prajituri", "imagine": "images/prajitura.jpg" }
]
```

## Folder Structure

- **/app**: Contains the Flask application files.
  - **__init__.py**: Initializes the app and manages the database connection.
  - **routes.py**: Contains all the routes for the application.
  - **/templates**: HTML files for rendering the different pages.
  - **/static**: Static resources like CSS, JS, and images.
- **run.py**: Main entry point for running the application.

## Contributing

Contributions are welcome! Please fork this repository and open a pull request with your changes. Make sure to follow the style guide and thoroughly test your additions.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

If you encounter any issues or have suggestions, feel free to create an issue on the GitHub repository or contact me directly.

