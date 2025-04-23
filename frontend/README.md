# Healthcare Form Data Extractor - Frontend

A modern React frontend for the Healthcare Form Data Extraction PoC, built with Vite, React 18, and Material UI.

## Features

- Modern, responsive UI built with Material UI 5.14
- Drag-and-drop file upload for healthcare forms (PDF, JPEG, PNG, TIFF)
- Real-time data extraction with progress indicators
- Structured display of extracted patient information
- Form screenshot visualization
- JSON data export capability

## Technology Stack

- **React 18** - UI library
- **Vite** - Build tool and development server
- **Material UI 5.14** - Component library and design system
- **Axios** - HTTP client for API requests
- **React Dropzone** - Drag-and-drop file upload
- **React Syntax Highlighter** - JSON data formatting

## Project Structure

```
frontend/
├── public/               # Static assets
├── src/
│   ├── components/       # React components
│   │   ├── FileUploader.jsx  # File upload component
│   │   └── ResultViewer.jsx  # Data visualization component
│   ├── services/         # API services
│   │   └── api.js        # Backend API integration
│   ├── App.jsx           # Main application component
│   ├── main.jsx          # Application entry point
│   └── index.css         # Global styles
├── index.html            # HTML template
├── package.json          # Dependencies and scripts
└── vite.config.js        # Vite configuration
```

## Setup Instructions

### Prerequisites

- Node.js 18.x or higher
- npm 9.x or higher
- Backend server running (see backend README)

### Installation

1. Install dependencies:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
```

2. Start the development server:

```bash
npm run dev
```

The application will be available at http://localhost:5173

### Building for Production

```bash
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Integration with Backend

This frontend is designed to work with the Healthcare Form Data Extraction backend API. By default, it connects to the backend at `http://localhost:8001`. If your backend is running on a different URL, update the `baseURL` in `src/services/api.js`.

## Features

### File Upload

- Supports PDF, JPEG, PNG, and TIFF files
- File size validation (max 10MB)
- Drag-and-drop interface
- File type validation

### Data Extraction

- Sends files to backend API for processing
- Displays loading indicators during extraction
- Shows success/error notifications

### Result Visualization

- Structured display of patient information
- Form screenshot preview
- JSON data view with copy capability
- Responsive layout for all device sizes
