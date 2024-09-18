# HomeHub

## Introduction

Welcome to **HomeHub**  a platform designed to connect house agents and users seeking to rent house, in the housing market. Agents can sign up and post vacant homes available for rent, while users seeking houses can browse through these listings, view detailed information, and contact agents directly using their provided phone numbers.

- **Live Site**: [HomeHub Live](https://devnonso.pythonanywhere.com/home/)
- **Project Blog**: [Project Blog Article](https://docs.google.com/document/d/1EfhvIjUeUxMG1Ahbo_aJodXzKdT7KUXZQn37nOUYYyQ/edit?usp=sharing)
- **Authors**: 
  - [Tochukwu Ilonuba](https://www.linkedin.com/in/tochukwu-ilonuba-831088185)
  - [Chinonso Ogbonnaya](https://www.linkedin.com/in/chinonso-ogbonnaya-024931297)
  - [Sulaiman Fatai](https://www.linkedin.com/in/fatai-sulaiman-93818b65)

## Installation

To set up the project locally, follow these steps:

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Tochukwu92/HomeHub.git
    cd homehub
    ```

2. **Set up a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables** (create a `.env` file):
    ```
    FLASK_APP=run.py
    FLASK_ENV=development
    SECRET_KEY=your_secret_key
    DATABASE_URL=your_database_url
    ```

5. **Set up the database**:
    ```bash
    flask db upgrade
    ```

6. **Run the application**:
    ```bash
    flask run
    ```

The application should now be running on `http://127.0.0.1:5000/`.

## Usage

- **Agents**: Sign up and log in to post available properties with detailed information and images. Manage your listings directly through the account dashboard.
- **Users**: Browse available properties, view detailed property descriptions, and contact agents for more information.

## Contributing

We welcome contributions! Here's how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Push your branch and submit a pull request.

Please make sure to follow coding standards and write clear commit messages.

## Related Projects

- [kwaralist](https://kwaralist.com.ng)
- [Propertylisthub](https://propertylisthub.com/projects/)
- [adron homes](https://adronhomesproperties.com)

## License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for more details.
