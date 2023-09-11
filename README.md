<div align="center">

  # Eventside

  An event management web application where users can browse, create and manage events.
  
  ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)&nbsp;
  ![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)&nbsp;
  ![jQuery](https://img.shields.io/badge/jquery-%230769AD.svg?style=for-the-badge&logo=jquery&logoColor=white)&nbsp;
  ![Bootstrap](https://img.shields.io/badge/bootstrap-%238511FA.svg?style=for-the-badge&logo=bootstrap&logoColor=white)

![eventside](https://github.com/ottohellwig/eventside/assets/105997582/202f8965-bbd0-434e-b895-785d49bd2cfb)

</div>

## Description

Eventside is a music event management web application developed with Flask, SQLite, jQuery and Bootstrap. The web app is dynamic and gives users a wide range of control from user registration/login, event creation and management to purchasing tickets. The project is built with the Flask framework and uses Flask-SQLAlchemy to interact with a SQLite database for querying and storage. jQuery is used for dynamic loading and features like searching or filtering. The Bootstrap framework was used for the UI with many elements such as the modals, buttons and navbar being assets from the CSS framework. This was an entry-level project that was designed with a MVC architecture and developed further from a high fidelity prototype, any contributions or ideas on improvements that could be made, would be greatly appreciated.

## Features

<details>
  <summary>
    <i>Click to view features</i>
  </summary>
  <p>

  - Flask-SQLAlchemy DB interaction
  - SQLite database
  - jQuery dynamic loading
  - Flask-WTF forms
  - Bootstrap elements
  - Event and user management
  - MVC architecture

  </p>
</details>

## Installation

If you want to make changes or have a local version, you will need to do the following:

1. Clone the repo
  ```
  $ git clone https://github.com/ottohellwig/eventside.git
  $ cd eventside
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv --no-site-packages env
  $ source env/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ python main.py
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

## Contributing

Contributions (Issues/PRs/Discussions) are the driver of improvements in projects. Any contributions you make are greatly appreciated.
