# Raspberry Pi Development Environment Setup

This document records the steps I followed to prepare my Raspberry Pi for development and connect it to my GitHub workflow.

The goal of this setup was to establish a development environment where I can:

- Access the Raspberry Pi remotely through SSH.
- Keep the Raspberry Pi's software up to date.
- Install and configure Git.
- Authenticate with GitHub using SSH.
- Clone and manage GitHub repositories directly from the Raspberry Pi.
- Connect to the Raspberry Pi through Visual Studio Code using Remote SSH.
- Edit, commit, and push code from the Raspberry Pi development environment.

> **Note:** Personal information, IP addresses, SSH keys, email addresses, and other machine-specific information have been removed or replaced with placeholders.

---

## 1. Verifying Raspberry Pi Connectivity

Before connecting to the Raspberry Pi, I checked whether the device was reachable on my local network.

```bash
ping <pi-hostname>.local
```

A successful response indicates that the Raspberry Pi is reachable over the network.

I then connected to it using SSH:

```bash
ssh <pi-user>@<pi-hostname>.local
```

This gave me remote terminal access to the Raspberry Pi.

---

## 2. Updating the System

Before installing additional development tools, I updated the Raspberry Pi's package information.

```bash
sudo apt update
```

`apt update` refreshes the local package index so the system knows which package versions are currently available from its configured repositories. It does **not** install those updates.

I then installed the available package upgrades:

```bash
sudo apt upgrade
```

During my setup, this updated packages related to OpenSSL and Raspberry Pi configuration utilities, including:

- `libssl3t64`
- `openssl-provider-legacy`
- `openssl`
- `raspi-config-core`
- `raspi-config`

After the upgrade completed, I ran:

```bash
sudo apt update
```

again to confirm that the package information was current.

> Raspberry Pi's current documentation recommends `sudo apt full-upgrade` for normal Raspberry Pi OS system updates because it can handle dependency changes that a standard `apt upgrade` may not. I used `apt upgrade` during this setup and am documenting the command I actually ran.

---

## 3. Installing Git

I wanted Git installed directly on the Raspberry Pi so I could track changes and interact with GitHub repositories from the device.

I installed Git using:

```bash
sudo apt install git
```

The installation completed successfully.

At the time of this setup, the installed package reported Git version `2.47.3`.

I verified the installation with:

```bash
git --version
```

---

## 4. Basic Git Commands

Some of the Git commands I will use throughout the project include:

### Stage changes

```bash
git add <filename>
```

To stage all changed files:

```bash
git add .
```

### Commit changes

```bash
git commit -m "Describe the changes"
```

### Push commits

```bash
git push origin <branch-name>
```

### Pull remote changes

```bash
git pull origin <branch-name>
```

These commands form part of the basic workflow I will use to track the project's development.

---

## 5. Configuring My Git Identity

After installing Git, I configured the identity Git associates with my commits.

```bash
git config --global user.name "<github-username>"
git config --global user.email "<email-associated-with-git>"
```

I then verified the configuration:

```bash
git config --list
```

This confirmed that Git had stored my global configuration.

---

## 6. Configuring GitHub SSH Authentication

Instead of authenticating with GitHub every time I interact with the repository, I configured SSH authentication between the Raspberry Pi and GitHub.

### Check for existing SSH keys

I first checked whether the Raspberry Pi already had SSH keys:

```bash
ls -al ~/.ssh
```

I did not have an existing key that I wanted to use, so I generated a new one.

### Generate an Ed25519 key

I created an Ed25519 SSH key:

```bash
ssh-keygen -t ed25519 -C "<email-associated-with-github>"
```

I chose Ed25519 because it is a modern SSH key algorithm with strong security and relatively small key sizes. GitHub also recommends Ed25519 for systems that support it.

The command generated a private/public key pair.

The default files are:

```text
~/.ssh/id_ed25519
~/.ssh/id_ed25519.pub
```

The private key must remain private.

The `.pub` file contains the public key that can be shared with GitHub.

---

## 7. Adding the SSH Key to the SSH Agent

I started an SSH agent for the current shell:

```bash
eval "$(ssh-agent -s)"
```

The SSH agent manages SSH private keys for the session.

I then added my private key:

```bash
ssh-add ~/.ssh/id_ed25519
```

The key was added successfully.

---

## 8. Adding the Public Key to GitHub

To retrieve the public key, I ran:

```bash
cat ~/.ssh/id_ed25519.pub
```

I copied the resulting public key.

I then opened GitHub and navigated to:

```text
Settings
└── SSH and GPG keys
    └── New SSH key
```

I provided a descriptive title, selected the appropriate key type, pasted the public key, and added it to my GitHub account.

I intentionally do not include the actual key in this repository documentation.

---

## 9. Testing the GitHub SSH Connection

After adding the key to GitHub, I tested the SSH connection:

```bash
ssh -T git@github.com
```

On the first connection, SSH asked whether I trusted the GitHub host.

Before accepting a host for the first time, its fingerprint should be compared with GitHub's published SSH host fingerprints.

After accepting the verified host, GitHub confirmed that authentication was successful.

A successful GitHub SSH authentication produces a message similar to:

```text
Hi <github-username>! You've successfully authenticated, but GitHub does not provide shell access.
```

The statement that GitHub does not provide shell access is expected. The purpose of this connection is Git authentication, not obtaining a shell on GitHub's servers.

At this point, the Raspberry Pi could authenticate with my GitHub account through SSH.

---

## 10. Cloning the Project Repository

With Git and GitHub SSH authentication configured, I cloned the project repository onto the Raspberry Pi.

```bash
git clone git@github.com:<github-username>/piops.git
```

I then entered the repository:

```bash
cd ~/piops
```

I checked its contents:

```bash
ls
```

The repository contained:

```text
docs
README.md
```

I also used:

```bash
ls -la
```

to verify that the `.git` directory existed.

The presence of `.git` confirmed that the directory was a Git repository rather than simply a folder containing copied project files.

---

## 11. SSH Connection Interruption

During the setup, one of my SSH sessions ended with a broken pipe.

A broken SSH pipe can occur when the network connection between the client and Raspberry Pi is interrupted long enough for the SSH connection to terminate. Possible causes include Wi-Fi interruptions, temporary network connectivity problems, or changes in the client's network state.

I was able to reconnect afterward, so this did not prevent me from continuing the setup.

Because I eventually want the Raspberry Pi to operate as an always-available system, connection reliability is something I may investigate further as the project develops.

---

## 12. Verifying the Raspberry Pi SSH Server

Before configuring Visual Studio Code, I confirmed that the SSH server was running on the Raspberry Pi.

I used:

```bash
sudo systemctl status ssh
```

The service reported:

```text
Active: active (running)
```

I also checked whether SSH was configured to start automatically:

```bash
systemctl is-enabled ssh
```

It returned:

```text
enabled
```

This confirmed two different things:

- `active (running)` indicated that the SSH server was currently running.
- `enabled` indicated that the service was configured to start automatically during boot.

---

## 13. Connecting Visual Studio Code to the Raspberry Pi

With SSH working, I installed the **Remote - SSH** extension in Visual Studio Code on my development computer.

I then created a Remote SSH connection using the same SSH host information I had already tested from the terminal:

```text
<pi-user>@<pi-hostname>
```

After connecting, Visual Studio Code opened a remote development session on the Raspberry Pi.

I opened the cloned project directory:

```text
~/piops
```

This means Visual Studio Code runs on my computer as the interface, while the project files and development environment are located on the Raspberry Pi.

---

## 14. Testing the Complete Development Workflow

To verify that everything was working together, I created a test directory and file from the VS Code Remote SSH session.

I saved the changes and successfully used Git to send them to GitHub.

The completed workflow was therefore:

```text
Development Computer
        │
        │ SSH
        ▼
   Raspberry Pi
        │
        │ Git over SSH
        ▼
      GitHub
```

This confirmed that I could:

1. Connect remotely to the Raspberry Pi.
2. Open its files through Visual Studio Code.
3. Modify project files.
4. Track those changes with Git.
5. Commit the changes.
6. Push them to GitHub.

---

## 15. Disconnecting from the Raspberry Pi

When I finished working remotely, I closed the Visual Studio Code remote session.

This can be done through the Remote SSH controls in VS Code by selecting the option to close the remote connection.

Closing the VS Code remote session does **not** shut down the Raspberry Pi. It only terminates the remote development connection.

---

## Current Setup

At the end of this setup session, I had the following working environment:

```text
Raspberry Pi
├── Raspberry Pi OS
├── SSH server
├── Git
├── Git identity configuration
├── GitHub SSH authentication
└── piops repository
        │
        └── Connected to GitHub

Development Computer
├── SSH client
├── Visual Studio Code
└── Remote - SSH
        │
        └── Connected to Raspberry Pi
```

The Raspberry Pi can now function as a remote Linux development environment connected to my GitHub workflow.

This establishes the foundation I will use for the next stages of the project.

---

## References

The following resources were used during my research and setup:

- [ServerMania — SSH on macOS](https://www.servermania.com/kb/articles/ssh-mac)
- [GeeksforGeeks — How to Install Git on Raspberry Pi](https://www.geeksforgeeks.org/installation-guide/how-to-install-git-on-raspberry-pi/)
- [Linuxize — How to Install Git on Raspberry Pi](https://linuxize.com/post/how-to-install-git-on-raspberry-pi/)
- [Mathias Rocks — GitHub SSH Keys on Raspberry Pi](https://mathias.rocks/blog/2025/github-ssh-keys-raspberry-pi)
- [Raspberry Pi GitBook — Git](https://mlagerberg.gitbooks.io/raspberry-pi/content/4.3-git.html)
- [Fab Academy — Raspberry Pi GitHub Configuration](https://fabacademy.org/2020/labs/kannai/students/tatsuro-homma/project/RaspPi_G_01_GithubConfiguration.html)
- [Random Nerd Tutorials — Raspberry Pi Remote SSH with VS Code](https://randomnerdtutorials.com/raspberry-pi-remote-ssh-vs-code/)

### Additional Official Documentation Used for Verification

- [Raspberry Pi Documentation — Raspberry Pi OS and APT](https://www.raspberrypi.com/documentation/computers/os.html)
- [GitHub Docs — Connecting to GitHub with SSH](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)
- [Visual Studio Code — Remote Development Using SSH](https://code.visualstudio.com/docs/remote/ssh)