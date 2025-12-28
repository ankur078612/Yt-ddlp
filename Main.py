<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Leak Search Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #0f172a;
            color: #e5e7eb;
            padding: 20px;
        }
        h1 {
            text-align: center;
            color: #38bdf8;
        }
        .box {
            max-width: 700px;
            margin: auto;
            background: #020617;
            padding: 20px;
            border-radius: 10px;
        }
        input, button {
            width: 100%;
            padding: 12px;
            margin-top: 10px;
            border-radius: 6px;
            border: none;
            font-size: 16px;
        }
        input {
            background: #020617;
            color: white;
            border: 1px solid #334155;
        }
        button {
            background: #38bdf8;
            color: black;
            cursor: pointer;
            font-weight: bold;
        }
        button:hover {
            background: #0ea5e9;
        }
        pre {
            background: #020617;
            padding: 15px;
            border-radius: 6px;
            overflow-x: auto;
            margin-top: 20px;
            border: 1px solid #334155;
        }
        .loading {
            text-align: center;
            margin-top: 10px;
            color: #facc15;
        }
    </style>
</head>
<body>

<h1>🔍 Leak Database Search</h1>

<div class="box">
    <input type="text" id="query" placeholder="Enter email / phone / username">
    <button onclick="searchLeak()">Search</button>
    <div id="loading" class="loading"></div>
    <pre id="result"></pre>
</div>

<script>
const API_TOKEN = "AvyiSBXM";
const API_URL = "https://leakosintapi.com/";

async function searchLeak() {
    const query = document.getElementById("query").value.trim();
    const resultBox = document.getElementById("result");
    const loading = document.getElementById("loading");

    if (!query) {
        alert("Please enter a search query");
        return;
    }

    resultBox.textContent = "";
    loading.textContent = "Searching databases...";

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                token: API_TOKEN,
                request: query,
                limit: 50,
                lang: "ru"
            })
        });

        const data = await response.json();
        loading.textContent = "";

        if (data["Error code"]) {
            resultBox.textContent = "API Error: " + data["Error code"];
            return;
        }

        let output = "";
        for (const db in data.List) {
            output += "=== " + db + " ===\n";
            output += data.List[db].InfoLeak + "\n\n";

            if (data.List[db].Data) {
                data.List[db].Data.forEach(row => {
                    for (const key in row) {
                        output += key + ": " + row[key] + "\n";
                    }
                    output += "\n";
                });
            }
            output += "\n--------------------------------\n\n";
        }

        resultBox.textContent = output || "No results found";

    } catch (err) {
        loading.textContent = "";
        resultBox.textContent = "Error connecting to API";
        console.error(err);
    }
}
</script>

</body>
</html>
