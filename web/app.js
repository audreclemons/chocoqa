// app.js (SECURITY-CLEAN)

// Load master data on page load
window.addEventListener("DOMContentLoaded", async () => {
  try {
    if (!window.API_BASE_URL) {
      throw new Error("API base URL not configured");
    }

    // Load ingredients
    const ingredientsResponse = await fetch(
      `${window.API_BASE_URL}/master/ingredients`,
      { method: "GET" }
    );
    const ingredientsData = await ingredientsResponse.json();

    const ingredientSelect = document.getElementById("ingredientId");
    ingredientsData.ingredients.forEach((ingredient) => {
      const option = document.createElement("option");
      option.value = ingredient.ingredientId;
      option.textContent = `${ingredient.ingredientName} (${ingredient.defaultUnit})`;
      ingredientSelect.appendChild(option);
    });

    // Load products
    const productsResponse = await fetch(
      `${window.API_BASE_URL}/master/products`,
      { method: "GET" }
    );
    const productsData = await productsResponse.json();

    const productSelect = document.getElementById("productId");
    productsData.products.forEach((product) => {
      const option = document.createElement("option");
      option.value = product.productNo;
      option.textContent = `${product.productName} (${product.productType})`;
      option.dataset.specs = JSON.stringify(product.specs || {});
      productSelect.appendChild(option);
    });

    // Display specs on product selection
    productSelect.addEventListener("change", () => {
      const specsDiv = document.getElementById("specs");
      if (!productSelect.value) {
        specsDiv.hidden = true;
        specsDiv.textContent = "";
        return;
      }

      const specs = JSON.parse(
        productSelect.options[productSelect.selectedIndex].dataset.specs
      );

      specsDiv.textContent = `Specs — Temp: ${specs.tempMin}–${specs.tempMax} °C, Viscosity: ${specs.viscosityMin}–${specs.viscosityMax}`;
      specsDiv.hidden = false;
    });
  } catch (err) {
    console.error("Initialization failed");
  }
});

// Handle form submission
document
  .getElementById("submitForm")
  .addEventListener("submit", async (event) => {
    event.preventDefault();

    const payload = {
      productId: document.getElementById("productId").value,
      ingredientId: document.getElementById("ingredientId").value,
      percentage: Number(document.getElementById("percentage").value),
      temperature: document.getElementById("temperature").value
        ? Number(document.getElementById("temperature").value)
        : null,
      viscosity: document.getElementById("viscosity").value
        ? Number(document.getElementById("viscosity").value)
        : null,
      data: document.getElementById("data").value.trim(),
      timestamp: new Date().toISOString(),
    };

    try {
      const response = await fetch(`${window.API_BASE_URL}/submit`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      const result = await response.json();

      if (!response.ok) {
        alert("Submission failed");
        return;
      }

      alert(`Submission successful — Status: ${result.specStatus}`);
      document.getElementById("submitForm").reset();
    } catch (err) {
      alert("Submission error");
    }
  });
