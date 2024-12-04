
async function fetchResponse() {
  console.log("hellwo");
  
  ouputPutBox = document.getElementById("outputText")
  ouputPutBox.value = "paraphrasing...";
  ouputPutBox.classList.add("animate-pulse");
  const inputText = document.getElementById("inputText")
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
  const url = "/output";
  const data = {
    "inputText": inputText.value
  }
  try {

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data)
    });
    if (!response.ok) {
      throw new Error(`Response status: ${response.status}`);
    }
    const json = await response.json();
    ouputPutBox.classList.remove("animate-pulse");
    document.getElementById("outputText").value = json.outputText
  } catch (error) {
    console.error(error.message);
  }
}