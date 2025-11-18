#!/usr/bin/env node

/**
 * Post-install script for legend-ai npm package
 * Checks Python and offers to install the Python package
 */

const { execSync } = require('child_process');
const readline = require('readline');

function checkPython() {
  try {
    const version = execSync('python3 --version', { encoding: 'utf8' });
    console.log('✓ Found Python:', version.trim());
    return true;
  } catch (e) {
    console.error('✗ Python 3.11+ is required but not found');
    console.error('  Install from: https://www.python.org/downloads/');
    return false;
  }
}

function checkLegendAI() {
  try {
    execSync('python3 -m legend_cli --version', { encoding: 'utf8', stdio: 'pipe' });
    return true;
  } catch (e) {
    return false;
  }
}

function installLegendAI() {
  console.log('\nInstalling legend-ai Python package...');
  try {
    execSync('pip install legend-ai', { stdio: 'inherit' });
    console.log('\n✓ legend-ai installed successfully!');
    return true;
  } catch (e) {
    console.error('\n✗ Failed to install legend-ai');
    console.error('  Try manually: pip install legend-ai');
    return false;
  }
}

function main() {
  console.log('Legend AI CLI - Post-install\n');

  // Check Python
  if (!checkPython()) {
    process.exit(1);
  }

  // Check if legend-ai is already installed
  if (checkLegendAI()) {
    console.log('✓ legend-ai is already installed');
    console.log('\nYou can now use: legend --help');
    return;
  }

  // Offer to install
  console.log('\nlegend-ai Python package is not installed.');
  console.log('Installing now...');

  if (installLegendAI()) {
    console.log('\n✓ Setup complete!');
    console.log('\nQuick start:');
    console.log('  legend config init      # Initialize config');
    console.log('  legend analyze AAPL     # Analyze a stock');
    console.log('  legend tui              # Interactive mode');
    console.log('  legend --help           # Show help');
  } else {
    console.log('\nManual installation required:');
    console.log('  pip install legend-ai');
  }
}

main();
