# Contributing to AFRelay

First off, thank you for considering contributing! It’s people like you who make open-source tools awesome.

To keep things moving smoothly, here are some practical guidelines to help you get started.

---

## Local Setup

To get the project running on your machine:

- Fork the repository.
- Clone your fork: git clone `https://github.com/YOUR-USERNAME/AFRelay.git`
- Install dependencies: `pip install -r requirements.txt`
- Create a branch: `git checkout -b feat/your-feature-name`.

---

### Coding Standards

- **Tests:** If you add a new feature, you must include unit tests for the added functions. This ensures your code works as expected and helps us prevent regressions in the future.

- **AI-Generated Code:** We do not accept AI-generated code if the Pull Request author cannot fully explain its internal logic and purpose. You are responsible for every line you submit.

- **No "Vibe Coding":** Every change must be backed by clear technical reasoning. Avoid submitting code simply because it "seems to work" without understanding the why behind it. Refrain from introducing **low-quality** or **"magic"** code that compromises the codebase.

- **Keep PRs Atomic:** Avoid submitting "mega-PRs" with hundreds of modified lines across multiple scopes. Large, sweeping changes are difficult to review and prone to bugs. Please break down your contributions into smaller and focused Pull Requests.

- **Simplicity over complexity:** If you can write it in 5 lines instead of 20, do it.

---

### Documentation

Writing docs is dead boring and one of the big problems with many open source projects but someone's gotta do it. It makes things a lot easier if you submit a small description of your fix or your new features with every contribution so that it can be swiftly added to the package documentation.

---

### How to Contribute

### 1. Reporting bugs
Check the issues tab to see if the bug has already been reported.
If not, open a new issue. Please include:
- A clear and descriptive title.
- Steps to reproduce the bug.
- What you expected to happen vs. what actually happened

### 2. Suggesting Enhacements

We love new ideas. Before writing code, please open an issue labeled `enhancement` so we can discuss the implementation and ensure it aligns with the project's roadmap.

### 3. Pull Requests (PRs)
- Keep your PRs focused. Small, single-purpose PRs are much easier to review.
- Ensure your code follows the existing style (please run `isort . `).
- Write meaningful commit messages (e.g., `feat: add data verification`). We follow [Conventional Commits](https://www.conventionalcommits.org/).
---

### Need Help?

If you get stuck or have questions, don't hesitate to:

- Open a discussion in the Discussions tab.