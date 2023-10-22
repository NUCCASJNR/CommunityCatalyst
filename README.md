# Community Catalyst

Community Catalyst is a crowdfunding platform that connects individuals and organizations with impactful projects in their communities. Users can discover, support, and create projects that make a difference in their local areas.

![Community Catalyst](/templates/static/new_assets/img/logo.png)
## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Project Description

Community Catalyst is a web-based platform that empowers community leaders, activists, and organizations to create projects that require funding. These projects can range from local infrastructure improvements to educational initiatives. Users can explore, fund, and even collaborate on these projects.

### Features

- **Project Creation**: Users can create and launch their projects with descriptions, funding goals, and timelines.
- **Project Discovery**: Users can explore a wide range of community projects, filter by categories, and find those that resonate with them.
- **Fundraising**: Users can fund projects of their choice using various payment methods, making a real impact.
- **Collaboration**: Community members can join project teams, volunteer, or contribute their skills to bring the project to life.

## Getting Started

### Prerequisites

Before getting started, make sure you have the following prerequisites:

- Python 3
- pip
- MySQL

### Installation

1. **Clone the repository:**

```bash
git clone https://github.com/NUCCASJNR/CommunityCatalyst.git
cd CommunityCatalyst
```
2. **Install the requirements file**

```bash
pip install -r requirements.txt
```
3. **Set up the MySql user and database**

```mysql
cat setup_mysql_dev.sql | sudo mysql
```

4. **Set The environment variables required**

```bash
echo 'export COMMUNITY_USER="Community_Catalyst_user"' >> ~/.bashrc
echo 'export COMMUNITY_DB="Community_Catalyst_db"' >> ~/.bashrc
echo 'export COMMUNITY_PWD="Community_Catalyst_pwd"' >> ~/.bashrc
echo 'export COMMUNITY_HOST="localhost"' >> ~/.bashrc
```

5. **Source the Bashrc File to make the environment variables global**

```bash
source ~/.bashrc
```

### Project Structure

<ul>
    <li><strong>CommunityCatalyst</strong>
        <ul>
            <li><strong>api</strong>
                <ul>
                    <li><a href="api/app.py">app.py</a></li>
                    <li><a href="api/__init__.py">__init__.py</a></li>
                    <li>v1</li>
                      <ul><a href="api/v1/user.py">user.py</a></ul>
                </ul>
            </li>
            <li><a href="app.py">app.py</a></li>
            <li><a href="config.py">config.py</a></li>
            <li><a href="__pycache__">__pycache__</a></li>
            <li><strong>routes</strong>
                <ul>
                    <li><a href="routes/__init__.py">__init__.py</a></li>
                    <li><a href="routes/login.py">login.py</a></li>
                    <li><a href="routes/project.py">project.py</a></li>
                    <li><a href="routes/__pycache__">__pycache__</a></li>
                    <li><a href="routes/signup.py">signup.py</a></li>
                    <li><a href="routes/utils.py">utils.py</a></li>
                </ul>
            </li>
            <li><a href="tests">tests</a></li>
            <li><a href="utils">utils</a></li>
            <li><a href="automate.py">automate.py</a></li>
            <li><strong>forms</strong>
                <ul>
                    <li><a href="forms/login.py">login.py</a></li>
                    <li><a href="forms/project.py">project.py</a></li>
                    <li><a href="forms/__pycache__">__pycache__</a></li>
                    <li><a href="forms/signup.py">signup.py</a></li>
                </ul>
            </li>
            <li><a href="README.md">README.md</a></li>
            <li><a href="setup_mysql_dev.sql">setup_mysql_dev.sql</a></li>
            <li><strong>communitycatalyst</strong></li>
            <li><strong>models</strong>
                <ul>
                    <li><a href="models/base_model.py">base_model.py</a></li>
                    <li><a href="models/comment.py">comment.py</a></li>
                    <li><a href="models/__init__.py">__init__.py</a></li>
                    <li><a href="models/__pycache__">__pycache__</a></li>
                    <li><a href="models/category.py">category.py</a></li>
                    <li><a href="models/contribution.py">contribution.py</a></li>
                    <li><a href="models/project.py">project.py</a></li>
                    <li><a href="models/user.py">user.py</a></li>
                </ul>
            </li>
            <li><a href="requirements.txt">requirements.txt</a></li>
            <li><a href="templates">templates</a></li>
        </ul>
    </li>
</ul>
