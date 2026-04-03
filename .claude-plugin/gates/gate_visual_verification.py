#!/usr/bin/env python3
"""Gate Visual Verification: Playwright headless check that the page renders correctly."""

import sys
import pathlib
import json
import tempfile
import os
import subprocess

PROJECT_ROOT = pathlib.Path.cwd()
GATE_SCRIPT = pathlib.Path(__file__).parent

sys.path.insert(0, str(GATE_SCRIPT))
from _json_output import gate_exit

def check_dev_server_running() -> bool:
    """Check if bun dev is running on port 3000."""
    import urllib.request
    try:
        req = urllib.request.Request("http://localhost:3000")
        urllib.request.urlopen(req, timeout=3)
        return True
    except Exception:
        return False

def run_playwright_check() -> dict:
    """Run a Playwright headless script to verify page renders."""
    script_content = """
const { chromium } = require('playwright');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const errors = [];
  page.on('console', msg => {
    if (msg.type() === 'error') errors.push(msg.text());
  });
  page.on('pageerror', err => errors.push(err.message));

  try {
    const response = await page.goto('http://localhost:3000', { waitUntil: 'networkidle', timeout: 15000 });
    if (!response || response.status() >= 400) {
      const msg = { status: 'fail', message: 'Page returned HTTP ' + (response ? response.status() : 'no response') };
      console.log(JSON.stringify(msg));
      await browser.close();
      process.exit(1);
    }
    const body = await page.content();
    const hasNav = body.includes('nav') || body.includes('Nav') || body.includes('router-link');
    const hasContent = body.includes('<form') || body.includes('UCard') || body.includes('UForm') || body.includes('<main') || body.includes('<button');
    const hasBody = body.trim().length > 500;

    if (errors.length > 0) {
      const msg = { status: 'fail', message: 'Console errors: ' + errors.join('; ') };
      console.log(JSON.stringify(msg));
      await browser.close();
      process.exit(1);
    }
    if (!(hasNav || hasContent || hasBody)) {
      const msg = { status: 'fail', message: 'Page appears empty — no nav, form, or content found' };
      console.log(JSON.stringify(msg));
      await browser.close();
      process.exit(1);
    }
    const msg = { status: 'pass', message: 'Page renders correctly' };
    console.log(JSON.stringify(msg));
  } catch (e) {
    const msg = { status: 'fail', message: 'Exception: ' + e.message };
    console.log(JSON.stringify(msg));
    await browser.close();
    process.exit(1);
  }
  await browser.close();
  process.exit(0);
})();
"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.js', delete=False) as f:
        f.write(script_content)
        script_path = f.name

    try:
        result = subprocess.run(
            ['node', script_path],
            capture_output=True,
            text=True,
            cwd=str(PROJECT_ROOT),
            timeout=30,
        )
        try:
            return json.loads(result.stdout.strip())
        except Exception:
            return {'status': 'fail', 'message': 'Could not parse output: ' + result.stdout + ' stderr: ' + result.stderr}
    finally:
        os.unlink(script_path)

def main() -> int:
    print("=== Gate Visual Verification ===\n")

    if not check_dev_server_running():
        return gate_exit('visual_verification', [{
            'check': 'dev_server',
            'status': 'fail',
            'message': 'bun dev is not running on port 3000',
            'fix': 'Start bun dev before running this gate',
        }])

    print("Dev server: running\n")
    result = run_playwright_check()

    checks = [{
        'check': 'page_renders',
        'status': result['status'],
        'message': result.get('message', 'unknown'),
    }]

    for c in checks:
        symbol = {'pass': '✅', 'fail': '❌'}.get(c['status'], '?')
        print(f"{symbol} {c['message']}")

    return gate_exit('visual_verification', checks)

if __name__ == '__main__':
    sys.exit(main())
