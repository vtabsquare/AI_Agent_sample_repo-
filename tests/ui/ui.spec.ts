import { test, expect } from '@playwright/test';

test('Server responds successfully', async ({ page }) => {
  const baseURL = process.env.BASE_URL || 'http://localhost:8080';
  const response = await page.goto(baseURL);
  expect(response?.ok()).toBeTruthy();
});
