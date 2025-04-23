import { useState } from 'react';
import { 
  Box, 
  Typography, 
  Grid, 
  Card, 
  CardContent, 
  CardMedia, 
  Button, 
  Divider,
  Paper,
  Tooltip,
  IconButton,
  Chip
} from '@mui/material';
import ContentCopyIcon from '@mui/icons-material/ContentCopy';
import DownloadIcon from '@mui/icons-material/Download';
import OpenInNewIcon from '@mui/icons-material/OpenInNew';
import { Light as SyntaxHighlighter } from 'react-syntax-highlighter';
import json from 'react-syntax-highlighter/dist/esm/languages/hljs/json';
import { docco } from 'react-syntax-highlighter/dist/esm/styles/hljs';

// Register the language
SyntaxHighlighter.registerLanguage('json', json);

const ResultViewer = ({ result }) => {
  const [copied, setCopied] = useState(false);

  if (!result) {
    return null;
  }

  const { data, screenshot_url } = result;

  const handleCopyJson = () => {
    navigator.clipboard.writeText(JSON.stringify(data, null, 2));
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleOpenScreenshot = () => {
    window.open(`http://localhost:8001${screenshot_url}`, '_blank');
  };

  const formatListData = (list) => {
    if (!list || list.length === 0) {
      return <Typography color="text.secondary">None</Typography>;
    }
    
    return (
      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
        {list.map((item, index) => (
          <Chip 
            key={index} 
            label={typeof item === 'string' ? item : item.name} 
            size="small" 
            color="primary" 
            variant="outlined"
          />
        ))}
      </Box>
    );
  };

  return (
    <Grid container spacing={3}>
      <Grid item xs={12} md={7}>
        <Paper sx={{ position: 'relative', p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            JSON Data
          </Typography>
          <Tooltip title={copied ? "Copied!" : "Copy JSON"}>
            <IconButton 
              aria-label="copy json" 
              onClick={handleCopyJson}
              sx={{ position: 'absolute', top: 8, right: 8 }}
            >
              <ContentCopyIcon />
            </IconButton>
          </Tooltip>
          <Box className="json-viewer">
            <SyntaxHighlighter language="json" style={docco}>
              {JSON.stringify(data, null, 2)}
            </SyntaxHighlighter>
          </Box>
        </Paper>
      </Grid>

      <Grid item xs={12} md={5}>
        <Paper sx={{ p: 2, mb: 2 }}>
          <Typography variant="h6" gutterBottom>
            Form Screenshot
          </Typography>
          <Card sx={{ mb: 2 }}>
            <CardMedia
              component="img"
              height="200"
              image={`http://localhost:8001${screenshot_url}`}
              alt="Form screenshot"
              sx={{ objectFit: 'cover' }}
            />
            <CardContent sx={{ py: 1 }}>
              <Button 
                startIcon={<OpenInNewIcon />} 
                onClick={handleOpenScreenshot}
                fullWidth
              >
                View Full Screenshot
              </Button>
            </CardContent>
          </Card>
        </Paper>

        <Paper sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Patient Information
          </Typography>
          <Box sx={{ mb: 2 }}>
            <Typography variant="subtitle2" color="text.secondary">
              Patient Name
            </Typography>
            <Typography variant="body1">
              {data.patient_name}
            </Typography>
          </Box>
          
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Date of Birth
              </Typography>
              <Typography variant="body1">
                {data.date_of_birth}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Gender
              </Typography>
              <Typography variant="body1">
                {data.gender}
              </Typography>
            </Grid>
          </Grid>
          
          <Divider sx={{ my: 2 }} />
          
          <Typography variant="subtitle2" color="text.secondary">
            Address
          </Typography>
          <Typography variant="body1" paragraph>
            {data.address}
          </Typography>
          
          <Grid container spacing={2}>
            <Grid item xs={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Phone
              </Typography>
              <Typography variant="body1">
                {data.phone_number}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Email
              </Typography>
              <Typography variant="body1">
                {data.email || 'N/A'}
              </Typography>
            </Grid>
          </Grid>
          
          <Divider sx={{ my: 2 }} />
          
          <Typography variant="subtitle2" color="text.secondary">
            Insurance Provider
          </Typography>
          <Typography variant="body1">
            {data.insurance_provider}
          </Typography>
          
          <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 1 }}>
            Insurance ID
          </Typography>
          <Typography variant="body1">
            {data.insurance_id}
          </Typography>
          
          <Divider sx={{ my: 2 }} />
          
          <Typography variant="subtitle2" color="text.secondary">
            Medical History
          </Typography>
          {formatListData(data.medical_history)}
          
          <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 2 }}>
            Current Medications
          </Typography>
          {formatListData(data.current_medications)}
          
          <Typography variant="subtitle2" color="text.secondary" sx={{ mt: 2 }}>
            Allergies
          </Typography>
          {formatListData(data.allergies)}
          
          <Divider sx={{ my: 2 }} />
          
          <Typography variant="subtitle2" color="text.secondary">
            Primary Complaint
          </Typography>
          <Typography variant="body1">
            {data.primary_complaint}
          </Typography>
          
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Appointment Date
              </Typography>
              <Typography variant="body1">
                {data.appointment_date || 'N/A'}
              </Typography>
            </Grid>
            <Grid item xs={6}>
              <Typography variant="subtitle2" color="text.secondary">
                Doctor
              </Typography>
              <Typography variant="body1">
                {data.doctor_name || 'N/A'}
              </Typography>
            </Grid>
          </Grid>
        </Paper>
      </Grid>
    </Grid>
  );
};

export default ResultViewer;
