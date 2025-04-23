import { useState, useCallback } from 'react';
import { 
  Box, 
  Button, 
  Typography, 
  CircularProgress,
  Paper,
  Alert
} from '@mui/material';
import { useDropzone } from 'react-dropzone';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import InsertDriveFileIcon from '@mui/icons-material/InsertDriveFile';
import { extractData } from '../services/api';

const FileUploader = ({ 
  onFileChange, 
  onExtractStart, 
  onExtractComplete, 
  onError, 
  file, 
  isLoading 
}) => {
  const [fileError, setFileError] = useState(null);

  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length === 0) {
      return;
    }

    const selectedFile = acceptedFiles[0];
    
    // Check file type
    const validTypes = ['application/pdf', 'image/jpeg', 'image/png', 'image/tiff'];
    if (!validTypes.includes(selectedFile.type)) {
      setFileError('Please upload a PDF or image file (JPEG, PNG, TIFF)');
      return;
    }

    // Check file size (max 10MB)
    if (selectedFile.size > 10 * 1024 * 1024) {
      setFileError('File size exceeds 10MB limit');
      return;
    }

    setFileError(null);
    onFileChange(selectedFile);
  }, [onFileChange]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
      'image/tiff': ['.tiff', '.tif']
    },
    multiple: false
  });

  const handleExtract = async () => {
    if (!file) {
      setFileError('Please select a file first');
      return;
    }

    try {
      onExtractStart();
      const result = await extractData(file);
      onExtractComplete(result);
    } catch (error) {
      onError(error.message || 'Failed to extract data');
    }
  };

  return (
    <Box sx={{ mt: 2 }}>
      <Box 
        {...getRootProps()} 
        className={`dropzone ${isDragActive ? 'dropzone-active' : ''}`}
        sx={{ mb: 2 }}
      >
        <input {...getInputProps()} />
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 3 }}>
          <CloudUploadIcon sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
          {isDragActive ? (
            <Typography variant="h6">Drop the file here...</Typography>
          ) : (
            <Typography variant="h6">
              Drag & drop a file here, or click to select
            </Typography>
          )}
          <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
            Supported formats: PDF, JPEG, PNG, TIFF (Max 10MB)
          </Typography>
        </Box>
      </Box>

      {fileError && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {fileError}
        </Alert>
      )}

      {file && (
        <Paper variant="outlined" sx={{ p: 2, mb: 2, display: 'flex', alignItems: 'center' }}>
          <InsertDriveFileIcon sx={{ mr: 1, color: 'primary.main' }} />
          <Box sx={{ flexGrow: 1 }}>
            <Typography variant="body1" noWrap>
              {file.name}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {(file.size / 1024).toFixed(1)} KB • {file.type}
            </Typography>
          </Box>
        </Paper>
      )}

      <Button
        variant="contained"
        color="primary"
        size="large"
        onClick={handleExtract}
        disabled={!file || isLoading}
        startIcon={isLoading ? <CircularProgress size={20} color="inherit" /> : null}
        fullWidth
      >
        {isLoading ? 'Extracting...' : 'Extract Data'}
      </Button>
    </Box>
  );
};

export default FileUploader;
