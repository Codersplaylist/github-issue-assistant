# 📋 BEGINNER'S GUIDE: How to Submit Your Project

Welcome! This guide will walk you through **everything** step-by-step. Don't worry if this is your first time - I'll explain every single step! 🚀

---

## 🎯 The Big Picture: What We're Going to Do

1. **Get an API key** from Google (free, takes 2 minutes)
2. **Test your app locally** to make sure it works
3. **Put your code on GitHub** so you can share it
4. **Submit the GitHub link** to Seedling Labs

That's it! Let's break each step down.

---

## PART 1: Get Your Free Google Gemini API Key

### What is an API key?
Think of it like a password that lets your app talk to Google's AI. It's free!

### How to get it:

1. **Open this link in your browser:**
   ```
   https://aistudio.google.com/app/apikey
   ```

2. **You'll see a page that says "Create a new key"**
   - In the "Name your key" box, type: `GitHub Issue Assistant`
   - Click on "Default Gemini Project" (or just leave it)
   - Click the blue "Create" button

3. **Copy the key that appears**
   - It will look like: `AIzaSyAaBbCcDd1234567890...`
   - Click the copy button OR select all and copy it
   - **IMPORTANT**: Save this somewhere safe! You'll need it in a minute

---

## PART 2: Test Your App Locally

### What does "test locally" mean?
It means running the app on YOUR computer to make sure it works before submitting.

### Step-by-step instructions:

#### STEP 2.1: Open Terminal

- On Mac: Press `Cmd + Space`, type "Terminal", press Enter
- You'll see a white or black window where you can type commands

#### STEP 2.2: Go to Your Project Folder

Copy and paste this **EXACT** command into Terminal, then press Enter:

```bash
cd /Users/mac/.gemini/antigravity/scratch/github-issue-assistant
```

**What this does**: It takes you straight to your project folder, no matter where you started.

#### STEP 2.3: Create Your Secret API Key File

Copy this command, but **REPLACE** `your_key_here` with the actual key you copied earlier:

```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```

**Example** (don't use this exact key, use yours):
```bash
echo "GEMINI_API_KEY=AIzaSyAaBbCcDd1234567890EeFfGgHhIiJjKk" > .env
```

**What this does**: Creates a secret file called `.env` that stores your API key safely.

#### STEP 2.4: Clean Up and Set Up Backend (Server)

We need to make sure we use the **correct version of Python (3.12)** because the default one (3.14) is too new for some tools.

Copy these commands **ONE AT A TIME** and press Enter after each:

1. **Go to the backend folder:**
   ```bash
   cd /Users/mac/.gemini/antigravity/scratch/github-issue-assistant/backend
   ```

2. **Remove any old broken setup (just in case):**
   ```bash
   rm -rf venv
   ```

3. **Create a fresh environment using Python 3.12:**
   ```bash
   python3.12 -m venv venv
   ```
   *(This might take 5-10 seconds. If it says "command not found", stop and let me know!)*

4. **Activate the environment:**
   ```bash
   source venv/bin/activate
   ```
   *You should see `(venv)` appear at the start of your terminal line.*

5. **Install the required tools:**
   ```bash
   pip install -r requirements.txt
   ```
   *This will print a lot of text. Wait for it to finish (approx 30-60 seconds).*

6. **Start the server:**
   ```bash
   python app.py
   ```

**What you should see:**
```
🚀 Starting GitHub Issue Assistant API...
📍 Server running at http://0.0.0.0:8000
```

✅ **SUCCESS!** Your backend is running! **Keep this window OPEN.**

#### STEP 2.5: Start the Frontend (Website)

**Open a NEW Terminal window** (Cmd + N in Terminal).

Copy these commands ONE AT A TIME:

1. **Go to the frontend folder:**
   ```bash
   cd /Users/mac/.gemini/antigravity/scratch/github-issue-assistant/frontend
   ```

2. **Start the website server:**
   ```bash
   python3 -m http.server 3000
   ```

**What you should see:**
```
Serving HTTP on :: port 3000 ...
```

✅ **SUCCESS!** Your frontend is running!

#### STEP 2.6: Test in Your Browser

1. **Open your web browser** (Chrome, Safari, Firefox, etc.)

2. **Type this in the address bar:**
   ```
   http://localhost:3000
   ```

3. **You should see a beautiful dark purple website!** 🎨

4. **Quick test:**
   - Click the button that says "React #28858"
   - Click "Analyze Issue"
   - Wait 5-10 seconds
   - You should see AI analysis appear!

🎉 **If you see the analysis, YOUR APP WORKS!**

#### STEP 2.7: Stop the Servers (When Done Testing)

- In both Terminal windows, press `Ctrl + C` to stop the servers
- You can close the Terminal windows

---

## PART 3: Put Your Code on GitHub

### What is GitHub?
It's like Google Drive, but for code. You'll upload your project there so Seedling Labs can see it.

### Step-by-step:

#### STEP 3.1: Create a GitHub Account (if you don't have one)

1. Go to: https://github.com
2. Click "Sign up"
3. Create a free account
4. Verify your email

#### STEP 3.2: Create a New Repository

1. **Log into GitHub**

2. **Click the "+" button** in the top-right corner

3. **Click "New repository"**

4. **Fill in the form:**
   - **Repository name**: `github-issue-assistant`
   - **Description**: `AI-powered GitHub issue analysis tool built for Seedling Labs`
   - **Make sure "Public" is selected** ✅ (NOT Private!)
   - **DON'T check** "Add a README file"
   - **Click "Create repository"**

5. **You'll see a page with instructions** - IGNORE THEM! We'll use different commands.

#### STEP 3.3: Upload Your Code to GitHub

**Open Terminal** (if closed, reopen it)

Copy these commands ONE AT A TIME:

1. **Go to your project:**
   ```bash
   cd /Users/mac/.gemini/antigravity/scratch/github-issue-assistant
   ```

2. **Connect to GitHub (Replace YOUR_USERNAME!):**
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/github-issue-assistant.git
   ```
   *Example: `git remote add origin https://github.com/john/github-issue-assistant.git`*

3. **Rename branch:**
   ```bash
   git branch -M main
   ```

4. **Upload code:**
   ```bash
   git push -u origin main
   ```

**If asked for a password:**
- Use your GitHub username.
- For password, you might need a "Personal Access Token". If your normal password fails, see Step 3.3b below.

#### STEP 3.3b: Create GitHub Personal Access Token (if needed)

If GitHub asks for a password and won't accept it:

1. Go to: https://github.com/settings/tokens
2. Click "Generate new token" → "Generate new token (classic)"
3. Give it a name: `Issue Assistant Upload`
4. Check the box next to `repo`
5. Click "Generate token" at the bottom
6. **Copy the token** (starts with `ghp_`)
7. Use this as your password when git asks

---

## PART 4: Submit to Seedling Labs

Your **GitHub repository URL** is:
```
https://github.com/YOUR_USERNAME/github-issue-assistant
```

1. **Go to your repository on GitHub** (you should see all your files there).
2. **Copy the URL from your browser's address bar.**
3. **Submit this URL.**

---

## 🆘 Troubleshooting

### "Command not found: python3.12"
If Step 2.4 fails saying `python3.12: command not found`:
1. Run `brew install python@3.12` (if you have Homebrew)
2. OR download Python 3.12 from python.org
3. Let me know if you need help installing it!

### "Permission denied"
- Add `sudo` before the command (e.g., `sudo python app.py`).

### "Port already in use"
- Someone else is using that port. Change `3000` to `3001` or `8000` to `8001`.

---

## 🎉 You're Done!

**You did great!** 🌟 Use this guide to submit your work and good luck!
