const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const browser = await puppeteer.launch({ headless: 'new' });
  const page = await browser.newPage();
  
  const htmlPath = path.resolve(__dirname, 'playbook-final.html');
  await page.goto(`file://${htmlPath}`, { waitUntil: 'networkidle0', timeout: 30000 });
  
  // Wait for fonts to load
  await page.evaluateHandle('document.fonts.ready');
  
  await page.pdf({
    path: path.resolve(__dirname, 'The-AI-Co-Founder-Playbook.pdf'),
    format: 'A4',
    margin: { top: '2.5cm', bottom: '2.5cm', left: '2.2cm', right: '2.2cm' },
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<span></span>',
    footerTemplate: `
      <div style="width: 100%; text-align: center; font-size: 9px; color: #6B7D8D; font-family: Inter, sans-serif; padding-top: 8px;">
        <span class="pageNumber"></span>
      </div>
    `,
  });
  
  await browser.close();
  console.log('PDF generated successfully');
})();
