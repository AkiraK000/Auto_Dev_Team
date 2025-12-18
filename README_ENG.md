# Auto_Dev_Team

**Auto_Dev_Team** is a lightweight Python framework for autonomous software development, where a team of three AI agents (Architect, Developer, and QA Engineer) iteratively works to create, review, and improve code based on your technical specifications.

This project demonstrates the power of multi-agent systems to automate the software development lifecycle, from planning to the approval of the final product.

---

## Features

* **AI Teamwork**: Three specialized agents with unique roles to achieve the best possible result.
   * **Architect**: Designs a clear and structured technical plan.
   * **Developer**: Writes clean, documented Python code according to the plan.
   * **QA Engineer**: Conducts a meticulous review, finds bugs, and writes pytest unit tests.
* **Iterative Process**: The agents work in a "code-review-refactor" loop until the QA Engineer approves the final result.
* **Simplicity and Lightweight**: The entire framework is implemented in a single script with no complex dependencies.
* **Flexibility**: Easily adaptable to use with various Google Gemini or Google Gemma models.

   ---

  ## Quick Start

### 1. Clone the Repository

```Bash
git clone https://github.com/AkiraK000/Auto_Dev_Team.git
cd Auto_Dev_Team
```

### 2. Install Dependencies

The project requires `google-generativeai`.

```Bash
pip install google-generativeai
```

### 3. Set Up Your API Key

Open the `main.py` file and paste your API key from Google AI Studio into the following line:

```Python
# Paste your key here
API_KEY = ""
```
*For security, it is highly recommended to use environment variables or other secret management methods.*

### 4. Run the Script

Execute the script from your terminal or within your IDE:

```Bash
python main.py
```

The program will prompt you to enter a technical task. Describe the task (e.g., "Create a function that calculates the factorial of a number") and watch the team of agents get to work!

---

## How It Works

1. **Task Input**: The user (you) provides a high-level description of the task.
2. **Planning**: The **Architect** receives the task and decomposes it into a detailed technical plan.
3. **Development**: The **Developer** receives the plan and writes the first version of the code.
4. **Quality Assurance**: The **QA Engineer** receives the code, analyzes it for errors, standard compliance, and potential issues. It writes unit tests and delivers a verdict: "CODE APPROVED" or "CODE NEEDS REWORK".
5. **Iteration**: If the code needs rework, it is sent back to the **Developer** along with the QA's review. The cycle repeats until the **QA Engineer** is fully satisfied with the code quality.
6. **Result**: You receive the final, approved, and tested code.

---

## Contributing

This project is open-source, and any contributions are welcome! If you have ideas for improvement, feel free to create Issues or Pull Requests.

**Possible directions for future development**:
* Adding support for other LLM providers (Anthropic, Ollama, Groq).
* The ability to save and load the development history.
* Integration with the file system to work with multiple files.
* Creating a web interface (e.g., using Gradio or Streamlit).
* Integrating with LangChain for Tool Calling or RAG capabilities.

---
  
## License

This project is distributed under the MIT License. See the LICENSE file for more details.

---

## A Word from the Creator

If you like the idea and want to suggest solutions to improve the project, you can contact me via Telegram or email.

**My Telegram**: *@K_I_R07*

**My Email**: *hanikaevaleksandr5@gmail.com*
