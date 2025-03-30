# Laser Tag Scoring and Match Control System

A modern, original Python application for managing competitive team-based laser tag events. Built with a fully custom UI and UDP-based equipment communication. Designed for Debian virtual machines and real-time gameplay.

---

## 📦 Setup Instructions

### 0. Install Python 3 (if not already installed)
To install Python 3 on a Debian-based system:

```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 1. Download & Navigate
Download the zip and extract to any location.

```bash
cd /path/to/project/
```

### 2. Install Dependencies
Ensure Python 3 is installed, then run:

```bash
sudo apt-get install python3-tk python3-pip python3-pygame
python3 -m pip install Pillow typing psycopg2-binary pygubu pygame
```

> If you encounter a database constraint error, run:
> ```sql
> ALTER TABLE players ADD CONSTRAINT unique_user_id UNIQUE (id);
> ALTER TABLE players ADD CONSTRAINT unique_codename UNIQUE (codename);
> ```

---

## 🚀 Running the Application

```bash
python3 app.py
```

---

## 🕹️ How to Use

### Player Entry Screen
- Input **User ID** and **Equipment ID**.
- If the User ID exists in the database, the **Codename** will auto-fill.
- If not, leave the field blank and enter a new Codename manually.
- Press **F5** or click **Continue** to proceed to the match screen.
- Press **F12** or click **Clear All** to reset the form.

Each team supports **up to 15 players**. Teams are visually split (Green and Red).

### Game Screen
- See full team lineups and scores.
- Use **Start Game** to launch a 30-second countdown.
- After countdown, code `202` is sent over UDP to activate gear.
- Use **Back to Entry** to revise players (data auto-loads).

---

## 🧰 System Details
- **Platform**: Debian VM
- **Database**: PostgreSQL (`photon` DB, `players` table)
- **Networking**:
  - Transmit: `127.0.0.1:7500`
  - Receive:  `127.0.0.1:7501`
  - Transmit format: integer (equipment ID)
  - Receive format: `int:int` (attacker:target)

---

## 🔍 Database Access
To view saved players:

```bash
psql photon
SELECT * FROM players;
```

---

## 👤 Author
| GitHub Username   | Name             |
|------------------|------------------|
| solomon-sudo-e    | Solomon Hufford  |

---

## ✅ Features
- Full keyboard support (F5, F12)
- PostgreSQL-integrated codename lookup
- Countdown timer + automatic gear activation
- Duplicate ID/equipment protection
- Clean UI for both player entry and game view
