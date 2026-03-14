# 🎮 Pygame Tetris
## เกม Tetris พัฒนาด้วย Python และ Pygame

เกมนี้สาธิตหลักการ **OOP (Object-Oriented Programming)** และ **SOLID Principles** ผ่านการสร้างเกม Tetris ที่สมบูรณ์

📚 **เพื่ออ่านรายละเอียดเกี่ยวกับการออกแบบและสถาปัตยกรรม** โปรดดู **[PRESENT.md](PRESENT.md)**

---

## 🏗️ สถาปัตยกรรมและโครงสร้างโครงการ

โปรเจกต์นี้ถูกออกแบบโดยยึดหลัก SOLID และ Design Patterns ต่างๆ เพื่อให้โค้ดขยายต่อได้ง่ายและเป็นระเบียบ:

```text
pygame_tetris/
├── main.py                  # 🎬 จุดเข้าของเกม
├── requirements.txt         # 📦 การพึ่งพา (dependencies)
├── pyproject.toml           # ⚙️ การตั้งค่าโครงการ
├── README.md                # 📖 ไฟล์นี้
│
├── config/                  # ⚙️ การตั้งค่า
│   ├── __init__.py
│   └── config.py            # ค่าคงที่ทั้งหมดของเกม
│
├── core/                    # 🎮 เครื่องเล่นเกมหลัก
│   ├── __init__.py
│   ├── game.py              # ตัวควบคุมเกมหลัก (Main Controller)
│   ├── game_engine.py       # เครื่องเล่นเกม (Game Loop)
│   ├── state_machine.py     # ระบบการจัดการสถานะ
│   └── event_system.py      # ระบบเหตุการณ์
│
├── game/                    # 🎲 ตรรกะเกม
│   ├── __init__.py
│   ├── entities/            # 🔷 ชิ้นส่วนเกม
│   │   ├── __init__.py
│   │   ├── tetromino.py     # คลาสพื้นฐาน Tetromino (ABC)
│   │   └── piece_randomizer.py # ระบบ 7-Bag Randomizer
│   │
│   ├── world/               # 🗺️ โลกเกม
│   │   ├── __init__.py
│   │   └── board.py         # ตรรกะกระดานเกม
│   │
│   └── systems/             # ⚙️ ระบบเกม
│       ├── __init__.py
│       ├── collision_system.py # ตรวจสอบการชนกัน
│       ├── gravity_system.py   # การตกของชิ้นส่วน
│       ├── scoring_system.py   # ระบบสกอร์
│       └── wall_kick_system.py # ระบบการหมุน SRS
│
├── input/                   # ⌨️ การจัดการอินพุต
│   ├── __init__.py
│   ├── input_handler.py     # จัดการ input จากผู้เล่น
│   └── input_behavior.py    # พฤติกรรมอินพุต
│
├── rendering/               # 🎨 ระบบการแสดงผล
│   ├── __init__.py
│   └── renderer.py          # Pygame Renderer
│
├── audio/                   # 🔊 ระบบเสียง
│   ├── __init__.py
│   └── sound_manager.py     # ผู้จัดการเสียง
│
├── ui/                      # 🖼️ ส่วนติดต่อผู้ใช้
│   ├── __init__.py
│   └── menu_screen.py       # จอเมนู
│
└── data/                    # 💾 ข้อมูล
    └── highscore.json       # คะแนนสูงสุด

---


## 💾 การติดตั้ง

### ✅ ข้อกำหนดเบื้องต้นก่อนติดตั้ง

ก่อนเริ่มติดตั้ง กรุณาตรวจสอบข้อกำหนดต่อไปนี้:

#### 1. **Python 3.8 หรือใหม่กว่า**

**ตรวจเวอร์ชัน Python**:
```bash
python --version
```
หรือบน macOS/Linux:
```bash
python3 --version
```

หากไม่มี Python ให้ดาวน์โหลดจาก: https://www.python.org/downloads/

#### 2. **pip (Package Manager)**

pip มาพร้อมกับ Python โดยอัตโนมัติ ตรวจสอบว่ามีใช้งานได้:
```bash
pip --version
```
หรือบน macOS/Linux:
```bash
pip3 --version
```

#### 3. **Git**

ดาวน์โหลด Git จาก: https://git-scm.com/downloads

ตรวจสอบการติดตั้ง:
```bash
git --version
```

---

### 📥 ขั้นตอนการติดตั้งแบบละเอียด

#### **ขั้นตอนที่ 1: Clone โครงการลงมาจาก GitHub**

เปิด Terminal หรือ PowerShell แล้วรันคำสั่ง:

```bash
git clone https://github.com/krittahatwa68-hub/pygame_tertris.git
```

เข้าไปในโฟลเดอร์โครงการ:

```bash
cd pygame_tertris
```

---

#### **ขั้นตอนที่ 2: สร้าง Virtual Environment**

**Virtual Environment** คือ environment แยกต่างหากสำหรับโครงการนี้ เพื่อไม่ให้ dependency ของโครงการอื่น ๆ ทำให้เกิด conflict

**บน Windows (PowerShell)**:

```powershell
python -m venv venv
```

**บน macOS/Linux (Terminal)**:

```bash
python3 -m venv venv
```

---

#### **ขั้นตอนที่ 3: เปิดใช้งาน Virtual Environment**

**บน Windows (PowerShell)**:

```powershell
.\venv\Scripts\Activate.ps1
```

**บน macOS/Linux (Terminal)**:

```bash
source venv/bin/activate
```

**ตรวจสอบว่าเปิดใช้งานได้**:
- รหัสกำหนด (Prompt) ข้างหน้าควรมี `(venv)` ปรากฏ บ่งชี้ว่า Virtual Environment ถูกเปิดใช้งาน:

```
(venv) C:\Users\...\pygame_tertris>
```

---

#### **ขั้นตอนที่ 4: ติดตั้ง Dependencies**

ติดตั้ง Pygame และ dependencies อื่น ๆ จากไฟล์ `requirements.txt`:

```bash
pip install -r requirements.txt
```

**ก็ต้องรอสักครู่ให้เสร็จการติดตั้ง** ระบบจะ download และติดตั้ง:
- `pygame-ce==2.5.7` (Pygame Community Edition)

เมื่อเสร็จแล้ว คุณจะเห็นข้อความ:
```
Successfully installed pygame-ce-2.5.7
```

---

**ทำการตรวจสอบการติดตั้ง** (Optional):

```bash
python -c "import pygame; print('Pygame successfully installed!')"
```

ถ้า output เป็น `Pygame successfully installed!` แสดงว่าติดตั้งสำเร็จ

---

### 🚀 ขั้นตอนการรันเกม

#### **ขั้นตอนที่ 1: ตรวจสอบว่า Virtual Environment ยังเปิดใช้งาน**

คุณต้องเห็น `(venv)` ในเส้นสั่ง (Command Prompt):

```
(venv) C:\Users\...\pygame_tertris>
```

ถ้าไม่เห็น ให้เปิดใช้งานตามขั้นตอนที่ 3 ข้างต้น

#### **ขั้นตอนที่ 2: รันเกม**

```bash
python main.py
```

**บน macOS/Linux** (หากใช้ Python 3):

```bash
python3 main.py
```

#### **ขั้นตอนที่ 3: เล่นเกม!**

หน้าจอเกม Tetris จะปรากฏขึ้น พร้อมข้อมูลเกี่ยวกับสถาปัตยกรรม

---

### ⌨️ ปุ่มควบคุมในเกม

| ปุ่ม | หน้าที่ | คำอธิบาย |
|-----|--------|---------|
| **← (ลูกศร ซ้าย)** | เลื่อนชิ้นไปซ้าย | ชิ้นจะเลื่อนไปทางซ้ายหนึ่งช่อง |
| **→ (ลูกศร ขวา)** | เลื่อนชิ้นไปขวา | ชิ้นจะเลื่อนไปทางขวาหนึ่งช่อง |
| **↑ (ลูกศร ขึ้น)** | หมุนชิ้น | ชิ้นจะหมุนตามเข็มนาฬิกา |
| **↓ (ลูกศร ลง)** | เร่งการตก | ชิ้นจะตกลงมาเร็วขึ้น |
| **SPACE** | ปล่อยชิ้น | ชิ้นจะตกลงไปถึงพื้นทันที |
| **C** | Hold (ระงับชิ้น) | เก็บชิ้นปัจจุบันและเอาชิ้นที่เก็บออกมา |
| **P** | Pause/Resume | หยุดเกม/เล่นต่อ |
| **ESC** | ออกจากเกม | ปิดเกม |

---

### 🎯 วิธีการเล่น

1. **เรียงแถว**: เติมแถวให้เต็มโดยใช้ชิ้นส่วน 7 ตัว เมื่อแถวเต็ม มันจะลบไป
2. **ได้คะแนน**: 
   - ลบ 1 แถว = 100 คะแนน
   - ลบ 2 แถว = 300 คะแนน
   - ลบ 3 แถว = 500 คะแนน
   - ลบ 4 แถว (Tetris) = 800 คะแนน
3. **ไม่ให้เต็ม**: หากชิ้นใหม่ไม่สามารถวางได้ (ชนกับด้านบน) = Game Over

---

## 🐛 แก้ไขปัญหาทั่วไป (Troubleshooting)

### ปัญหา: "pygame not found" หรือ "ModuleNotFoundError"

**วิธีแก้**:
1. ตรวจสอบว่า virtual environment ถูกเปิดใช้งาน
2. ติดตั้ง dependencies อีกครั้ง:
   ```bash
   pip install -r requirements.txt
   ```

### ปัญหา: เกมไม่ทำงาน บน macOS/Linux

**วิธีแก้**:
ใช้ `python3` แทน `python`:
```bash
python3 main.py
```

### ปัญหา: หน้าจอเกมจางหรือไม่แสดง

**วิธีแก้**:
- ตรวจสอบว่าระบบของคุณรองรับ Pygame-CE
- ลองอัปเดต Pygame:
  ```bash
  pip install --upgrade pygame-ce
  ```

---

## 📚 ทรัพยากรเพิ่มเติม

### เรียนรู้ OOP และ SOLID

- [Real Python: OOP](https://realpython.com/tutorials/oop/)
- [SOLID Principles](https://en.wikipedia.org/wiki/SOLID)
- [PEP 8 - Style Guide](https://pep8.org/)

### เรียนรู้ Pygame

- [Pygame Documentation](https://www.pygame.org/docs/)
- [Pygame CE (Community Edition)](https://github.com/pygame-community/pygame-ce)

### Tetris Guidelines

- [Tetris Guideline](https://tetris.fandom.com/wiki/Tetris_Guideline)
- [Super Rotation System (SRS)](https://tetris.fandom.com/wiki/SRS)

---

## 📋 โครงสร้างข้อมูล

### ข้อมูลกระดาน

กระดานเก็บตัวอักษร 1 และ 0:
- `0` = ช่องว่าง
- `1` = ช่องที่มีบล็อก

```python
board_state = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    # ... 20 แถว ทั้งหมด
    [1, 1, 1, 1, 1, 0, 1, 1, 1, 1],  # แถวที่จะลบ
]
```

### ข้อมูล High Score

```json
{
  "highscore": 15000,
  "player_name": "Player",
  "date": "2024-01-15"
}
```

---

---

## 🎓 บันทึกการเรียนรู้

### สิ่งที่เราเรียนรู้จากโครงการนี้

1. **OOP Design Patterns**: Inheritance, Composition, Polymorphism
2. **SOLID Principles**: วิธีการสร้างโค้ดที่ยืดหยุ่นและขยายได้
3. **Game Development**: Game Loop, State Management, Collision Detection
4. **Software Architecture**: Modular Design, Separation of Concerns
5. **Best Practices**: Type Hints, Documentation, Testing

---

## ✨ สรุป

Pygame Tetris เป็นตัวอย่างที่ยอดเยี่ยมของการประยุกต์ใช้หลักการ OOP และ SOLID ในการสร้างโปรแกรมที่ดี

หวังว่าโครงการนี้จะช่วยให้คุณเข้าใจการออกแบบซอฟต์แวร์ได้ลึกซึ้งยิ่งขึ้น!

---
