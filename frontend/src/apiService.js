// apiService.js
// Centralized service for making API calls

/**
 * Makes a GET request to the specified endpoint.
 * @param {string} endpoint - The API endpoint to call.
 * @returns {Promise<any>} - The response data.
 */
export async function get(endpoint) {
  try {
    const response = await fetch(endpoint);
    if (!response.ok) {
      throw new Error(`GET request failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error in GET request: ${error.message}`);
    throw error;
  }
}

/**
 * Makes a POST request to the specified endpoint with the given data.
 * @param {string} endpoint - The API endpoint to call.
 * @param {any} data - The data to send in the request body.
 * @returns {Promise<any>} - The response data.
 */
export async function post(endpoint, data) {
  try {
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    });
    if (!response.ok) {
      throw new Error(`POST request failed: ${response.statusText}`);
    }
    return await response.json();
  } catch (error) {
    console.error(`Error in POST request: ${error.message}`);
    throw error;
  }
}