import fs from 'fs';
import path from 'path';

function auditUI() {
  console.log('Running Autonomous Anti-Slop & Design Audit...');
  const readmePath = path.resolve(process.cwd(), 'README.md');
  if (!fs.existsSync(readmePath)) {
    console.error('FAIL: README.md not found.');
    process.exit(1);
  }

  const content = fs.readFileSync(readmePath, 'utf8');
  const violations = [];

  // Check 1: Forbidden pseudo-military word DISPATCH
  if (/\bdispatch\b/i.test(content)) {
    violations.push('Violation: Forbidden pseudo-military word "DISPATCH" found.');
  }

  // Check 2: Card soup cliches
  if (/rounded-xl border bg-surface/i.test(content)) {
    violations.push('Violation: Generic card soup classes detected.');
  }

  // Check 3: Asset references integrity
  const imgMatches = content.match(/src="([^"]+)"/g) || [];
  for (const m of imgMatches) {
    const src = m.match(/src="([^"]+)"/)[1];
    if (src.startsWith('./assets/') || src.startsWith('assets/')) {
      const cleanPath = path.resolve(process.cwd(), src.replace(/^\.\//, ''));
      if (!fs.existsSync(cleanPath)) {
        violations.push(`Violation: Asset does not exist on disk: ${src}`);
      }
    }
  }

  if (violations.length > 0) {
    console.error('Audit failed with violations:');
    violations.forEach(v => console.error(' - ' + v));
    process.exit(1);
  }

  console.log('PASS: All Anti-Slop, Typographic, and Asset Integrity checks passed.');
}

auditUI();
