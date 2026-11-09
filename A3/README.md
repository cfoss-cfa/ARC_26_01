# A3 How to Use GitHub for a BIM Project

**Course:** DTU 41934 Advanced BIM  
**Project Group:** Facade, ARC_26_01  
**Focus Group:** Architecture  
**Tools:** GitHub, Web Browser, VS Code (optional)

**BIM Role:** OpenBIM Modeller  
**Learning Level:** 1  
**Focus Area:** Architecture

### Summary

This how-to explains how we use GitHub to organise and share files in BIM projects. It covers navigating repositories, downloading files, understanding documentation, and using Git commands such as commit, push and pull to collaborate and manage file versions.

## Why We Use GitHub in BIM Projects

In our Advanced BIM course, we use GitHub to share and organise project files, Python scripts and documentation. Since BIM projects often involve several people working on the same files, it is useful to have one shared place where changes can be tracked.

We have found GitHub particularly useful for keeping track of different file versions and sharing our work within the group. However, understanding the difference between saving a file locally and updating it on GitHub can be a little tricky at first.

## 1. How to Find and Navigate a Repository

Go to [GitHub](https://github.com) and open the repository you want to work with.

For our project, we use:

[ARC_26_01 – GitHub Repository](https://github.com/cfoss-cfa/ARC_26_01)

The repository contains folders and files organized by activities.

Click on a folder to see its contents, or select a file to view it directly in your browser.

**Something to keep in mind:** GitHub can look like a regular file explorer, BUT clicking on a file usually opens a preview rather than downloading it.

## 2. How to Download Project Files

There are two ways to download files from GitHub.

**Download a single file:**

1. Open the intended you want.
2. Click the download icon or select **Download raw file**.
3. Save the file to your computer.

**Download the entire repository:**

1. Go to the repository's main page.
2. Click the green **Code** button.
3. Select **Download ZIP**.
4. Extract the ZIP file on your computer.

**Something that can be tricky:** Downloading a repository as a ZIP gives you a copy of the files, but it does not automatically update when someone changes the files on GitHub. You will need to download the updated version again or use Git to synchronise changes.

## 3. How to Understand a README File

Most repositories contain a file called `README.md`.

This is usually a good place to start because it often explains what the project is about, how the files are organised and how to use them.

The `.md` extension stands for Markdown, a simple format used for writing documentation.

**Our advice:** Before downloading or opening scripts, check the README. It can save time by explaining which files are relevant and whether additional software is required.

## 4. How to Open a Python File in VS Code

Some BIM projects include Python scripts that can be viewed or edited in VS Code.

1. Download the Python file from GitHub.
2. Open VS Code.
3. Select **File → Open File**.
4. Choose the downloaded `.py` file.

You can now read the script and make changes if needed.

**Something to be aware of:** Opening a Python file in VS Code does not mean it can automatically run. Some scripts require specific Python libraries or software environments, such as Blender/Bonsai.

For example, a script that uses Bonsai to access an IFC model may need to run inside Blender rather than directly in VS Code.

## 5. How to Commit, Push and Pull Changes

When working on a shared GitHub project, downloading files is not always enough. If several people are editing the same project, it is important to keep the files updated.

Three useful Git functions are:

- **Commit:** Saves a snapshot of your changes in your local Git repository.
- **Push:** Uploads your local commits to GitHub.
- **Pull:** Downloads and integrates changes made by others into your local repository.

### How to Do It in VS Code

First, clone the GitHub repository to your computer and open the folder in VS Code. Make sure Git is installed.

1. **Pull:** Open the Source Control panel, click the `...` menu and select **Pull** to get the latest changes.
2. **Edit:** Make changes to a file and save it.
3. **Commit:** In Source Control, review your changes, stage the files using `+`, write a short commit message and click **Commit**.
4. **Push:** Select **Push** or **Sync Changes** to upload your commits to GitHub.

**Something we found tricky:** Saving a file in VS Code does not automatically update it on GitHub. You need to commit and push your changes. Also, if someone else has updated the same file, you may need to pull their changes and resolve any conflicts before pushing.

**Our advice:** Always pull before starting work, and use clear commit messages so other group members can understand what has changed.

## 6. How to Avoid Common Problems

A few things are worth checking when working with GitHub:

- **Wrong file version:** Make sure you are viewing the correct branch and latest relevant version.
- **Missing files:** Check whether the file is located inside another folder.
- **Downloading instead of editing:** Changes to downloaded files are not automatically uploaded to GitHub.
- **File extensions:** Keep the original extension, such as `.py` or `.md`, when saving files.
- **Overwriting work:** If several people edit the same files, coordinate changes to avoid losing each other's work.

GitHub becomes much easier to work with once you understand the difference between viewing files online, downloading copies and updating the actual repository.
