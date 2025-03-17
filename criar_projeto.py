import os

# Estrutura de diretórios
estrutura = [
    "Auto_Click/src",
    "Auto_Click/tests",
    "Auto_Click/docs",
    "Auto_Click/data",
    "Auto_Click/configs",
    "Auto_Click/venv",
]

# Arquivos base
arquivos = {
    "Auto_Click/.gitignore": "venv/\n__pycache__/\n*.pyc\n",
    "Auto_Click/requirements.txt": "",
    "Auto_Click/README.md": "# Meu Projeto\n\nDescrição do projeto.",
    "Auto_Click/setup.py": 'from setuptools import setup, find_packages\n\nsetup(name="Auto_Click", packages=find_packages())',
    "Auto_Click/src/__init__.py": "",
    "Auto_Click/src/main.py": 'if __name__ == "__main__":\n    print("Olá, Mundo!")',
    "Auto_Click/tests/test_main.py": 'def test_exemplo():\n    assert 1 + 1 == 2',
}

# Criar diretórios
for pasta in estrutura:
    os.makedirs(pasta, exist_ok=True)

# Criar arquivos com conteúdo
for caminho, conteudo in arquivos.items():
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(conteudo)

print("Estrutura do projeto criada com sucesso! 🚀")
