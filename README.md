# 🌟 Menu Morpher: Transform Your Menu Management 🌟

![img.png](asset/menu_morpher.png)
## Description

Menu Morpher is a Python client for the Google My Business API focused on updating and downloading business menus. This tool allows businesses to easily manage and transform their menu data programmatically. No more hassle in finding your `account_id`, `location_id`, and reading Google API documentation! 

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.6 or higher
- pip (Python package installer)

## Installation

### Clone the Repository

Start by cloning the repository to your local machine:

```bash
git clone https://github.com/ericdwkim/Menu-Morpher.git
cd Menu-Morpher
```

## Setting Up Your Development Environment

You can set up your development environment using either `venv` (recommended for pure Python) or `Conda` (useful if you are managing dependencies that include non-Python packages).

### Using venv

If you don't have `virtualenv` installed, you can install it first:

```bash
python3 -m pip install --user virtualenv
python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

### Using conda

Create and activate a Conda environment:

```bash
conda create --name menumorpher python=3.8
conda activate menumorpher
```

### Install dependencies

```bash
pip install -r requirements.txt
```