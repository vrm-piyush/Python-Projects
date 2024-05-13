# Contributing to the Python Projects Repository

Thank you for your interest in contributing to the Python Projects Repository! Your contributions help improve the quality and diversity of the projects in this repository. Whether you want to suggest an improvement, report a bug, or add a new project, your contributions are highly appreciated.

## ![image](assets\contributing.png) How to Contribute

To contribute to this repository, please follow these steps:

<details>
<summary>
1. Star The Repo
</summary>

Star the repo by pressing the top most-right button to start your wonderful journey

![star repo](https://docs.github.com/assets/images/help/stars/starring-a-repository.png)

</details>

---

<details>
<summary>
2. Fork the repository
</summary>

Click the [**"Fork"**](https://github.com/vrm-piyush/python-mini-project) button on the top right corner of this page to create a copy of the repository in your GitHub account.

![fork image](https://upload.wikimedia.org/wikipedia/commons/3/38/GitHub_Fork_Button.png)

</details>

---

<details>
<summary>
3. Clone the forked repository
</summary>

- **Method 1:** GitHub Desktop

> ⚠️ **NOTE:** If you're not familiar with Git, using **GitHub Desktop Application** is a better start. If you choose this method, make sure to download it before continuing reading.
>
> ❗❗ Access link to download [**here**](https://desktop.github.com).

Learn more about how to clone the remote respository on your local machine using **GitHub Desktop** [here](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/adding-and-cloning-repositories/cloning-and-forking-repositories-from-github-desktop#cloning-a-repository).

- **Method 2:** Git

Use the following command to clone the forked repository to your local machine

```bash
git clone https://github.com/vrm-piyush/Python-Projects.git
```

> This makes a local copy of the repository in your machine.

Learn more about [forking](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) and [cloning a repo](https://docs.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository).

</details>

---

<details>
<summary>
4. Create your feature branch 
</summary>

Always keep your local copy of the repository updated with the original repository.
Before making any changes and/or in an appropriate interval, follow the following steps:

- **Method 1:** GitHub Desktop

Learn more about how to create new branch [here](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/making-changes-in-a-branch/managing-branches#creating-a-branch) and how to fetch and pull origin from/to your local machine [here](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/keeping-your-local-repository-in-sync-with-github/syncing-your-branch).

Learn more about how to fetch and pull origin from/to your local machine using **GitHub Desktop** [here](https://docs.github.com/en/desktop/contributing-and-collaborating-using-github-desktop/keeping-your-local-repository-in-sync-with-github/syncing-your-branch).

- **Method 2:** Git

Run the following commands **_carefully_** to update your local repository

```sh
# If you cloned a while ago, get the latest changes from upstream
git checkout <master>
git pull upstream <master>

# Make a feature branch (Always check your current branch is up to date before creating a new branch from it to avoid merge conflicts)
git checkout -b <branch-name>

#
```

</details>

---

<details>
<summary>
5. Ready, Set, Go...
</summary>

Once you have completed these steps, you are ready to start contributing to the project and creating **pull requests**.

- Create a folder in
  [projects directory](https://github.com/vrm-piyush/python-projects) according to your project name.
  > The folder name should follow the following format "Your_Project_Name_Here". For example: Dice_Stimulator
- Write your code and add to the respective folder in the projects directory, locally.
- Don't forget to add a `README.md` in your folder, according to the
  [README_TEMPLATE.](README_TEMPLATE.md)

2. **Clone the forked repository**: Use the following command to clone the forked repository to your local machine:

3. **Create a new branch**: Choose a descriptive name for your feature or bug fix branch and create it with the following command:

   ```bash
   git checkout -b feature-branch-name
   ```

4. **Make your changes**: Implement your changes or additions to the project and commit them to your branch:

   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

5. **Push your changes**: Push your branch to your forked repository with the following command:

   ```bash
   git push origin feature-branch-name
   ```

6. **Open a pull request (PR)**: Open a pull request from your forked repository to the main repository. Provide a clear and descriptive title for your PR and explain the changes you've made.

## Code Style Guidelines

- **Follow PEP 8 guidelines**: Adhere to the PEP 8 style guide for Python code.
- **Use clear and descriptive names**: Choose meaningful variable and function names.
- **Write docstrings**: Document functions and modules as needed for clarity.
- **Use comments**: Explain complex sections of code with comments for better understanding.

## Reporting Bugs

If you encounter any bugs or issues with the projects in this repository, please open an issue on the GitHub issue tracker. Provide detailed information about the bug, including steps to reproduce it and any relevant error messages.

## Feature Requests

If you have ideas for new projects or features to add to existing projects, feel free to open an issue on the GitHub issue tracker. Describe your idea or feature request in detail, and it will be considered for future development.

## Contact

If you have any questions or need further assistance, feel free to contact me.

---

## Guidelines

To ensure that your contributions are accepted with ease, please follow these guidelines:

- **Create a new folder for each project**: Each project should have its own folder in the repository.
- **Use clear and descriptive names**: Choose meaningful names for variables, functions, and files.
- **Include a README**: Each project should include a README file that describes the project and how to run it.
- **Follow the PEP 8 style guide**: Adhere to the PEP 8 style guide for Python code.
- **Use comments**: Explain complex sections of code with comments for better understanding.
- **Document functions**: Include docstrings for functions to describe their purpose and usage.
- **Avoid hardcoding**: Use variables and configuration files to avoid hardcoding values.
- **Test your code**: Ensure that your code is correct and runs without errors before submitting a PR.

---

### Git Guidelines

- **Create a new branch**: Always create a new branch for your changes.
- **Keep your branch updated**: Regularly update your branch with the main branch to avoid conflicts.
- **Write descriptive commit messages**: Provide a clear and descriptive commit message for each commit.
- **Follow the pull request template**: Use the pull request template when opening a pull request.
- **Follow the code review guidelines**: Respond to code reviews and make changes as needed.
- **Keep pull requests small**: Submit small pull requests with a single change instead of multiple changes.
- **Close issues with pull requests**: Reference the issue number in the pull request description to close the issue automatically.

## Development Guidelines

When contributing to the projects in this repository, please follow these guidelines to ensure a smooth development process and maintain code consistency across the repository.

### Issues Guidelines

- **Search for existing issues**: Check the issue tracker to see if someone has already reported the issue or suggested the feature.
- **Provide detailed information**: Include detailed information about the issue or feature request to help others understand it.
- **Follow the template**: Use the issue template to provide the necessary information and context for your issue.

## Acknowledgements

- [GitHub Docs](https://docs.github.com/en) - For providing detailed guides on using GitHub features.
- [Git Handbook](https://guides.github.com/introduction/git-handbook/) - For explaining how to use Git and GitHub effectively.
- [Open Source Guides](https://opensource.guide/) - For providing resources on open source projects and contributions.

## Support

If you have any questions or need assistance with your contributions, feel free to reach out to the repository owner or open an issue on the repository. Your feedback and suggestions are welcome!

## License

By contributing to this repository, you agree that your contributions will be licensed under the [MIT License](LICENSE).

## Code of Conduct

Please read the [Code of Conduct](CODE_OF_CONDUCT.md) before contributing to this repository. This code outlines the expectations for all contributors and maintainers of this repository.

## Resources

- [Python Documentation](https://docs.python.org/3/) - Official Python documentation for reference.
- [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/) - Official Python style guide for writing clean and readable code.
- [GitHub Guides](https://guides.github.com/) - Official GitHub guides on how to use Git and GitHub.
- [Open Source Guide](https://opensource.guide/) - A guide to open source projects and how to contribute.

## Contributors

A big thank you to all the contributors who have helped improve this repository with their suggestions and contributions!
