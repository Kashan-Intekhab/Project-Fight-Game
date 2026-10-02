# 🥊 2D Python Fighting Game

A feature-rich, polished 2D local two-player arcade fighting game built in Python using **Pygame**. Experience fast-paced local multiplayer combat with jumping physics, punch mechanics, fireball projectiles, timed shields, visual particle impact effects, and full arcade audio!

---

## 🎮 Game Overview & Rules

* **Match Objective**: Reduce your opponent's health bar (100 HP) to zero before the 60-second round timer runs out!
* **Round System**: Tracks scores across multiple rounds. Pressing **`R`** after a match resets the stage, increments the round counter (*ROUND 1*, *ROUND 2*, etc.), and starts the next fight.
* **Time Over**: If time expires before a player is knocked out, the player with the higher remaining HP wins the round. If health is equal, it's declared a Draw.
* **Shield Stamina**: Players can block incoming attacks, but shields have a limited duration (40 frames max). Holding the shield drains stamina; releasing it recharges your shield bar.

---

## ⌨️ Control Scheme

### 🔴 Player 1 (Kashan Intekhab - Red)
| Action | Key | Description |
| :--- | :--- | :--- |
| **Move Left** | `A` | Walk left across the arena |
| **Move Right** | `D` | Walk right across the arena |
| **Jump** | `W` | Perform a high jump |
| **Block / Shield** | `S` | Deploy shield (blocks punch & fireball damage) |
| **Punch Attack** | `F` | Melee strike (10 DMG + Knockback) |
| **Fireball** | `G` | Launch ranged projectile (15 DMG + Extra Knockback, 2s Cooldown) |

---

### 🔵 Player 2 (Ali Hammad - Blue)
| Action | Key | Description |
| :--- | :--- | :--- |
| **Move Left** | `LEFT ARROW` | Walk left across the arena |
| **Move Right** | `RIGHT ARROW` | Walk right across the arena |
| **Jump** | `UP ARROW` | Perform a high jump |
| **Block / Shield** | `DOWN ARROW` | Deploy shield (blocks punch & fireball damage) |
| **Punch Attack** | `L` | Melee strike (10 DMG + Knockback) |
| **Fireball** | `K` | Launch ranged projectile (15 DMG + Extra Knockback, 2s Cooldown) |

---

### ⚙️ System Controls
* **Restart Match**: Press `R` when the match ends to start the next round.
* **Quit Game**: Click the window close (`X`) button or terminate via terminal.

---

## ✨ Features & Mechanics

* ⚡ **Dynamic Combat Mechanics**: Melee strikes with cooldowns, ranged fireballs, and physical player knockbacks upon taking hits.
* 🛡️ **Shield & Stamina System**: Visual stamina duration bar above the character indicating remaining block time.
* 💥 **Particle Effects (Hit Sparks)**: Custom particle system rendering vibrant green spark bursts on punch hits, shield blocks, and fireball explosions.
* 🎵 **Audio & Sound FX**: Looping background soundtrack alongside custom audio for punches, hits, shield blocks, clashes, and fireball launches.
* ⏱️ **Arcade UI & Banners**: Integrated round timer, score counters, dynamic HP bars, and animated text announcements (*ROUND X*, *FIGHT!*, *Winner Prompts*).
* 💥 **Collision Clash Physics**: Players bounce off each other when walking directly into one another with custom audio feedback.

---

## 📂 File & Folder Structure

Ensure your project directory contains the following assets before running:

```text
Project Fight Game/
│
├── main.py                  # Primary Python script
├── README.md                # Project documentation
└── Sounds/                  # Audio asset folder
    ├── bg_music.mp3         # Background soundtrack
    ├── punch.ogg            # Swing sound effect
    ├── fireball.wav         # Fireball launch effect
    ├── hit.wav              # Direct hit sound effect
    ├── block.wav            # Shield block effect
    └── bump.aiff            # Player clash/bump effect
