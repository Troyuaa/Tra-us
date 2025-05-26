````markdown
# TraçuS 🚀

**TraçuS** é um sistema de investigação de sites simples e eficiente, com menu interativo no terminal, desenvolvido em Python.  
Permite analisar URLs para contar páginas, obter IP, detectar falhas básicas de segurança, coletar informações do responsável pelo domínio e gerar relatórios completos.

---

## Funcionalidades

- 🔍 **Contar páginas** vinculadas na URL inicial  
- 🌐 **Mostrar IP** do site  
- ⚠️ **Verificar falhas simples** (exposição de áreas administrativas, possíveis senhas em texto, mensagens de erro)  
- 👤 **Informações do responsável** pelo domínio (via API Whois)  
- 📝 **Gerar relatório completo** salvo em arquivo `.txt`

---

## Pré-requisitos

- Python 3.7 ou superior  
- Pacotes Python necessários:
  - `requests`
  - `beautifulsoup4`
  - `rich`

Instale as dependências com:

```bash
pip install requests beautifulsoup4 rich
````

---

## Como usar

1. Clone este repositório:

   ```bash
   git clone https://github.com/seu-usuario/Tracus.git
   cd Tracus
   ```

2. Execute o script:

   ```bash
   python tracus.py
   ```

3. Use o menu para escolher a análise desejada e informe a URL do site.

---

## Observações

* A consulta Whois usa uma API pública gratuita para demonstração, que pode ter limitações.
* As verificações de falhas são básicas e devem ser usadas apenas para aprendizado/demonstração.
* Não nos responsabilizamos por quaisquer danos a terceiros.

---

## Licença

MIT License © Troyuaa - Illeg4l

---

## Contato

Se quiser contribuir, abrir issues ou sugestões, fique à vontade!
Email: [troyuaa@gmail.com](mailto:troyuaa@gmail.com)
GitHub: [https://github.com/Troyuaa](https://github.com/troyuaa)

---

⚡️ Você está investigando com **TraçuS**! ⚡️

```
