#!/usr/bin/env node

/**
 * Legend AI CLI - Node.js wrapper
 *
 * This is a thin wrapper that calls the Python CLI.
 * Requires Python 3.11+ and legend-ai package to be installed.
 */

const { spawn } = require('child_process');
const path = require('path');

// Check if Python is available
function findPython() {
  const pythonCommands = ['python3', 'python'];

  for (const cmd of pythonCommands) {
    try {
      const result = spawn(cmd, ['--version'], { stdio: 'pipe' });
      if (result) {
        return cmd;
      }
    } catch (e) {
      continue;
    }
  }

  return null;
}

// Main execution
function main() {
  const python = findPython();

  if (!python) {
    console.error('Error: Python 3.11+ is required but not found.');
    console.error('Please install Python from https://www.python.org/downloads/');
    process.exit(1);
  }

  // Get command line arguments (skip node and script name)
  const args = process.argv.slice(2);

  // Spawn legend CLI
  const legendProcess = spawn(python, ['-m', 'legend_cli', ...args], {
    stdio: 'inherit',
    shell: true
  });

  legendProcess.on('error', (error) => {
    console.error('Error running legend CLI:', error.message);
    console.error('\nMake sure legend-ai is installed:');
    console.error('  pip install legend-ai');
    process.exit(1);
  });

  legendProcess.on('exit', (code) => {
    process.exit(code || 0);
  });
}

main();
