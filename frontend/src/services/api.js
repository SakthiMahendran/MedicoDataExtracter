import axios from 'axios';

// Create an axios instance with default config
const api = axios.create({
  baseURL: 'http://localhost:8001',
  timeout: 60000, // 60 seconds timeout for long-running extraction
  headers: {
    'Content-Type': 'multipart/form-data',
  },
});

/**
 * Extract data from a healthcare form file
 * @param {File} file - The file to extract data from (PDF or image)
 * @returns {Promise<Object>} - The extracted data and screenshot URL
 */
export const extractData = async (file) => {
  try {
    // Create a FormData object to send the file
    const formData = new FormData();
    formData.append('file', file);

    // Make the request to the backend
    const response = await api.post('/api/extract', formData, {
      onUploadProgress: (progressEvent) => {
        // You can use this to track upload progress if needed
        const percentCompleted = Math.round(
          (progressEvent.loaded * 100) / progressEvent.total
        );
        console.log(`Upload progress: ${percentCompleted}%`);
      },
    });

    // Return the data from the response
    return response.data;
  } catch (error) {
    // Handle errors
    console.error('Error extracting data:', error);
    
    // Throw a more user-friendly error
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      throw new Error(error.response.data.detail || 'Server error');
    } else if (error.request) {
      // The request was made but no response was received
      throw new Error('No response from server. Please check if the backend is running.');
    } else {
      // Something happened in setting up the request that triggered an Error
      throw new Error(error.message || 'Error processing request');
    }
  }
};

export default api;
