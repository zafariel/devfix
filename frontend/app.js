const button = document.getElementById("analyzeButton");
const input = document.getElementById("urlInput");

const status = document.getElementById("status");
const results = document.getElementById("results");
const issuesContainer = document.getElementById("issues");
const scoreElement = document.getElementById("score");


button.addEventListener("click", analyze);


input.addEventListener("keydown", (event) => {
    if (event.key === "Enter") {
        analyze();
    }
});


async function analyze() {

    const url = input.value.trim();

    if (!url) {
        status.textContent = "Digite uma URL.";
        return;
    }

    status.textContent = "Analisando site...";
    button.disabled = true;

    results.classList.add("hidden");

    try {

        const response = await fetch("/analyze", {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                url: url
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || "Erro ao analisar.");
        }

        renderResults(data);

        status.textContent = "Análise concluída.";

    } catch (error) {

        status.textContent = error.message;

    } finally {

        button.disabled = false;
    }
}


function renderResults(data) {

    results.classList.remove("hidden");

    const issues = data.issues || [];

    issuesContainer.innerHTML = "";

    if (issues.length === 0) {

        issuesContainer.innerHTML = `
            <div class="issue">
                <h3>✓ Nenhum problema encontrado</h3>
                <p>
                    O DEVFIX não encontrou problemas nas verificações atuais.
                </p>
            </div>
        `;

        scoreElement.textContent = "100";

        return;
    }

    let score = 100;

    issues.forEach(issue => {

        if (issue.severity === "high") {
            score -= 20;
        }

        if (issue.severity === "medium") {
            score -= 10;
        }

        if (issue.severity === "low") {
            score -= 5;
        }

        const element = document.createElement("div");

        element.className = "issue";

        element.innerHTML = `
            <div class="issue-top">
                <h3>${escapeHtml(issue.message)}</h3>
                <span class="severity">
                    ${escapeHtml(issue.severity)}
                </span>
            </div>

            <p>
                ${escapeHtml(issue.recommendation)}
            </p>
        `;

        issuesContainer.appendChild(element);
    });

    score = Math.max(score, 0);

    scoreElement.textContent = score;
}


function escapeHtml(value) {

    const div = document.createElement("div");

    div.textContent = value;

    return div.innerHTML;
}
