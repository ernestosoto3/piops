# Python Development Environment Setup

This document records the steps I followed to establish and verify the Python development environment for the `piops` project.

The goal of this stage was to create an isolated Python environment on the Raspberry Pi and verify that Python, pip, the virtual environment, Git, and my VS Code Remote SSH workflow could work together correctly.

During this stage, I:

- Verified the installed Python version.
- Learned how `pip` is used to manage Python packages.
- Installed and verified `pip`.
- Created a Python virtual environment.
- Used the virtual environment through my VS Code Remote SSH workflow.
- Added the virtual environment to `.gitignore`.
- Researched possible structures for the project as it grows.
- Verified that packages were being installed inside the virtual environment.
- Created `check_env.py` to inspect and verify the Python environment.
- Considered Tailscale as a possible future addition for remote access.

> **Note:** Personal information, usernames, hostnames, IP addresses, and machine-specific paths have been removed or generalized in this documentation.

---

## 1. Verifying the Python Installation

Before creating the development environment, I checked which Python installations were available on the Raspberry Pi.

```bash
ls /usr/bin/python*
```

I then checked the active Python version:

```bash
python --version
```

At the time of this setup, the Raspberry Pi reported:

```text
Python 3.13.5
```

This confirmed that Python was already installed and available.

---

## 2. Understanding and Installing pip

The next step was preparing Python package management.

`pip` is Python's package installer. It allows me to install and manage external Python packages that are not included with the Python standard library.

For example:

```bash
pip install <package-name>
```

Before installing `pip`, I refreshed the Raspberry Pi's package information:

```bash
sudo apt update
```

The system reported that all packages were up to date, so I did not need to install additional system upgrades at that point.

I then installed pip for Python 3:

```bash
sudo apt install python3-pip
```

After installation, I verified it with:

```bash
pip --version
```

The installed version reported during this setup was:

```text
pip 25.1.1
```

and it was associated with Python 3.13.

---

## 3. Why I Am Using a Virtual Environment

Instead of installing every Python package globally on the Raspberry Pi, I decided to use a virtual environment for the project.

A Python virtual environment provides an isolated Python environment for a specific project.

This gives me several benefits:

- Project dependencies remain separated from system-level Python packages.
- Different projects can use different package versions.
- Packages that are only needed for one project do not clutter the global Python environment.
- The project's dependencies can later be documented and reproduced.
- I reduce the risk of creating conflicts with packages required by the operating system.

A virtual environment is not another running operating system or virtual machine. It primarily provides an isolated Python environment and package location.

This is useful for `piops`, especially because I want to keep the Raspberry Pi's limited resources and system installation as clean as possible.

---

## 4. Creating the Virtual Environment

I created the virtual environment inside the project repository.

The general command is:

```bash
python -m venv <environment-name>
```

For this project, I chose `.venv`:

```bash
python -m venv .venv
```

This created:

```text
piops/
└── .venv/
```

The `.venv` directory contains the project's isolated Python environment.

If I need to completely remove the environment, I can delete it with:

```bash
rm -rf .venv
```

Because `.venv` will not be stored in Git, the long-term goal is for the project's required dependencies to be documented separately so the environment can be recreated when necessary.

---

## 5. Activating and Deactivating the Environment

I activate the virtual environment with:

```bash
source .venv/bin/activate
```

After activation, commands such as:

```bash
python
```

and:

```bash
pip
```

use the virtual environment.

When I am finished, I can leave the environment with:

```bash
deactivate
```

---

## 6. Using the Virtual Environment with VS Code Remote SSH

An important part of this stage was making sure the Python virtual environment worked with the Remote SSH workflow I established previously.

My workflow is:

```text
Development Computer
        │
        │ VS Code Remote SSH
        ▼
   Raspberry Pi
        │
        ▼
     piops/
        │
        └── .venv/
              └── Python environment
```

VS Code runs on my development computer while Remote SSH allows me to open and work with the files stored on the Raspberry Pi.

The Python environment also remains on the Raspberry Pi.

This means I can use VS Code as my development interface while the actual project and Python interpreter run remotely on the Pi.

The virtual environment's Python interpreter is located at:

```text
.venv/bin/python
```

This allows the terminal, Python interpreter, installed packages, and VS Code development environment to work together on the Raspberry Pi.

---

## 7. Creating the Initial `.gitignore`

Because `.venv` contains locally generated files and installed packages, I do not want Git to track it.

I created a `.gitignore` containing:

```gitignore
# Virtual Environment
.venv/
```

At this stage, this is the **only entry in my `.gitignore`**.

I intentionally decided not to copy a large pre-generated Python `.gitignore` template.

During my research, I found other entries commonly used in Python projects, such as:

```gitignore
__pycache__/
*.py[cod]
.env
.vscode/
.idea/
.DS_Store
```

However, I have **not added these entries yet**.

My current approach is to expand `.gitignore` as the project develops and as these files become relevant. This allows me to understand why each entry exists instead of starting with a large list of exclusions that the project may never use.

---

## 8. Researching the Future Project Structure

I also researched how Python projects are commonly structured.

One structure I considered was the `src/` layout:

```text
my_project/
├── src/
│   └── my_package/
│       ├── __init__.py
│       ├── main.py
│       └── module.py
├── tests/
│   ├── __init__.py
│   └── test_module.py
├── docs/
├── .gitignore
├── pyproject.toml
├── README.md
└── LICENSE
```

In this type of structure:

- `src/` contains the Python source code.
- `tests/` contains automated tests.
- `docs/` contains project documentation.
- `.gitignore` defines files Git should not track.
- `pyproject.toml` can contain Python project metadata and configuration.
- `README.md` provides the main repository documentation.
- `LICENSE` defines how the project can legally be used or distributed.

I decided that a structured layout like this could make sense as `piops` becomes larger.

However, **I have not created this entire structure yet**.

I do not want to add directories or configuration files simply because they are considered standard. I want the repository structure to grow based on what the project actually needs.

---

## 9. Verifying the Active Python Environment

After creating and activating `.venv`, I verified which Python executable was being used:

```bash
which python
```

The result pointed inside:

```text
<project-directory>/.venv/bin/python
```

I also checked pip:

```bash
pip -V
```

Its location also pointed inside the `.venv` directory.

This confirmed that both Python and pip were using the virtual environment rather than the system-level Python environment.

---

## 10. Testing Package Isolation

I wanted to verify that packages installed with pip while the environment was active were actually being stored inside `.venv`.

For this test, I installed `requests`:

```bash
pip install requests
```

The installation completed successfully.

I then checked where Python was loading the package from:

```bash
python -c "import requests; print(requests.__file__)"
```

The returned location pointed inside:

```text
<project-directory>/.venv/lib/python3.13/site-packages/
```

This confirmed that `requests` had been installed inside the project's virtual environment rather than globally on the Raspberry Pi.

---

## 11. Understanding Python Environment Detection

After manually verifying the environment, I wanted to understand how I could check the same information from Python.

I used Python's built-in `sys` module:

```python
import sys
```

Two useful values are:

```python
sys.prefix
sys.base_prefix
```

### `sys.prefix`

`sys.prefix` shows the prefix for the Python environment currently being used.

When my virtual environment is active, this points to `.venv`.

### `sys.base_prefix`

`sys.base_prefix` identifies the base Python installation from which the virtual environment was created.

Because the two values are different when running inside my virtual environment, I can check:

```python
in_venv = sys.prefix != sys.base_prefix
```

When I am running the script using the virtual environment, this should return:

```text
True
```

---

## 12. Checking the Python Executable

I can also use:

```python
sys.executable
```

to see the exact Python executable currently running the program.

Inside my virtual environment, I expect it to point to:

```text
.venv/bin/python
```

This gives me another way to verify that my program is using the expected Python installation.

---

## 13. Checking `VIRTUAL_ENV`

I also researched how the shell identifies an activated virtual environment.

When I activate `.venv`, the activation script normally sets the environment variable:

```text
VIRTUAL_ENV
```

Python's `os` module gives me access to environment variables:

```python
import os
```

I can retrieve `VIRTUAL_ENV` with:

```python
venv_path = os.environ.get("VIRTUAL_ENV")
```

I then display it using:

```python
print(f"VIRTUAL_ENV: {venv_path or 'Not set'}")
```

If `venv_path` contains a value, Python displays it.

If it does not, the `or` expression causes:

```text
Not set
```

to be displayed instead.

---

## 14. Creating `check_env.py`

After researching the individual checks, I created a small Python program named:

```text
check_env.py
```

I added this file to the repository as a simple way to inspect the Python environment.

My current script is:

```python
import sys
import os

print("=== Virtual Environment Check ===\n")

# 1. Check if inside a venv
in_venv = sys.prefix != sys.base_prefix # Verifies if the current installation is different than the base
print(f"In virtual environment: {in_venv}")

# 2. Show key paths
print(f"Python executable:  {sys.executable}")
print(f"sys.prefix:         {sys.prefix}")
print(f"sys.base_prefix:    {sys.base_prefix}")

# 3. Show VIRTUAL_ENV variable
venv_path = os.environ.get("VIRTUAL_ENV")
print(f"VIRTUAL_ENV:        {venv_path or 'Not set'}") # Gets the variable from .environ

# 4. Test that pip works
import subprocess
result = subprocess.run(
    [sys.executable, "-m", "pip", "--version"],
    capture_output=True, text=True
)
print(f"\npip: {result.stdout.strip()}")

# 5. Test a basic import
try:
    import json
    print(f"\nStandard library import (json): OK")
except ImportError:
    print("\nStandard library import (json): FAILED")

print("\n=== Done ===")
```

The script performs five checks.

### 1. Virtual environment detection

```python
in_venv = sys.prefix != sys.base_prefix
```

This compares the current Python environment with the base Python installation.

### 2. Python paths

The script displays:

```python
sys.executable
sys.prefix
sys.base_prefix
```

This allows me to see exactly which Python installation and environment are being used.

### 3. `VIRTUAL_ENV`

The script checks:

```python
os.environ.get("VIRTUAL_ENV")
```

to see whether the shell has set the virtual environment variable.

### 4. pip

The script executes:

```text
python -m pip --version
```

using the same Python executable that is currently running `check_env.py`.

Using:

```python
sys.executable
```

helps ensure that I am checking pip for the same Python interpreter running the script.

### 5. Standard library import

Finally, I import Python's built-in `json` module.

This provides a simple check that the interpreter can successfully import a standard-library module.

The purpose of `check_env.py` is not to perform application functionality yet. It is a small verification program that helped me understand and confirm how the Python environment is configured.

---

## 15. Current Repository State

At the end of this stage, the relevant repository structure is approximately:

```text
piops/
├── docs/
├── test/
├── .gitignore
├── check_env.py
└── README.md
```

Locally, the repository also contains:

```text
.venv/
```

but Git does not track this directory because of the `.gitignore` rule.

Conceptually:

```text
piops/
├── .venv/             # Local only — ignored by Git
├── docs/              # Development documentation
├── test/
├── .gitignore
├── check_env.py       # Python environment verification
└── README.md
```

This is intentionally still a small repository.

Rather than creating a large project structure immediately, I am building the repository alongside the actual requirements of `piops`.

---

## 16. Future Consideration: Remote Access with Tailscale

During this stage, I also started considering how I could access the Raspberry Pi when I am outside my local network.

One possible solution I identified is Tailscale.

My current SSH workflow depends on being able to reach the Raspberry Pi over the network. Tailscale could potentially allow me to reach the Raspberry Pi remotely without directly exposing the Pi's SSH port to the public internet.

I have **not implemented Tailscale as part of this stage**.

Before adding it, I want to evaluate:

- How it fits into the overall `piops` project.
- Its resource usage on my Raspberry Pi.
- Its security model.
- How it would change my SSH workflow.
- Whether another continuously running service is justified on the Raspberry Pi.

I may implement and document remote access as a separate stage of the project.

---

## 17. What I Completed

During this stage, I successfully:

1. Verified the Raspberry Pi's Python installation.
2. Installed and verified pip.
3. Researched the purpose and benefits of Python virtual environments.
4. Created `.venv` for the project.
5. Activated and deactivated the virtual environment.
6. Used the virtual environment through my VS Code Remote SSH workflow.
7. Added `.venv/` to `.gitignore`.
8. Researched possible future Python project structures.
9. Verified the Python executable used by `.venv`.
10. Verified the pip installation used by `.venv`.
11. Installed `requests` inside the virtual environment.
12. Confirmed that the package was installed inside `.venv`.
13. Learned how `sys.prefix`, `sys.base_prefix`, `sys.executable`, and `VIRTUAL_ENV` can be used to inspect a Python environment.
14. Created and added `check_env.py` to verify the development environment.

This gives `piops` a working Python development environment while keeping the repository itself intentionally simple.

---

## References

The following resources were used during my research for this stage:

- [Dot Linux — How to Check Python Version on Raspberry Pi](https://www.dotlinux.net/blog/how-to-check-python-version-on-raspberry-pi/)
- [Pi My Life Up — Installing pip on Raspberry Pi](https://pimylifeup.com/raspberry-pi-pip/)
- [Raspberry Pi Forums — Python and pip Discussion](https://forums.raspberrypi.com/viewtopic.php?p=2381694)
- [Raspberry Pi Documentation — Raspberry Pi OS](https://www.raspberrypi.com/documentation/computers/os.html)
- [SunFounder — Access Raspberry Pi Remotely with Tailscale](https://www.sunfounder.com/blogs/news/how-to-access-raspberry-pi-remotely-with-tailscale-no-port-forwarding)
- [Tech Insider — Tailscale Setup](https://tech-insider.org/ca/how-to-set-up-tailscale-2026/)
- [GeeksforGeeks — How to Create a `.gitignore` File](https://www.geeksforgeeks.org/git/how-to-create-gitignore-file/)