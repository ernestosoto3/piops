# Tailscale Remote Access Setup

This document records the steps I followed to add secure remote access to the Raspberry Pi using Tailscale.

Until this stage, my SSH workflow depended primarily on the Raspberry Pi and my development computer being reachable through the same local network.

The goal of this stage was to remove that limitation and allow me to securely access the Raspberry Pi when my development computer is outside the Pi's local network.

During this stage, I:

- Researched the networking problem Tailscale solves.
- Compared LAN, public, and Tailscale IP addresses.
- Considered the security implications of public SSH port forwarding.
- Installed Tailscale on the Raspberry Pi.
- Added the Raspberry Pi to my existing tailnet.
- Verified that my development computer and Raspberry Pi were on the same tailnet.
- Connected to the Raspberry Pi through its Tailscale network.
- Tested the connection from outside the Pi's local network.
- Verified that VS Code Remote SSH worked over Tailscale.
- Researched the difference between regular SSH over Tailscale and Tailscale SSH.
- Enabled Tailscale SSH.
- Encountered and resolved a locale configuration issue.

> **Note:** Personal information, usernames, hostnames, authentication URLs, IP addresses, SSH fingerprints, tailnet information, and other machine-specific values have been removed or generalized in this documentation.

---

## 1. The Remote Access Problem

Before adding Tailscale, my normal SSH connection depended on being able to reach the Raspberry Pi through its local network.

Conceptually, the setup looked like:

```text
Development Computer
        │
        │ Local Network
        ▼
     Router
        │
        ▼
 Raspberry Pi
```

This works when the devices can communicate through the same network, but it becomes a problem when my development computer leaves that network.

For example:

```text
Home Network                       External Network

Raspberry Pi                       Development Computer
     │                                    │
     ▼                                    ▼
Home Router                         Mobile Hotspot
     │                                    │
     └──────────── Internet ──────────────┘
```

The Raspberry Pi's normal private LAN address is not directly routable across the public internet.

I therefore needed a secure method for connecting the two devices across different networks.

---

## 2. What Tailscale Solves

Tailscale creates a private network between authenticated devices.

Instead of requiring every device to be physically connected to the same LAN, Tailscale creates an encrypted overlay network called a **tailnet**.

Conceptually:

```text
                Tailnet
                   │
        ┌──────────┴──────────┐
        │                     │
        ▼                     ▼
Development Computer     Raspberry Pi
        │                     │
External Network          Home Network
```

Both devices can communicate through the tailnet even though their underlying physical networks are different.

This gives me a way to reach the Raspberry Pi remotely without directly exposing the Raspberry Pi's SSH port to the public internet.

---

## 3. LAN IP vs. Public IP vs. Tailscale IP

Before configuring Tailscale, I researched the difference between the different addresses involved.

### LAN IP Address

A LAN IP identifies a device inside a local network.

For example:

```text
Development Computer ─┐
                      │
Raspberry Pi ─────────┼── Local Network
                      │
Other Devices ────────┘
```

The Raspberry Pi typically receives its LAN address from the local network's DHCP server.

This address may change and normally only has meaning within that network.

---

### Public IP Address

A public IP represents an internet-routable connection.

Devices inside a home network commonly access the internet through a router associated with a public IP.

Conceptually:

```text
Raspberry Pi
     │
     │ Private LAN
     ▼
   Router
     │
     │ Public IP
     ▼
  Internet
```

The Raspberry Pi's private LAN address is therefore different from the public-facing address used by the network.

---

### Tailscale IP Address

Tailscale assigns devices addresses inside the tailnet.

A Tailscale IPv4 address typically comes from the `100.x.x.x` range used by Tailscale.

Conceptually, the Raspberry Pi can therefore have several different network identities:

```text
Raspberry Pi
│
├── LAN IP
│   └── Used on the local network
│
├── Public network connection
│   └── Reached through the router
│
└── Tailscale IP
    └── Used inside the tailnet
```

The Tailscale address provides a stable way for devices in the tailnet to communicate even when their physical networks change.

---

## 4. Why I Did Not Use Public SSH Port Forwarding

One possible method for remote SSH access is configuring the router to forward an internet-facing port to port `22` on the Raspberry Pi.

Conceptually:

```text
Internet
   │
   │ Public SSH connection
   ▼
Router
   │
   │ Port Forward
   ▼
Raspberry Pi :22
```

However, exposing SSH directly to the internet increases the system's public attack surface.

An internet-accessible SSH service can receive automated connection attempts, scans, and authentication attempts from external systems.

Instead, I decided to use Tailscale.

With this approach:

```text
Development Computer
        │
        │ Encrypted Tailnet
        ▼
   Raspberry Pi
```

I do not need to expose the Raspberry Pi's SSH port directly to the public internet for this workflow.

---

## 5. Existing Tailscale Account

I already had a Tailscale account and Tailscale installed on my development computer.

Because of this, I did not need to create a new account.

The main task was adding the Raspberry Pi to the same tailnet.

---

## 6. Installing Tailscale on the Raspberry Pi

I installed Tailscale using its Linux installation script:

```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

The installer detected the Raspberry Pi's Debian-based environment and configured the appropriate Tailscale package repository.

During installation, several packages were installed, including:

```text
tailscale
tailscale-archive-keyring
iptables
libip4tc2
libip6tc2
```

The installation also configured the `tailscaled` service to start through `systemd`.

At the time of this installation, the Tailscale package installed on the Raspberry Pi reported version:

```text
1.102.5
```

The installation completed successfully.

---

## 7. Adding the Raspberry Pi to My Tailnet

After installing Tailscale, I connected the Raspberry Pi to my existing tailnet:

```bash
sudo tailscale up
```

Tailscale provided an authentication URL.

I opened the URL, authenticated using my existing Tailscale account, and authorized the Raspberry Pi.

After authentication, the terminal reported:

```text
Success.
```

The Raspberry Pi was now part of my tailnet.

> The authentication URL used during this process is intentionally not included in this repository.

---

## 8. Verifying the Tailnet

My development computer already had Tailscale installed and authenticated.

I opened the Tailscale administration interface and checked the list of machines connected to my tailnet.

Both devices appeared:

```text
Tailnet
│
├── Development Computer
│
└── Raspberry Pi
```

This confirmed that both systems were members of the same Tailscale network.

---

## 9. Identifying the Tailscale Address

After joining the tailnet, the Raspberry Pi received its own Tailscale IP address.

For privacy, I do not include the actual address in this documentation.

It can conceptually be represented as:

```text
100.x.x.x
```

Tailscale can also provide DNS-based device naming through MagicDNS.

This means I can potentially reach the Raspberry Pi using either its tailnet address or an appropriate machine name rather than depending on its changing LAN address.

---

## 10. First SSH Test over Tailscale

I first tested whether the Raspberry Pi's existing SSH server could be reached through the Tailscale network.

From my development computer, I used:

```bash
ssh <pi-user>@<tailscale-ip>
```

On the first connection, SSH treated the Tailscale IP as a new destination and asked me to confirm the host.

After confirming the host and authenticating, I successfully received a shell on the Raspberry Pi.

I then exited:

```bash
logout
```

This proved that my existing SSH service could operate **over the Tailscale network**.

At this point, I was still using the Raspberry Pi's normal SSH server. Tailscale was providing the private network path between the two devices.

Conceptually:

```text
Development Computer
        │
        │ Tailscale Network
        │
        │ Regular SSH
        ▼
   Raspberry Pi
        │
        └── sshd
```

This distinction became important later when I investigated Tailscale SSH.

---

## 11. Testing from Outside the Raspberry Pi's Local Network

The most important test was confirming that the setup worked when the two devices were no longer on the same local network.

For this test:

- The Raspberry Pi remained connected to the home network.
- I disconnected my development computer from that network.
- I connected my development computer through a separate personal hotspot.

The network layout was now approximately:

```text
Home Network                         Mobile Network
     │                                    │
     ▼                                    ▼
Raspberry Pi                       Development Computer
     │                                    │
     └─────────── Tailscale ──────────────┘
```

I first tested Tailscale connectivity:

```bash
tailscale ping <pi-tailscale-ip>
```

The Raspberry Pi responded successfully.

I then tested SSH:

```bash
ssh <pi-user>@<pi-tailscale-ip>
```

The connection also succeeded.

This was an important milestone because the Raspberry Pi and development computer were now on completely different physical networks.

I could still access the Raspberry Pi remotely through the tailnet.

---

## 12. Verifying VS Code Remote SSH over Tailscale

My next test was determining whether the VS Code Remote SSH workflow I had already configured would continue to work through Tailscale.

I opened Visual Studio Code and selected the Raspberry Pi through Remote SSH.

The remote environment loaded successfully.

This meant the development workflow could now operate approximately like:

```text
Development Computer
│
├── VS Code
│
└── Remote SSH
      │
      │ Tailscale
      ▼
 Raspberry Pi
      │
      └── piops/
```

The important difference from my previous setup is that the development computer no longer needs to be on the Raspberry Pi's local network.

---

## 13. Regular SSH over Tailscale vs. Tailscale SSH

During this setup, I learned that **using SSH over Tailscale and using Tailscale SSH are two different configurations**.

### Regular SSH over Tailscale

This was the configuration I tested first.

Tailscale provided the network connection, while the Raspberry Pi's normal SSH server still handled authentication.

```text
Tailscale
   │
   │ Provides network path
   ▼
Raspberry Pi
   │
   └── OpenSSH
        └── Handles SSH authentication
```

The connection looked like:

```bash
ssh <pi-user>@<tailscale-ip>
```

I still authenticated using the SSH configuration available on the Raspberry Pi.

---

### Tailscale SSH

Tailscale SSH integrates SSH access with the identity and access controls of the tailnet.

Instead of only providing the network path, Tailscale can also intercept and manage SSH connections according to Tailscale's SSH configuration and access policies.

Conceptually:

```text
Tailscale Identity
       │
       ▼
Tailnet Access Rules
       │
       ▼
  Tailscale SSH
       │
       ▼
 Raspberry Pi
```

This provides a different access-control model from simply running traditional SSH over a Tailscale connection.

---

## 14. Enabling Tailscale SSH

After successfully testing normal SSH over the tailnet, I decided to enable Tailscale SSH on the Raspberry Pi.

I connected to the Raspberry Pi and ran:

```bash
sudo tailscale set --ssh
```

Because I was already connected to the Raspberry Pi through Tailscale, the command warned me that enabling Tailscale SSH would reroute SSH traffic and disconnect my current session.

The warning was expected.

After confirming the change, the existing SSH session terminated:

```text
Connection reset by peer
```

This was not an unexpected network failure.

The command had changed how SSH connections arriving through Tailscale were handled, so terminating the existing session was part of applying that change.

I then established a new connection.

---

## 15. Locale Configuration Problem

After enabling Tailscale SSH and reconnecting, I encountered an unrelated configuration problem.

The Raspberry Pi displayed warnings similar to:

```text
WARNING! Your environment specifies an invalid locale.
```

and:

```text
setlocale: LC_CTYPE: cannot change locale
```

The warnings referenced:

```text
en_US.UTF-8
```

I investigated the installed locales with:

```bash
locale -a
```

The system showed locales including:

```text
C
C.utf8
POSIX
en_GB.utf8
```

However, `en_US.UTF-8` was not available.

I then inspected the current locale environment:

```bash
locale
```

The shell was attempting to use:

```text
en_US.UTF-8
```

for several locale categories.

I also checked the system locale configuration:

```bash
cat /etc/default/locale
```

This showed:

```text
LANG=en_GB.UTF-8
```

This revealed a mismatch: the SSH environment was attempting to use `en_US.UTF-8`, but that locale had not been generated on the Raspberry Pi.

---

## 16. Fixing the Locale

I used Raspberry Pi's configuration utility:

```bash
sudo raspi-config
```

I navigated through:

```text
Localisation Options
└── Locale
```

I selected:

```text
en_US.UTF-8
```

and configured it as the default locale.

After completing the configuration, I verified that the locale had been generated:

```bash
locale -a | grep en_US
```

The Raspberry Pi returned:

```text
en_US.utf8
```

I also checked:

```bash
echo $LANG
```

which returned:

```text
en_US.UTF-8
```

I disconnected and established a new SSH session.

The locale warnings no longer appeared.

This confirmed that the locale configuration issue had been resolved.

---

## 17. Final Remote Access Architecture

After completing this stage, the remote development architecture changed significantly.

### Before Tailscale

```text
Development Computer
        │
        │ Same Local Network
        ▼
   Raspberry Pi
        │
        └── piops
```

Remote access depended on local-network reachability.

### After Tailscale

```text
Development Computer
        │
        │
        ▼
    Tailscale
      Tailnet
        │
        ▼
   Raspberry Pi
        │
        ├── Tailscale
        ├── SSH
        └── piops
```

The physical networks can now be different:

```text
Development Computer
        │
        ├── Home Wi-Fi
        ├── Mobile Hotspot
        └── Other Network
                 │
                 ▼
             Tailscale
                 │
                 ▼
           Raspberry Pi
                 │
                 └── Home Network
```

This removes the requirement that my development computer be connected to the Raspberry Pi's local network.

---

## 18. Current Development Workflow

My current workflow is now approximately:

```text
Development Computer
│
├── Tailscale
│
├── Visual Studio Code
│
└── Remote SSH
      │
      ▼
   Tailnet
      │
      ▼
Raspberry Pi
│
├── Tailscale
├── SSH access
├── Git
├── Python
│
└── piops/
    ├── .venv/
    ├── docs/
    ├── test/
    ├── .gitignore
    ├── check_env.py
    └── README.md
```

This builds on the previous stages of the project rather than replacing them.

Git still handles version control.

VS Code Remote SSH still provides my remote development interface.

The Python virtual environment still isolates project dependencies.

Tailscale now provides the private networking layer that allows me to reach the Raspberry Pi from outside its local network.

---

## 19. What I Completed

During this stage, I successfully:

1. Researched the purpose of Tailscale.
2. Learned the difference between LAN, public, and Tailscale IP addresses.
3. Evaluated public SSH port forwarding against a private Tailscale connection.
4. Installed Tailscale on the Raspberry Pi.
5. Connected the Raspberry Pi to my existing tailnet.
6. Verified that the Raspberry Pi and development computer appeared on the same tailnet.
7. Identified the Raspberry Pi's Tailscale address.
8. Successfully connected to the Raspberry Pi using SSH over Tailscale.
9. Successfully used `tailscale ping` to verify tailnet connectivity.
10. Tested the connection while the Raspberry Pi and development computer were on different physical networks.
11. Successfully connected to the Raspberry Pi while my development computer was using a personal hotspot.
12. Verified that VS Code Remote SSH worked through the Tailscale connection.
13. Learned the difference between regular SSH over Tailscale and Tailscale SSH.
14. Enabled Tailscale SSH.
15. Investigated an invalid locale warning that appeared after reconnecting.
16. Generated and configured the missing `en_US.UTF-8` locale.
17. Reconnected and confirmed that the locale warning was resolved.

The Raspberry Pi can now be accessed remotely without requiring my development computer to remain on the same local network.

This gives `piops` a much more practical remote development environment and establishes another part of the infrastructure I can build on during future stages of the project.

---

## Security Notes

Several security decisions from this stage are intentional:

- I did not configure public router port forwarding for SSH.
- The Raspberry Pi's Tailscale IP is not included in this public repository.
- My tailnet name and MagicDNS domain are not included.
- Authentication URLs are not stored in the repository.
- SSH fingerprints and other machine-specific identifiers are not included.
- Tailscale access still depends on authenticated membership and the access rules configured for my tailnet.

The goal is to document how the system works without publishing information that is unnecessary for understanding or reproducing the project.

---

## References

The following resources were used during my research for this stage:

- [Tailscale Documentation](https://tailscale.com/kb)
- [Tailscale — How Tailscale Works](https://tailscale.com/blog/how-tailscale-works)
- [Tailscale — Install Tailscale on Linux](https://tailscale.com/download/linux)
- [Tailscale — Tailscale SSH](https://tailscale.com/kb/1193/tailscale-ssh)
- [Tailscale — MagicDNS](https://tailscale.com/kb/1081/magicdns)
- [Tailscale — IP Addresses](https://tailscale.com/kb/1033/ip-and-dns-addresses)
- [SunFounder — Access Raspberry Pi Remotely with Tailscale](https://www.sunfounder.com/blogs/news/how-to-access-raspberry-pi-remotely-with-tailscale-no-port-forwarding)
- [Raspberry Pi Documentation](https://www.raspberrypi.com/documentation/)