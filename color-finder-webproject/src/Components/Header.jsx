import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import { Link } from 'react-router-dom';
import Button from '@mui/material/Button';
import PaletteIcon from '@mui/icons-material/Palette';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import GoogleIcon from '@mui/icons-material/Google';
import { IconButton, Typography } from '@mui/material';

export default function ButtonAppBar() {
  return (
    <AppBar 
      position="static"
      sx={{ 
        background: "linear-gradient(135deg, #1e3c72,rgb(19, 53, 117))", 
        boxShadow: "0px 4px 10px rgba(0, 0, 0, 0.3)"
      }}
    >
      <Toolbar>
        <IconButton
          size="large"
          edge="start"
          color="inherit"
          aria-label="menu"
          sx={{ mr: 2 }}
        >
          <PaletteIcon />
        </IconButton>
        
        {/* Title & Navigation */}
        <Box sx={{ flexGrow: 1, display: 'flex', alignItems: "center" }}>
          <Typography 
            color='inherit' 
            variant="button" 
            sx={{ textTransform: "uppercase", pr: 2, fontWeight: "bold", letterSpacing: 1.5 }}
          >
            Color Finder Website
          </Typography>

          <Button 
            color="inherit" 
            component={Link} 
            to="/" 
            sx={{ "&:hover": { backgroundColor: "rgba(255,255,255,0.1)" }, borderRadius: 2 }}
          >
            Home
          </Button>
          <Button 
            color="inherit" 
            component={Link} 
            to="/about" 
            sx={{ "&:hover": { backgroundColor: "rgba(255,255,255,0.1)" }, borderRadius: 2 }}
          >
            About
          </Button>
        </Box>

        <Box sx={{ display: 'flex', gap: 1.5 }}>
          <IconButton color="inherit" sx={{ "&:hover": { color: "#DB4437" } }}>
            <GoogleIcon fontSize="medium" />
          </IconButton>
          <IconButton color="inherit" href='https://github.com/pedroaltobelli23' sx={{ "&:hover": { color: "#333" } }}>
            <GitHubIcon fontSize="medium" />
          </IconButton>
          <IconButton color="inherit" href='https://www.linkedin.com/in/pedro-altobelli-teixeira-pinto-0795a1234/' sx={{ "&:hover": { color: "#0077B5" } }}>
            <LinkedInIcon fontSize="medium" />
          </IconButton>
        </Box>
      </Toolbar>
    </AppBar>
  );
}
