# Community Catalyst

Community Catalyst is a crowdfunding platform that connects individuals and organizations with impactful projects in their communities. Users can discover, support, and create projects that make a difference in their local areas.

![Community Catalyst](/static/new_assets/img/logo.png)
## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Project Structure](#project-structure)
- [Tables Setup and migration](#Tables-Setup-And-Migration)
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



