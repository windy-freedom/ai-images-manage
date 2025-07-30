#!/usr/bin/env node

// Simple test script to demonstrate the pet-images MCP server
// This script shows how the server would be used in an MCP environment

const { spawn } = require('child_process');
const path = require('path');

console.log('Pet Images MCP Server Test');
console.log('==========================');
console.log();

console.log('Server Configuration:');
console.log('- Location:', path.resolve('./MCP-summary/pet-images-server/build/index.js'));
console.log('- Command: node build/index.js');
console.log();

console.log('Available Tools:');
console.log('1. get_random_pet - 获取随机的猫或狗图片');
console.log('   Parameters: type (optional): "cat", "dog", or "random"');
console.log();
console.log('2. get_dog_by_breed - 获取指定品种的狗狗图片');
console.log('   Parameters: breed (required): 狗狗品种名称');
console.log();
console.log('3. list_dog_breeds - 列出所有可用的狗狗品种');
console.log('   Parameters: none');
console.log();
console.log('4. get_cat_with_tag - 获取带有特定标签的猫咪图片');
console.log('   Parameters: tag (required): 标签名称');
console.log();

console.log('MCP Configuration (saved in mcp-config.json):');
console.log(JSON.stringify({
  "mcpServers": {
    "pet-images": {
      "command": "node",
      "args": [path.resolve('./MCP-summary/pet-images-server/build/index.js')],
      "env": {},
      "disabled": false,
      "autoApprove": []
    }
  }
}, null, 2));

console.log();
console.log('To use this MCP server:');
console.log('1. Add the configuration from mcp-config.json to your MCP client');
console.log('2. The server will be available as "pet-images"');
console.log('3. Use the tools listed above to get pet images');
console.log();
console.log('Server is ready to use! 🐱🐶');
