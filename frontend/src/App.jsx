import { useState } from 'react';
import {
  Box,
  Container,
  Typography,
  Paper,
  AppBar,
  Toolbar,
  Divider,
  LinearProgress,
  Alert,
  Snackbar
} from '@mui/material';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import FileUploader from './components/FileUploader';
import ResultViewer from './components/ResultViewer';

function App() {
  const [file, setFile] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [showSnackbar, setShowSnackbar] = useState(false);

  const handleFileChange = (selectedFile) => {
    setFile(selectedFile);
    setResult(null);
    setError(null);
  };

  const handleExtractComplete = (data) => {
    setResult(data);
    setIsLoading(false);
    setShowSnackbar(true);
  };

  const handleError = (errorMessage) => {
    setError(errorMessage);
    setIsLoading(false);
    setShowSnackbar(true);
  };

  const handleExtractStart = () => {
    setIsLoading(true);
    setResult(null);
    setError(null);
  };

  const handleCloseSnackbar = () => {
    setShowSnackbar(false);
  };

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <AppBar position="static">
        <Toolbar>
          <LocalHospitalIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Healthcare Form Data Extraction
          </Typography>
        </Toolbar>
      </AppBar>

      {isLoading && <LinearProgress />}

      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, flexGrow: 1 }}>
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h5" gutterBottom>
            Upload Healthcare Form
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph>
            Upload a healthcare form (PDF or image) to extract structured data using OCR and LLM technology.
          </Typography>
          <FileUploader 
            onFileChange={handleFileChange} 
            onExtractStart={handleExtractStart}
            onExtractComplete={handleExtractComplete}
            onError={handleError}
            file={file}
            isLoading={isLoading}
          />
        </Paper>

        {result && (
          <Paper sx={{ p: 3 }}>
            <Typography variant="h5" gutterBottom>
              Extracted Data
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <ResultViewer result={result} />
          </Paper>
        )}
      </Container>

      <Box component="footer" sx={{ p: 2, bgcolor: 'background.paper', mt: 'auto' }}>
        <Typography variant="body2" color="text.secondary" align="center">
          © {new Date().getFullYear()} Healthcare Form Data Extraction PoC
        </Typography>
      </Box>

      <Snackbar open={showSnackbar} autoHideDuration={6000} onClose={handleCloseSnackbar}>
        <Alert 
          onClose={handleCloseSnackbar} 
          severity={error ? "error" : "success"} 
          sx={{ width: '100%' }}
        >
          {error 
            ? `Error: ${error}` 
            : "Data extracted successfully!"}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default App;
