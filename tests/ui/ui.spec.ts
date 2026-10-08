import { test, expect } from '@playwright/test';

test('Calculator UI works correctly', async ({ page }) => {
  const baseURL = process.env.BASE_URL || 'http://localhost:8080';
  await page.goto(baseURL);
  
  // Verify title is correct
  await expect(page).toHaveTitle('AI Calculator Web App');
  
  // Fill in numbers
  await page.fill('#num1', '10');
  await page.fill('#num2', '5');
  
  // Click add
  await page.click('button:has-text("+")');
  
  // Verify result
  const result = page.locator('#result');
  await expect(result).toHaveText('Result: 15');
  
  // Fill zero and test division by zero
  await page.fill('#num2', '0');
  await page.click('button:has-text("÷")');
  await expect(result).toHaveText('Cannot divide by zero!');
});
