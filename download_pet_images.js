#!/usr/bin/env node

const { spawn } = require('child_process');
const fs = require('fs');
const https = require('https');
const http = require('http');
const path = require('path');

// Function to download image from URL
function downloadImage(url, filename) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https:') ? https : http;
    const file = fs.createWriteStream(filename);
    
    protocol.get(url, (response) => {
      response.pipe(file);
      file.on('finish', () => {
        file.close();
        console.log(`Downloaded: ${filename}`);
        resolve();
      });
    }).on('error', (err) => {
      fs.unlink(filename, () => {}); // Delete the file on error
      reject(err);
    });
  });
}

// Function to call MCP tool and get image URL
function getMCPImage(type) {
  return new Promise((resolve, reject) => {
    const serverPath = '/home/user/for-test/MCP-summary/pet-images-server/build/index.js';
    const child = spawn('node', [serverPath], { stdio: ['pipe', 'pipe', 'pipe'] });
    
    let output = '';
    let errorOutput = '';
    
    child.stdout.on('data', (data) => {
      output += data.toString();
    });
    
    child.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    child.on('close', (code) => {
      if (code === 0) {
        try {
          // Parse the MCP response to extract image URL
          const lines = output.split('\n');
          for (const line of lines) {
            if (line.includes('imageUrl')) {
              const match = line.match(/"imageUrl":"([^"]+)"/);
              if (match) {
                resolve(match[1]);
                return;
              }
            }
          }
          reject(new Error('No image URL found in response'));
        } catch (err) {
          reject(err);
        }
      } else {
        reject(new Error(`MCP process exited with code ${code}: ${errorOutput}`));
      }
    });
    
    // Send MCP request
    const request = {
      jsonrpc: "2.0",
      id: 1,
      method: "tools/call",
      params: {
        name: "get_random_pet",
        arguments: { type: type }
      }
    };
    
    child.stdin.write(JSON.stringify(request) + '\n');
    child.stdin.end();
  });
}

async function downloadPetImages() {
  console.log('Starting to download 8 more pet images...');
  
  const images = [
    { type: 'cat', filename: 'pics/cat_2.jpg' },
    { type: 'dog', filename: 'pics/dog_2.jpg' },
    { type: 'cat', filename: 'pics/cat_3.jpg' },
    { type: 'dog', filename: 'pics/dog_3.jpg' },
    { type: 'cat', filename: 'pics/cat_4.jpg' },
    { type: 'dog', filename: 'pics/dog_4.jpg' },
    { type: 'cat', filename: 'pics/cat_5.jpg' },
    { type: 'dog', filename: 'pics/dog_5.jpg' }
  ];
  
  for (const image of images) {
    try {
      console.log(`Getting ${image.type} image...`);
      const url = await getMCPImage(image.type);
      console.log(`Downloading from: ${url}`);
      await downloadImage(url, image.filename);
    } catch (error) {
      console.error(`Error downloading ${image.filename}:`, error.message);
    }
  }
  
  console.log('Finished downloading pet images!');
}

downloadPetImages().catch(console.error);
