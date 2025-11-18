# Homebrew Formula for Legend AI CLI
class LegendAi < Formula
  include Language::Python::Virtualenv

  desc "Professional trading pattern scanner and analysis CLI"
  homepage "https://github.com/Stockmasterflex/legend-ai-python"
  url "https://github.com/Stockmasterflex/legend-ai-python/archive/v1.0.0.tar.gz"
  sha256 "YOUR_SHA256_HERE"  # Update this with actual SHA256
  license "MIT"

  depends_on "python@3.11"
  depends_on "postgresql"

  resource "typer" do
    url "https://files.pythonhosted.org/packages/typer/typer-0.12.0.tar.gz"
    sha256 "TYPER_SHA256_HERE"
  end

  resource "rich" do
    url "https://files.pythonhosted.org/packages/rich/rich-13.7.0.tar.gz"
    sha256 "RICH_SHA256_HERE"
  end

  # Add other resources as needed

  def install
    virtualenv_install_with_resources
  end

  def caveats
    <<~EOS
      Legend AI CLI has been installed!

      To get started:
        1. Initialize config: legend config init
        2. Set API URL: legend config set api_url http://localhost:8000
        3. Check health: legend health
        4. Analyze a stock: legend analyze AAPL

      For interactive mode:
        legend tui

      For help:
        legend --help

      Documentation: https://github.com/Stockmasterflex/legend-ai-python
    EOS
  end

  test do
    system "#{bin}/legend", "--version"
    system "#{bin}/legend", "--help"
  end
end

# Installation:
# 1. Save this file to: /usr/local/Homebrew/Library/Taps/homebrew/homebrew-core/Formula/legend-ai.rb
# 2. Or create a tap: brew tap Stockmasterflex/legend-ai
# 3. Install: brew install legend-ai
#
# Tap Installation (recommended for development):
# 1. Create tap repo: https://github.com/Stockmasterflex/homebrew-legend-ai
# 2. Add formula: formula/legend-ai.rb
# 3. Install: brew tap Stockmasterflex/legend-ai && brew install legend-ai
