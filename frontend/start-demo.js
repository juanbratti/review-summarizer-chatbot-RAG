#!/usr/bin/env node

console.log('🚀 Starting ChatGPT-style Review Assistant...\n');
console.log('📋 Make sure your backend is running on http://localhost:8000');
console.log('🌐 Frontend will be available at http://localhost:3000\n');

const { spawn } = require('child_process');

const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
const start = spawn(npm, ['start'], { stdio: 'inherit' });

start.on('close', (code) => {
  console.log(`\n✅ Frontend process exited with code ${code}`);
}); 