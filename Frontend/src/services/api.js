const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  "http://localhost:8000/api";

export async function getAnalysis() {
  const response = await fetch(
    `${API_BASE_URL}/analysis`
  );

  if (!response.ok) {
    throw new Error(
      "Failed to fetch forecast analysis"
    );
  }

  return response.json();
}